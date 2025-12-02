from chromadb import PersistentClient
from ...config.settings import Config
from pathlib import Path
import os
import logging
import yaml
import uuid
import json

class KnowledgeStore:
    def __init__(self, kowledge_path: Path):
        self.vector_client=None
        self._initialize_vector_db(Config.CHROMADB_PERSISTANCE_PATH)
        self.knowledge_dir=kowledge_path
        self.collection=None

    
    def _initialize_vector_db(self, path: Path):
        if(not path.exists()):
            logging.error("Path for persistent VectorDB storage MUST be a valid directory.")
            raise FileNotFoundError(path)
        try:
            self.vector_client=PersistentClient(path=path)
            self.vector_client.heartbeat()
            logging.info(f"Successfully initialized ChromeDB Persistent Client for {self.vector_client.database}")
        except Exception as e:
            logging.error("Failed to initialize ChromaDB Persistent Client.")
            raise
    
    def process_knowledge(self):
        try:
            if(Config.SKILL_COLLECTION_NAME in [collection.name for collection in self.vector_client.list_collections()]):
                self.vector_client.delete_collection(Config.SKILL_COLLECTION_NAME)
            self.collection=self.vector_client.get_or_create_collection(Config.SKILL_COLLECTION_NAME)
        except Exception as e:
            logging.error(f"Failed to initialize ChromaDB collection: {Config.SKILL_COLLECTION_NAME}")
            raise
        
        if(not self.knowledge_dir.exists()):
            logging.error("Path for knowledge store data MUST be a valid directory.")
            raise FileNotFoundError(self.knowledge_dir)
        skills_dir_path=self.knowledge_dir.joinpath(Config.SKILL_KNOWLEDGE_DIR)
        if(not skills_dir_path.exists()):
            logging.error("Path for skill-specific knowledge store data MUST be a existing directory.")
            raise FileNotFoundError(skills_dir_path)
        
        skill_paths=list(skills_dir_path.glob('**/*.y[a]ml'))
        skill_details=[]
        for skill_path in skill_paths:
            skill_details.append(KnowledgeStore.parse_skill_file(skill_file_path=skill_path))
        
        
        skill_docs=[]
        for skill_detail in skill_details:
            skill_name=skill_detail.get("skill_name","").strip()
            definition=skill_detail.get("definition","").strip()
            related_skills=skill_detail.get("related_skills",[])
            resume_manifestations=skill_detail.get("resume_manifestations",[])
            specific_tools=skill_detail.get("specific_tools",[])
            category=skill_detail.get("category","").strip()
            source=skill_detail.get("source","").strip()


            id = str(uuid.uuid4())
            content=f"Skill: {skill_name}\Definition: {definition}\nSimilar Skills: {",".join(related_skills)}"
            metadata={
                "type":"definition",
                "skill": skill_name,
                "category": category,
                "source": source
            }
            skill_docs.append([id,content,metadata])

            for manifestation in resume_manifestations:
                id = str(uuid.uuid4())
                content=f"Resume example: {manifestation} demonstrates skill: {skill_name}"
                metadata={
                    "type":"manifestation",
                    "skill": skill_name,
                    "source": source
                }
                skill_docs.append([id,content,metadata])
            
            for tool in specific_tools:
                id = str(uuid.uuid4())
                content=f"Tool: {tool} is a tool for: {skill_name}"
                metadata={
                    "type":"tool",
                    "skill": skill_name,
                    "tool":tool,
                    "source": source
                }
                skill_docs.append([id,content,metadata])
        self._embed_document(skill_docs=skill_docs)
        
    def _embed_document(self,skill_docs):
        try:
            self.collection.add(
                ids=[doc[0] for doc in skill_docs],
                documents=[doc[1] for doc in skill_docs],
                metadatas=[doc[2] for doc in skill_docs]
            )
            logging.info(f"Successfully embedded {len(skill_docs)} chunks")
        except Exception as e:
            logging.error("Failed to embed chunks.")
            raise

    
    def query_vector_db(self, query: str, n_results:int, doc_type:str= None):
        if(self.collection==None):
            try:
                self.collection=self.vector_client.get_collection(Config.SKILL_COLLECTION_NAME)
                logging.info(f"Successfully retrieved ChromaDB collection: {Config.SKILL_COLLECTION_NAME}.")
            except:
                logging.error(f"Failed to get ChromaDB collection: {Config.SKILL_COLLECTION_NAME}.")
                raise
        results=None
        try:
            if(doc_type):
                results=self.collection.query(query_texts=[query],n_results=n_results, where={"type":doc_type})
            else:
                results=self.collection.query(query_texts=[query],n_results=n_results)
        except Exception as e:
            logging.error(f"Failed to query ChromaDB collection {Config.SKILL_COLLECTION_NAME}.")
            raise

        logging.info(f"Sucessfully qeried {len(results["ids"][0])} results from ChromaDB collection {Config.SKILL_COLLECTION_NAME}.")
        return list(zip(results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0]))


    
    @staticmethod
    def parse_skill_file(skill_file_path: Path):
        skill_details=None
        try:
            with open(skill_file_path, 'r') as f:
                skill_details=yaml.safe_load(f)
                skill_details["source"]= skill_file_path.name
                logging.info(f"Successfully parsed file: {skill_file_path}.")
        except:
            logging.error(f"Failed to parse skill file :{skill_file_path}")
            raise()
        return skill_details
        


    