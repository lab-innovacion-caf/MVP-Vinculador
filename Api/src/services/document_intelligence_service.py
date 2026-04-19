import logging
from src.interfaces.recognizer_interface import RecognizerInterface
from src.interfaces.blob_storage_interface import BlobStorageInterface
from src.utils.extract_formart_recognizer import extract_and_format_content_document

class DocumentIntelligenceService:
    def __init__(self, recognizer_repository: RecognizerInterface, blob_storage_repository: BlobStorageInterface) -> None:
        self.recognizer_repository = recognizer_repository
        self.blob_storage_repository = blob_storage_repository

    def document_intelligence_processing(self, blob, container_name: str):
        try:

            path_parts = blob.name.split("/")
            if len(path_parts) < 4:
                raise ValueError(f"Blob path has insufficient segments: {blob.name}")
            
            folder, subfolder, file_name = path_parts[1], path_parts[2], path_parts[3]

            logging.info(f"Folder: {folder}, Subfolder: {subfolder}, File Name: {file_name}")

            path = f"{folder}/{subfolder}/{file_name}"
            blob_data = self.blob_storage_repository.download_blob(file_path=path,container_name=container_name)
            get_content_document_from_recognizer = self.recognizer_repository.begin_analyze_document(file_stream=blob_data, file_name=file_name)
            
            if not get_content_document_from_recognizer:
                raise ValueError(f"Document intelligence response is empty")

            prepare_content_document = get_content_document_from_recognizer.content
            
            blob_path = f"{folder}/{subfolder}/{'.'.join(file_name.split('.')[:-1])}.txt"
            self.blob_storage_repository.upload_blob(file_content=prepare_content_document,file_name=blob_path)

            logging.info(f"[DocumentIntelligenceService - document_intelligence_processing] - Processed file successfully stored at: {blob_path}")

        except Exception as e:
            logging.error(f"[DocumentIntelligenceService - document_intelligence_processing] - Error: During document processing: {e}")