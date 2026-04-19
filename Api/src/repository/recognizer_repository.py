import logging
from azure.core.credentials import AzureKeyCredential
from src.interfaces.recognizer_interface import RecognizerInterface
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

class RecognizerRepository(RecognizerInterface):
    def __init__(self,recognizer_endpoint: str, recognizer_key:str)->None:
            self.document_analysis_client = DocumentIntelligenceClient(
            endpoint=recognizer_endpoint,
            credential=AzureKeyCredential(recognizer_key),
        )

    def begin_analyze_document(self, file_stream, file_name):
        try:
            extension = file_name.split('.')[-1].lower()

            if extension not in ['pdf', 'pptx', 'docx']:
                raise ValueError(f"Unsupported file extension: {extension}")

            poller = self.document_analysis_client.begin_analyze_document(
                "prebuilt-layout", AnalyzeDocumentRequest(bytes_source=file_stream)
                )
            result: AnalyzeResult = poller.result()

            logging.exception(f"[RecognizerRapository - begin_analyze_document] -  Processing document {file_name} successful!")
            return result
            
        except Exception as e:
            logging.exception(f"[RecognizerRapository - begin_analyze_document] - Error: Processing document {file_name}: {e}")
            raise