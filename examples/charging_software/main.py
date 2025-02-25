import logging
import os
import json
from modules.ontology import generate_ontology
from modules.kg_processing import build_knowledge_graph
from graphrag_sdk.models.litellm import LiteModel
from graphrag_sdk.models.ollama import OllamaGenerativeModel
from graphrag_sdk.models.gemini import GeminiGenerativeModel
from graphrag_sdk.model_config import KnowledgeGraphModelConfig
from graphrag_sdk.source import Source
from graphrag_sdk import KnowledgeGraph, Ontology
from graphrag_sdk.source import URL

MODEL_TYPE = "gemini"  # Switch to "ollama", "litellm" 


def select_model(model_name:str):

    if MODEL_TYPE == "litellm":
        model = LiteModel(model_name="deepseek/deepseek-chat")
        # model = LiteModel(model_name="deepseek/deepseek-reasoner")
    elif MODEL_TYPE == "groq":
        model = LiteModel(model_name="groq/deepseek-r1-distill-llama-70b")
    elif MODEL_TYPE == "openrouter":
        model = LiteModel(model_name="openrouter/deepseek/deepseek-r1:free")
    elif MODEL_TYPE == "ollama":
        model = OllamaGenerativeModel(model_name="deepseek-r1:14b")
    elif MODEL_TYPE == "gemini":
        model = GeminiGenerativeModel(model_name="models/gemini-2.0-flash-exp")
    else:
        logging.info("Specify LLM to be used.")

    return model
        

def generte_ontologies(sources:list[Source], model, f_name:str):
    pass

def merge_ontologies(ontologies_dir:str):
    pass

def build_knowledge_graph(ontology:Ontology, model):
    pass

def chat_with_knowledge_graph(kg, query:str):
    pass


def query_kg(chat, question: str):
    return chat.send_message(question)



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    folder = "ocpp"  # "everest-core"
    path_in = "/Users/david/Development/fenexity/data/graph_repos"
    # test


    # select model
    model = select_model(MODEL_TYPE) 
    
    ################### CREATE ONTOLOGIES FROM SOURCES ########################
    # Source configuration: Data folder.
    src_files = path_in+"/"+folder
    sources = []

    # For each file in the source directory and its subdirectories, create a new Source object.

    ignore_extensions = ['.gitignore', '.tmp', '.log', '.bak']  # Liste der zu ignorierenden Endungen
    for root, dirs, files in os.walk(src_files):
        # Filter out .github directory
        dirs[:] = [d for d in dirs if d != '.github']
        for file in files:
            # Hier können spezifische Dateifilter hinzugefügt werden, z.B. nur .txt-Dateien
            if any(file.endswith(ext) for ext in ignore_extensions):
                continue
            sources.append(Source(os.path.join(root, file)))

    f_name = "ontology_"+folder+".json"
    ## Generate ontology
    generate_ontology(sources, model, f_name)

    ######################### MERGE JSON ONTOLOGIES ###########################

    # ontologies_dir = "examples"+"/"+"charging_software"+"/"+"04_ontologies"
    # target_dir = "examples"+"/"+"charging_software"+"/"+"05_merged_ontologies"

    # merged = merge_ontology_directory(ontologies_dir)

    # # Save merged ontology
    # with open(os.path.join(target_dir, "merged_ontology.json"), "w") as f:
    #     json.dump(merged.to_json(), f, indent=2)

    ########### CREATE KNOWLEDGE GRAPH FROM (MERGED) ONTOLOGIES ###############

    # ontologies_dir = "examples"+"/"+"charging_software"+"/"+"04_ontologies"
    # name_onto = "ontology_"+folder
    # fname_onto = name_onto+".json"

    # ontology_dir = f"examples/charging_software/test/{f_name}"
    ontology_dir = "examples/charging_software/04_ontologies/ontology_citrineos-core.json"

    f_name = os.path.basename(ontology_dir).replace(".json", "")

    with open(ontology_dir, "r") as f:
        ontology = Ontology.from_json(json.loads(f.read()))

    # Build knowledge graph with unified config
    kg = KnowledgeGraph(
        name=f_name,
        model_config=KnowledgeGraphModelConfig.with_model(model),
        ontology=ontology,
        host="localhost",
        port=6379
    )
    
    kg.process_sources(sources)  # Only if directly from sources to kg.

    ########### INTERACT WITH KNOWLEDGE GRAPH, SAVE IT AS .rdb file ###########

    # Add chat interface from quickstart
    # def query_kg(question: str):
    #     chat = kg.chat_session()
    #     return chat.send_message(question)
    

    chat = kg.chat_session()

    while True:
        question = input("Enter a question: ")
        if question == "exit":
            break
        response = query_kg(chat, question)
        print(response["response"])

    
    # print(query_kg(chat, "Explain key EV charging concepts in this knowledge base"))

    logging.info("This is the end.")
