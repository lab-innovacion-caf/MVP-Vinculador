import uuid
import json
import logging
from src.utils import get_epoch_time
from src.interfaces.cosmosdb_interface import CosmosdbInterface
from src.models.search_model import Search
from src.interfaces.blob_storage_interface import BlobStorageInterface

TIME_ZONE = "America/Bogota"

class VinculadorService:
    def __init__(self, cosmosdb_repository: CosmosdbInterface, blob_storage_repository: BlobStorageInterface):
        self.cosmosdb_repository = cosmosdb_repository
        self.blob_storage_repository = blob_storage_repository

    def process(self, analisys):

        epoch_time = get_epoch_time.get_epoch_time(TIME_ZONE)
        uuid_value = uuid.uuid4()

        search = Search(id=str(uuid_value),isActive=True,createdAt=epoch_time,updatedAt=epoch_time,status="PROCESSING",numberOperation=analisys["numberOperation"])

        save_response = self.cosmosdb_repository.save(search)

        data = {
            "id": str(uuid_value)
        }
        file_name = str(uuid_value)+".json"
        self.blob_storage_repository.upload_blob(file_content=json.dumps(data,indent=4),file_name=file_name)

        return save_response

    def get_all_analysis(self, params):
        try:
            total = self.cosmosdb_repository.active_count(params.start_date, params.end_date)
            skip = (params.page - 1) * params.limit
            pages = -(-total // params.limit)

            data = self.cosmosdb_repository.get_all(
                start_date = params.start_date,
                end_date = params.end_date,
                skip = skip,
                limit = params.limit
                )
            
            response = {
                "total": total,
                "page": params.page,
                "limit": params.limit,
                "pages": pages,
                "data": data
            }
            return response
        except Exception as e:
            logging.error(f"[VinculadorService - get_all_analysis] - Error: {str(e)}")
            raise     

    def get_one_analysis(self, id: str):
        data = self.cosmosdb_repository.get_one(id)

        if len(data["response"]) == 0:
            return data
        
        data["response"] = sorted(data["response"], key=lambda x: x["compatibilityPorcentage"], reverse=True)
        return data
    
    def update_analysis_by_id(self, id: str, analysis):
        analysis["updatedAt"] = get_epoch_time.get_epoch_time(TIME_ZONE)
        return self.cosmosdb_repository.update(id, analysis)
    
    def get_documents(self, paths):
        folder_structure = {}

        for path in paths:
            parts = path.split("/")

            if parts[0] not in folder_structure:
                folder_structure[parts[0]]={}
            
            if parts[1] not in folder_structure[parts[0]]:
                folder_structure[parts[0]][parts[1]] = []

            folder_structure[parts[0]][parts[1]].append(parts[2])
        
        return folder_structure

    def get_folders_documents(self):
        blobs =  self.blob_storage_repository.list_blobs()
        # folders_path = []
        # logging.warning(f"folders_path: {folders_path}")
        # for blob in blobs:
        #     blob_name = blob.name
        #     folders_path.append(blob_name)

        folder_structure = self.get_documents(blobs)
        logging.warning(f"folder_structure: {folder_structure}")
        return folder_structure

    def upload_files(self, files, directory_name,subdirectory_name):
        uploaded_files = []
        path_base = f"{directory_name}/{subdirectory_name}"
        for file in files:
            try:
                file_format = file.filename
                path_file = f"{path_base}/{file_format}".replace("\n", "")
                self.blob_storage_repository.upload_blob(file.stream.read(),path_file)
                uploaded_files.append(path_file)
                logging.info(f"File {path_file} uploaded successfully.")
            except Exception as e:
                logging.error(f"Error uploading file {path_file}: {e}")
        return uploaded_files

    def delete_file(self, file_path):
        response = {
            "isDeleted": False,
            "pathFile": file_path
        }
        try:
            self.blob_storage_repository.delete_blob(file_path)
            response["isDeleted"] = True
            return response
        except Exception as e:
            logging.error(f"Error deleting file {file_path}: {e}")
            raise ValueError(e)