# Databricks notebook source
# MAGIC %pip install azure-storage-blob azure-cosmos

# COMMAND ----------

# MAGIC %pip uninstall openai

# COMMAND ----------

# MAGIC %pip install openai

# COMMAND ----------

# MAGIC %pip install --upgrade openai

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Import libraries

# COMMAND ----------

from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from openai import AzureOpenAI
import requests
import json
import re
from io import BytesIO
import time
import datetime 
import tempfile
import pytz
import uuid
import logging

# COMMAND ----------

# MAGIC %md
# MAGIC ### Set input parameters

# COMMAND ----------

dbutils.widgets.text("fileName", "08ebc5b7-3418-4ba0-9d60-643a685f5447.json")
id_request = dbutils.widgets.get("fileName")[:-5]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Set variables

# COMMAND ----------

STORAGE_ACCOUNT_NAME = "sapocvinculadorcr"
STORAGE_ACCOUNT_KEY = "2/FBxN0FLN1+R+nhpYlpjyGh8qtsnHA9jBV6LZoqtRaSsHTVVuSV2v6hjAQNkG54JHbBGHG0Oues+AStr1DLpQ=="
STORAGE_ACCOUNT_CONTAINER = "poc-vinculador-files-processed"
STORAGE_ACCOUNT_CONTAINER_SAS_TOKEN = "sp=racwdl&st=2025-01-20T13:33:30Z&se=2028-01-20T21:33:30Z&spr=https&sv=2022-11-02&sr=c&sig=LjbdkvUcVtusw5A2PAlcfZdop7Xa4q0QM5v08oWP0Ac%3D"
AZURE_OPENAI_ENDPOINT = "https://oai-poc-vinculador-cr.openai.azure.com/"
AZURE_OPENAI_KEY = "6kmXHwxEWbIcpqKnHa6Wvu9Xp0Q1rtjk7iOYb1MiQaV0Q5MxR2IjJQQJ99ALACYeBjFXJ3w3AAABACOGZ26i"
COSMOS_URI = "https://cd-poc-vinculador-cr.documents.azure.com:443/"
COSMOS_KEY = "2vh9dmM8wBi3F7z82n4DxUi67HLz7hklv394xaSRSiwnTugaqZK1W2Wlau7AUApd2SUdS2W4YTQpACDbri3eCw=="
AZURE_OPENAI_ENDPOINT = "https://oai-poc-vinculador-cr.openai.azure.com/"
OPENAI_API_KEY = "6kmXHwxEWbIcpqKnHa6Wvu9Xp0Q1rtjk7iOYb1MiQaV0Q5MxR2IjJQQJ99ALACYeBjFXJ3w3AAABACOGZ26i"
OPENAI_API_VERSION = "2024-07-01-preview"
APP_NAME = "vinculador_model_processing"
AUDTIS_API_URL_BASE = "https://azfunc-audits-cr.azurewebsites.net/api"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Connect to Cosmos DB

# COMMAND ----------

cosmos_client = CosmosClient(COSMOS_URI, COSMOS_KEY)
cosmos_database = cosmos_client.get_database_client("vinculador-db")
cosmos_container = cosmos_database.get_container_client("analysis")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Connect to Storage Account

# COMMAND ----------

endpoint = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
blob_service_client = BlobServiceClient(account_url=endpoint, credential=STORAGE_ACCOUNT_KEY)
container_client = blob_service_client.get_container_client(STORAGE_ACCOUNT_CONTAINER)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Functions

# COMMAND ----------

def getSubfoldersInFolder(specific_folder):
    subfolders = set()
    for blob in container_client.list_blobs(name_starts_with=specific_folder):
        remaining_path = blob.name[len(specific_folder):]
        if "/" in remaining_path:
            subfolder = remaining_path.split("/")[0]
            subfolders.add(subfolder)

    return subfolders

# COMMAND ----------

def getFilesInSubfolder(subfolder):
    files = {}
    for blob in container_client.list_blobs(name_starts_with=subfolder):
        remaining_path = blob.name[len(subfolder):] 
        if remaining_path:
            file_name = remaining_path.split("/")[-1]
            file_url = f"{endpoint}/{container_client.container_name}/{blob.name}"
            files[file_name] = file_url

    return files

