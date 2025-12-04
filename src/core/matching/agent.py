from ...models.database import DatabaseManager
from ...models.entities import Resume, Job
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from ...config.settings import Config
from ..knowledge.store import KnowledgeStore
from .context_builder import ContextBuilder   
import yaml, json
import time

class MatchingAgent:
    def __init__(self):
        self.db_manager=DatabaseManager()
        self.llm = Ollama(model="llama3.2", temperature=0)

        # Initialize KnowledgeStore once - it can be reused for all job matchings
        self.knowledge_store = KnowledgeStore(Config.KNOWLEDGE_PATH)

        prompts_file=Config.PROMPT_DIR.joinpath("matching.yaml")
        if(not prompts_file.exists()):
            raise Exception("MatchingAgent prompt file foes not exist")
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)
    
    def match_all_jobs(self):
        # GET ACTIVE RESUME
        active_resume=self.db_manager.get_active_resume()
        print(f"ACTIVE RESUME: {active_resume.id}")
        # GET ALL UNPROCESSED JOBS
        unprocessed_jobs=self.db_manager.get_all_unprocessed_jobs()
        print(f"Processing {len(unprocessed_jobs[:10])} jobs...\n")

        # Collect all match results
        results = []
        for job in unprocessed_jobs[:10]:
            self.match_job(active_resume, job)
            # match_result = self.match_job(active_resume, job)
        #     results.append({
        #         'job': job,
        #         'match': match_result
        #     })

        # # Sort results by recommendation priority
        # recommendation_order = {
        #     'STRONG MATCH': 1,
        #     'GOOD MATCH': 2,
        #     'MODERATE MATCH': 3,
        #     'WEAK MATCH': 4,
        #     'POOR MATCH': 5
        # }

        # sorted_results = sorted(
        #     results,
        #     key=lambda x: (
        #         recommendation_order.get(x['match'].get('recommendation', 'POOR MATCH'), 6),
        #         -x['match'].get('total_score', 0)
        #     )
        # )

        # # Print sorted results
        # print("\n" + "=" * 80)
        # print("SORTED RESULTS (Best to Worst)")
        # print("=" * 80)
        # for i, result in enumerate(sorted_results, 1):
        #     job = result['job']
        #     match = result['match']
        #     print(f"\n{i}. {job.title} at {job.company}")
        #     print(f"   Score: {match.get('total_score')}/100 - {match.get('recommendation')}")
        #     print(f"   URL: {job.url}")
        #     print(f"   Matching Skills: {match.get('matching_skills')}")
        #     print(f"   Missing Skills: {match.get('missing_skills')}")

        # return sorted_results

    def match_job(self, resume:Resume, job:Job):
        return self._llm_match_job(resume, job)
    
    def _llm_match_job(self, resume:Resume, job:Job):
        # Build context using ContextBuilder for this specific job-resume pair
        context_builder = ContextBuilder(
            resume=resume,
            job=job,
            knowledge_store=self.knowledge_store
        )
        skill_context = context_builder.build_context()

        prompt=PromptTemplate.from_template(self.prompts.get("job_matching")).format(
        resume_name=resume.name or '',
        resume_skills=resume.skills or '',
        resume_experience=resume.experience or '',
        resume_education=resume.education or '',
        resume_summary=resume.summary or '',
        job_title=job.title,
        job_company=job.company,
        job_description=job.description or '',
        job_requirements=job.requirements or '',
        job_key_technologies=job.key_technologies or '',
        skill_context=skill_context
        )
        print(prompt)
        # start_time = time.perf_counter()
        # try:
        #     resp=self.llm.invoke(prompt)
        #     resp_obj=json.loads(resp)
        # except Exception as e:
        #     print("LLM Inference ERROR")
        #     raise Exception(e)
        # end_time = time.perf_counter()

        # elapsed_time = end_time - start_time
        # print(f"Processed: {job.title} at {job.company} - Score: {resp_obj.get('total_score')}/100 - {resp_obj.get('recommendation')} ({elapsed_time:.2f}s)")
        # return resp_obj
