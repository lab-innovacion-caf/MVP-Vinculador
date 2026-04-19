import os
import json
import logging
import azure.functions as func
from src.const.const import API_URL_BASE
from src.services.vinculador_service import VinculadorService
from src.repository.comosdb_repository import CosmosdbRepository
from src.repository.blob_storage_repository import BlobStorageRepository
from src.repository.recognizer_repository import RecognizerRepository
from src.services.document_intelligence_service import DocumentIntelligenceService
from src.dto.pagination_dto import PaginationParamsDTO
from src.services.notifications_service import NotificationsService
from src.services.reminder_service import ReminderService
from src.services.logging_service import LoggingService

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

cosmosdb_connection_string = os.environ["COSMOS_DB_CONNECTION_STRING"]
cosmosdb_database_name = os.environ["COSMOS_DB_DATABASE"]
cosmosdb_container_name = os.environ["COSMOS_DB_CONTAINER"]

blob_connection_string = os.environ["BLOB_STORAGE_CONNECTION_STRING"]
blob_container_name = os.environ["BLOB_STORAGE_CONTAINER_NAME"]
blob_container_name_for_trigger = os.environ["BLOB_STORAGE_CONTAINER_NAME_FOR_TRIGGER"]
blob_container_name_from_document_intelligence= os.environ["BLOB_STORAGE_CONTAINER_NAME_FROM_DOCUMENT_INTELLIGENCE"]

form_recognizer_endpoint = os.environ["FORM_RECOGNIZER_ENDPOINT"]
form_recognizer_key= os.environ["FORM_RECOGNIZER_KEY"]

notifications_api_url_base = os.environ["NOTIFICATIONS_API_URL_BASE"]
cron_job_schedule = os.environ["CRON_JOB_SCHEDULE"]

audits_api_url_base = os.environ["AUDTIS_API_URL_BASE"]

cosmosdb_repository = CosmosdbRepository(
    connection_string = cosmosdb_connection_string,
    database_name = cosmosdb_database_name,
    container_name = cosmosdb_container_name
)
blob_storage_repository = BlobStorageRepository(connection_string = blob_connection_string,container_name = blob_container_name)
vinculador_service = VinculadorService(cosmosdb_repository, blob_storage_repository)


logging_service = LoggingService(audits_api_url_base)


@app.route(route="analysis", methods=["POST"])
def execute_analyzer(req: func.HttpRequest) -> func.HttpResponse:
    user = req.headers.get("user")
    analisys = req.get_json()
    log = {
            "user": user,
            "action": "CREATE",
            "api": f"{API_URL_BASE}/analysis",
            "request": json.dumps(analisys)
        }
    try:
        blob_storage_repository = BlobStorageRepository(connection_string = blob_connection_string,container_name = blob_container_name_for_trigger)
        vinculador_service = VinculadorService(cosmosdb_repository, blob_storage_repository)
        response = vinculador_service.process(analisys)
        log["response"] = json.dumps(response)
        log["isSuccess"] = True
        logging_service.save_log(log) 
        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.exception(f"[execute_analyzer] - Error: {str(e)}")
        log["isSuccess"] = False
        log["error"] = str(e)
        logging_service.save_log(log)        
        return func.HttpResponse(json.dumps({"error": str(e)}), mimetype="application/json", status_code=500)

@app.route(route="analysis", methods=["GET"])
def get_analysis(req: func.HttpRequest) -> func.HttpResponse:
    try:
        params = PaginationParamsDTO.validate_request(req)

        response = vinculador_service.get_all_analysis(params)

        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.exception(f"[get_analysis] - Error: {str(e)}")
        return func.HttpResponse(json.dumps({"error": str(e)}), mimetype="application/json", status_code=500)
    
@app.route(route="analysis/{id}", methods=["GET"])
def get_analysis_by_id(req: func.HttpRequest) -> func.HttpResponse:
    try:
        id = req.route_params.get("id")
        if not id:
            return func.HttpResponse("El parámetro 'id' es requerido", status_code=400)

        response = vinculador_service.get_one_analysis(id)

        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.exception(f"[get_analysis_by_id] - Error: {str(e)}")
        return func.HttpResponse(json.dumps({"error": str(e)}), mimetype="application/json", status_code=500)    

  
@app.route(route="analysis/{id}", methods=["PUT"])
def update_analysis_by_id(req: func.HttpRequest) -> func.HttpResponse:
    user = req.headers.get("user")
    id = req.route_params.get("id")
    analisys = req.get_json()
    log = {
            "user": user,
            "action": "UPDATE",
            "api": f"{API_URL_BASE}/analysis/{id}",
            "request": json.dumps(analisys)
        }
    try:

        if not id:
            return func.HttpResponse("El parámetro 'id' es requerido", status_code=400)

        if not analisys:
            return func.HttpResponse("El parámetro 'analisys' es requerido", status_code=400)
        
        response = vinculador_service.update_analysis_by_id(id, analisys)
        log["response"] = json.dumps(response)
        log["isSuccess"] = True
        logging_service.save_log(log) 
        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.exception(f"[update_analysis_by_id] - Error: {str(e)}")
        log["isSuccess"] = False
        log["error"] = str(e)
        logging_service.save_log(log)        
        return func.HttpResponse(json.dumps({"error": str(e)}), mimetype="application/json", status_code=500)    