# COMMAND ----------

def get_document_text(url):
    try:
        response = requests.get(url)
        document_text = response.text
        return document_text
    except Exception as e:
        print(f"An error occurred: {e}")

# COMMAND ----------

def write_jsonl_file(file_path, data):

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        for entry in data:
            temp_file.write(json.dumps(entry) + '\n')  # Write each dictionary as a line
        temp_file_path = temp_file.name

    # Use Databricks utilities to move the temporary file to Azure Blob Storage
    try:
        dbutils.fs.mv(f"file://{temp_file_path}", file_path)
        print(f"File successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing file to Azure Blob Storage: {e}")

# COMMAND ----------

def execute_openai_batch(id_request):

    client = AzureOpenAI(
        api_key=OPENAI_API_KEY,  
        api_version="2024-10-21",
        azure_endpoint = AZURE_OPENAI_ENDPOINT
    )

    file = client.files.create(
        file=open(f"/dbfs/mnt/poc-vinculador-gpt-files/gpt_call_{id_request}.jsonl", "rb"), 
        purpose="batch"
    )

    print(file.model_dump_json(indent=2))
    file_id = file.id

    status = "pending"
    while status != "processed":
        time.sleep(10)
        file_status = client.files.retrieve(file_id)
        status = file_status.status
        print(f"File status: {status}")

        if status in ["failed", "error"]:
            return []

    batch_response = client.batches.create(
        input_file_id=file_id,
        endpoint="/chat/completions",
        completion_window="24h",
    )

    batch_id = batch_response.id

    status = "validating"
    while status not in ("completed", "failed", "canceled"):
        time.sleep(60)
        batch_response = client.batches.retrieve(batch_id)
        status = batch_response.status
        print(f"{datetime.datetime.now()} Batch Id: {batch_id},  Status: {status}")

    if batch_response.status == "failed":
        for error in batch_response.errors.data:  
            print(f"Error code {error.code} Message {error.message}")

    if batch_response.status == "completed":
        output_file_id = batch_response.output_file_id

        if not output_file_id:
            output_file_id = batch_response.error_file_id

        if output_file_id:
            file_response = client.files.content(output_file_id)
            raw_responses = file_response.text.strip().split('\n')  
            formatted_json = [json.loads(raw_response) for raw_response in raw_responses]

            return formatted_json

# COMMAND ----------

def getAliadoItem(id_request):
    query = f"SELECT * FROM c WHERE c.id = '{id_request}'"
    print(f"QUERY: {query}")
    item = cosmos_container.query_items(query=query, enable_cross_partition_query=True)
    return list(item)

# COMMAND ----------

def get_epoch_time(timezone:str):
    timezone_tz = pytz.timezone(timezone)
    time = datetime.datetime.now(timezone_tz)
    epoch_time = int(time.timestamp())
    return epoch_time

def format_epoch_time(epoch_time: int, timezone: str) -> str:
    timezone_tz = pytz.timezone(timezone)
    time = datetime.datetime.fromtimestamp(epoch_time, timezone_tz)
    return time.strftime("%d/%m/%Y %H:%M:%S")

# COMMAND ----------

def successful_execution(final_results):

    formatted_time = format_epoch_time(final_results["createdAt"], "America/Bogota")
    number_of_results = len(final_results["response"])
    compatibility_count = sum(1 for element in final_results["response"] if element["result"]=="Elegible")
    table_data = []
    for element in final_results["response"]:
        if element["result"] == "Elegible":
            element_relevant_features = {
            "proyecto": element["project"],
            "aliado":  element["ally"],
            "cantidad de compatibilidad": element["compatibilityCount"]}

            table_data.append(element_relevant_features)

    table_data = sorted(table_data, key=lambda x: x["cantidad de compatibilidad"], reverse=True)

    url = "https://azfunc-poc-notifications-cr.azurewebsites.net/api/email-notification"
    headers = {
    "Content-Type": "application/json"
    }
    data = {
    "idProject": "VINCULADOR_DMAF",
    "typeNotification": "EMIAL",
    "notification": "SUCCESS_FINALLY_PROCESS",
    "data": [
        {
            "label": "{{createdAt}}",
            "value": formatted_time
        },
        {
            "label": "{{id}}",
            "value": final_results["id"]
        },
        {
            "label": "{{count}}", 
            "value": number_of_results
        },
        {
            "label": "{{compatibilityCount}}",
            "value": compatibility_count
        }
        ],
        "table": table_data
    }

    response = requests.post(url, json=data, headers=headers)

