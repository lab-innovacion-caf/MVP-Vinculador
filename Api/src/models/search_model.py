from dataclasses import dataclass

@dataclass
class Search:
    id: str
    isActive: bool
    createdAt: int
    updatedAt: int
    status: str
    numberOperation: str

    
