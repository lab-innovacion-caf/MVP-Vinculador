from abc import ABC, abstractmethod
from src.models.search_model import Search

class CosmosdbInterface(ABC):
    @abstractmethod
    def save(self, search: Search):
        pass

    @abstractmethod
    def get_all(self, start_date: int, end_date: int, skip: int, limit: int):
        pass

    @abstractmethod
    def get_one(self, id: str):
        pass

    @abstractmethod
    def update(self, id:str, search: Search):
        pass

    @abstractmethod
    def active_count(self, start_date, end_date):
        pass

    @abstractmethod
    def get_last_finished_row(self):
        pass