# COMMAND ----------

def error_execution(final_results):

    formatted_time = format_epoch_time(final_results["createdAt"], "America/Bogota")
    url = "https://azfunc-poc-notifications-cr.azurewebsites.net/api/email-notification"
    headers = {
    "Content-Type": "application/json"
    }
    data = {
    "idProject": "VINCULADOR_DMAF",
    "typeNotification": "EMIAL",
    "notification": "ERROR_FINALLY_PROCESS",
    "data": [
            {
                "label": "{{createdAt}}",
                "value": formatted_time
            },
            {
                "label": "{{id}}",
                "value": final_results["id"]
            }
        ]
    }   

    response = requests.post(url, json=data, headers=headers)

# COMMAND ----------

def save_logging(data):
    try:
        url = f"{AUDTIS_API_URL_BASE}/audits"
        headers = {
        "Content-Type": "application/json"
        }
        data["appName"] = APP_NAME
        response = requests.post(url, json=data, headers=headers)
        return response
    except Exception as e:
        logging.exception(f"[save_logging] - Error: {e}")
        raise

# COMMAND ----------

# MAGIC %md
# MAGIC ### Execution

# COMMAND ----------

log = {
            "user": "SYSTEM",
            "action": "UPDATE",
        }
try:
    allies_folders = list(getSubfoldersInFolder("allies/"))
    projects_folders = list(getSubfoldersInFolder("projects/"))

    json_batch_gpt_elements = []

    for ally in allies_folders:
        
        specific_subfolder_allies = f"allies/{ally}/"
        ally_files = getFilesInSubfolder(specific_subfolder_allies)
        ally_unique_file = list(ally_files.items())[0]
        ally_file_name = ally_unique_file[0]
        ally_file_url = ally_unique_file[1] + "?" + STORAGE_ACCOUNT_CONTAINER_SAS_TOKEN
        ally_file_content = get_document_text(ally_file_url)

        for project in projects_folders:
            specific_subfolder_projects = f"projects/{project}/"
            projects_files = getFilesInSubfolder(specific_subfolder_projects)
            list_projects_files = list(projects_files.items())

            projects_text = ""

            for project_file in list_projects_files:
                project_file_url = project_file[1] + "?" + STORAGE_ACCOUNT_CONTAINER_SAS_TOKEN
                project_file_content = get_document_text(project_file_url)
                projects_text += project_file_content

            system_prompt = """
            Eres un asistente preciso y orientado a los detalles encargado de determinar si un proyecto cumple con los requisitos generales para financiamiento. 

            ### Tus Objetivos:
            1. Analizar una lista predefinida de **Requisitos de Financiamiento**.
            2. Comparar estos requisitos con la **Información del Proyecto** proporcionada.
            3. Determinar y devolver **únicamente un JSON válido** con las siguientes claves:
            - **estado_general**: "Elegible" (si al menos un requisito es satisfecho) o "No Elegible" (si ningún requisito es satisfecho).
            - **explicacion_general**: 
                - Si es "Elegible," justifica con base en qué requisitos fueron cumplidos.
                - Si es "No Elegible," proporciona el mensaje: "Ninguno de los lineamientos de elegibilidad del aliado son satisfechos por el proyecto."
            - **pais**: El nombre del país donde se ejecutará el proyecto. Si no se especifica, devuelve "No especificado".
            - **conteo_compatibilidad**: El número de requisitos que son cumplidos.

            ### Directrices:
            - **La respuesta debe ser exclusivamente un JSON válido**, sin texto adicional, explicaciones o comentarios fuera del JSON.
            - Si no se proporciona información suficiente para determinar un atributo, devuelve "No especificado" para ese campo.
            - Asegúrate de que el JSON esté correctamente formado y no contenga errores de sintaxis.
            - Asegúrate de que todas las respuestas sean solamente en idioma español.
            """

            user_prompt = f"""
            A continuación se presentan los **Requisitos de Financiamiento** y la **Información del Proyecto**. 
            Evalúa el cumplimiento del proyecto y devuelve **únicamente un JSON válido** con las siguientes claves:

            - **estado_general**: "Elegible" o "No Elegible."
            - **explicacion_general**: 
                - Si es "Elegible," explica de manera clara y precisa cuáles requisitos se cumplen.
                - Si es "No Elegible," proporciona el mensaje: "Ninguno de los lineamientos de elegibilidad del aliado son satisfechos por el proyecto."
            - **pais**: Especifica el nombre del país donde se ejecutará el proyecto. Si no se especifica, devuelve "No especificado".
            - **conteo_compatibilidad**: Indica la cantidad de requisitos cumplidos.

            **Requisitos de Financiamiento:**
            {ally_file_content}

            **Información del Proyecto:**
            {projects_text}

            **Nota:** La respuesta debe ser exclusivamente un JSON válido, sin texto adicional, explicaciones o comentarios fuera del JSON.
            """

            json_batch_gpt_element = {
                "custom_id": f"{ally}-{project}",
                "method": "POST", 
                "url": "/chat/completions", 
                "body": {"model": "gpt-4o-batch", 
                        "messages": [{"role": "system", "content": system_prompt}, 
                                    {"role": "user", "content": user_prompt}]}
                }
            
            json_batch_gpt_elements.append(json_batch_gpt_element)

    write_jsonl_file(f"dbfs:/mnt/poc-vinculador-gpt-files/gpt_call_{id_request}.jsonl", json_batch_gpt_elements)

    gpt_batch_response = execute_openai_batch(id_request=id_request)

    results = []

    for element in gpt_batch_response:
        result = {}
        
        ally_name = element["custom_id"].split('-')[0]
        project_name = element["custom_id"].split('-')[1]

        try:
            response = element["response"]["body"]["choices"][0]['message']['content'].strip()

            response = re.sub(r'```json|```', '', response)
            response = response.strip()
    
            if not response.startswith("{") or not response.endswith("}"):
                raise ValueError("Invalid JSON format: " + response)

            response_dict = json.loads(response)

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            print("Raw Response:", response)

        status = response_dict["estado_general"]
        explanation = response_dict["explicacion_general"]
        country = response_dict["pais"]
        compatibility_count = response_dict["conteo_compatibilidad"]

        uuid_value = uuid.uuid4()
        result["idResponse"] = str(uuid_value)
        result["ally"] = ally_name
        result["project"] = project_name 
        result["country"] = country
        result["result"] = status
        result["detail"] = explanation
        result["compatibilityCount"] = compatibility_count
        result["isQualified"] = True if status == "Elegible" else False
        result["userCommentary"] = None
        result["isApprovedByUser"] =  False if compatibility_count == 0 else None
        
        results.append(result) 

    current_time = get_epoch_time("America/Bogota")

    item = getAliadoItem(id_request)[0]
    print("get_item: ", item)
    item["response"] = results
    item["status"] = "FINISHED"
    item["updatedAt"] = current_time
    print("item_for_update: ", item)
    cosmos_container.replace_item(item=item, body=item)

    log["response"] = json.dumps(item)
    log["isSuccess"] = True
    save_logging(log)

    successful_execution(item)

except Exception as e:
    current_time = get_epoch_time("America/Bogota")
    item = getAliadoItem(id_request)[0]
    item["response"] = {"errorDescription": str(e)}
    item["status"] = "ERROR"
    item["updatedAt"] = current_time
    cosmos_container.replace_item(item=item["id"], body=item)
    log["error"] = str(e)
    log["isSuccess"] = False
    save_logging(item)
    error_execution(item)
    print(e)