@app.route(route="files", methods=["GET"])
def get_folders_documents(req: func.HttpRequest) -> func.HttpResponse:
    try:

        response = vinculador_service.get_folders_documents()

        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.error(f"[get_folders_documents] - Error: {str(e)}")
        return func.HttpResponse(json.dumps({"error": str(e)}), mimetype="application/json", status_code=500)


@app.route(route="upload-files", methods=["POST"])
def upload_files(req: func.HttpRequest) -> func.HttpResponse:
    user = req.headers.get("user")
    log = {
            "user": user,
            "action": "UPLOAD",
            "api": f"{API_URL_BASE}/upload-files",
            "request": json.dumps(req.form)
        }    
    try:

        if 'files' not in req.files:
            return func.HttpResponse(json.dumps({"error": "No file part in the req"}), mimetype="application/json", status_code=400)

        files = req.files.getlist('files')
        directory_name = req.form.get('directoryName')
        subdirectory_name = req.form.get('subdirectoryName')
        if not files:
            logging.exception("No files provided")
            return func.HttpResponse(json.dumps({"error": "No files provided"}), mimetype="application/json", status_code=400)

        if not subdirectory_name:
            logging.exception("No subdirectory_name provided")
            return func.HttpResponse(json.dumps({"error": "No subdirectory_name provided"}), mimetype="application/json", status_code=400)
        
        response = vinculador_service.upload_files(files,directory_name,subdirectory_name)

        log["response"] = json.dumps(response)
        log["isSuccess"] = True
        logging_service.save_log(log) 
        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.exception(f"[upload_files] - Error: {str(e)}")
        log["isSuccess"] = False
        log["error"] = str(e)
        logging_service.save_log(log)        
        return func.HttpResponse(json.dumps({"error": str(e)}), mimetype="application/json", status_code=500)

@app.route(route="delete-file", methods=["DELETE"])
def delete_file(req: func.HttpRequest) -> func.HttpResponse:
    user = req.headers.get("user")
    request = req.get_json()
    log = {
            "user": user,
            "action": "DELETE",
            "api": f"{API_URL_BASE}/delete-file",
            "request": json.dumps(request)
        }       
    try:

        file_path = request.get("filePath")
        response = vinculador_service.delete_file(file_path)

        log["response"] = json.dumps(response)
        log["isSuccess"] = True
        logging_service.save_log(log) 
        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.exception(f"[delete_file] - Error: {str(e)}")
        log["isSuccess"] = False
        log["error"] = str(e)
        logging_service.save_log(log)        
        return func.HttpResponse(json.dumps({"error": str(e)}), mimetype="application/json", status_code=500)
    

@app.blob_trigger(arg_name="blob", path="poc-vinculador-files/{folders}/{subfolders}/{blobname}",
                  connection="BLOB_STORAGE_CONNECTION_STRING") 
def document_intelligence_processing(blob: func.InputStream):
    log = {
            "user": "SYSTEM",
            "action": "EXTRACT_TEXT",
            "api": "BLOB_TRIGGER",
            "request": blob.name
        }   
    try:
        recognizer_repository = RecognizerRepository(recognizer_endpoint=form_recognizer_endpoint, recognizer_key=form_recognizer_key)
        blob_storage_repository = BlobStorageRepository(connection_string = blob_connection_string,container_name = blob_container_name_from_document_intelligence)
        document_intelligence_service = DocumentIntelligenceService(recognizer_repository, blob_storage_repository)

        document_intelligence_service.document_intelligence_processing(blob, container_name= blob_container_name)
        log["isSuccess"] = True
        logging_service.save_log(log)    
    except Exception as e:
        logging.exception(f"Error during document processing: {e}")
        log["isSuccess"] = False
        log["error"] = str(e)
        logging_service.save_log(log)



@app.timer_trigger(arg_name="timer",schedule = cron_job_schedule,run_on_startup=False, use_monitor=False)
def reminder_notification(timer: func.TimerRequest) -> None:
    log = {
        "user": "SYSTEM",
        "action": "REMINDER_NOTIFICATION",
        "api": "CRON_JOB",
    }
    try:
        notifications_service = NotificationsService(notifications_api_url_base)
        reminder_service = ReminderService(notifications_service, cosmosdb_repository)
        response = reminder_service.send_notification()
        log["response"] = json.dumps(response)        
        log["isSuccess"] = True
        logging_service.save_log(log)
    except Exception as e:
        logging.exception(f"[reminder_notification] - Error: {e}")
        log["isSuccess"] = False
        log["error"] = str(e)
        logging_service.save_log(log)        