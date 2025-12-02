from ..knowledge.store import KnowledgeStore
from ...models.entities import Job, Resume
from ...config.settings import Config
import logging
import json


class ContextBuilder:
    def __init__(self, job:Job, resume: Resume, knowledge_store: KnowledgeStore):
        if(job==None):
            logging.error(f"Job and Resume must not be None.")
            raise
        if(resume==None):
            logging.error(f"Job and Resume must not be None.")
            raise
        if(knowledge_store==None):
            logging.error(f"Job and Resume must not be None.")
            raise
        self.job=job
        self.resume=resume
        self.kt_manager=knowledge_store
        
    
    def build_context(self)->str:
        context_data={}
        job_tech=json.loads(self.job.key_technologies)
        resume_skills=json.loads(self.resume.skills)
        
        skills=set()
        for skill_set in [job_tech,resume_skills]:
            skills.update([skill.strip().lower() for skill in skill_set])
        
        for skill in list(skills):
            for definition in self.kt_manager.query_vector_db(skill, Config.PER_SKILL_DEFINITIONS, "definition"):
                skill=definition[2].get("skill")
                if(skill not in context_data):
                    context_data[skill]={
                        "definition":None,
                        "tools":set(),
                        "resume_examples":set()
                    }
                context_data[skill]["definition"]=definition[1]
            for tool in self.kt_manager.query_vector_db(skill,Config.PER_SKILL_TOOLS,"tool"):
                skill=tool[2].get("skill")
                if(skill not in context_data):
                    context_data[skill]={
                        "definition":None,
                        "tools":set(),
                        "resume_examples":set()
                    }
                context_data[skill]["tools"].add(tool[1])
        
        all_exp=[]
        resume_experiences=json.loads(self.resume.experience)
        job_requirements=json.loads(self.job.requirements)
        for experience in resume_experiences:
            all_exp.extend(experience.get("responsibilities",[]))
        all_exp.extend(job_requirements)

        for exp in all_exp:
            exp_contexts=self.kt_manager.query_vector_db(exp,3,"manifestation")
            for exp_context in exp_contexts:
                skill=exp_context[2].get("skill")
                if(skill not in context_data):
                    context_data[skill]={
                        "definition":None,
                        "tools":set(),
                        "resume_examples":set()
                    }
                context_data[skill]["resume_examples"].add(exp_context[1])
        for skill in context_data:
            context_data[skill]["tools"]=list(context_data[skill]["tools"])
            context_data[skill]["resume_examples"]=list(context_data[skill]["resume_examples"])

        # Build formatted context string for LLM
        context_string = self._format_context_for_llm(context_data)
        return context_string

    def _format_context_for_llm(self, context_data: dict) -> str:
        """
        Formats the context data into a human-readable string optimized for LLM consumption.

        Args:
            context_data: Dictionary containing skill definitions, tools, and resume examples

        Returns:
            Formatted string with technical context for each skill
        """
        if not context_data:
            return "No additional technical context available."

        context_lines = []
        context_lines.append("TECHNICAL KNOWLEDGE CONTEXT:")
        context_lines.append("=" * 80)
        context_lines.append("")

        # Sort skills alphabetically for consistent output
        sorted_skills = sorted(context_data.keys())

        for skill in sorted_skills:
            skill_info = context_data[skill]

            # Skill header
            context_lines.append(f"SKILL: {skill.upper()}")
            context_lines.append("-" * 80)

            # Definition
            if skill_info.get("definition"):
                context_lines.append(f"Definition: {skill_info['definition']}")
            else:
                context_lines.append("Definition: Not available")

            # Tools and technologies
            if skill_info.get("tools"):
                tools_str = ", ".join(skill_info["tools"])
                context_lines.append(f"Common Tools/Technologies: {tools_str}")
            else:
                context_lines.append("Common Tools/Technologies: None listed")

            # Resume examples (how this skill manifests in practice)
            if skill_info.get("resume_examples"):
                context_lines.append("Practical Applications:")
                for i, example in enumerate(skill_info["resume_examples"], 1):
                    context_lines.append(f"  {i}. {example}")
            else:
                context_lines.append("Practical Applications: None listed")

            context_lines.append("")  # Empty line between skills

        return "\n".join(context_lines)
