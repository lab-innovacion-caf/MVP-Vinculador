from abc import ABC, abstractmethod

class RecognizerInterface(ABC):
    @abstractmethod
    def begin_analyze_document(self,file_stream, file_name):
        pass
