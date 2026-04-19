from datetime import datetime
from typing import Optional
import azure.functions as func
from dataclasses import dataclass

@dataclass
class PaginationParamsDTO:
    page: int
    limit: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    @classmethod
    def validate_request(cls, req: func.HttpRequest) -> 'PaginationParamsDTO':
        try:
            page = max(1, int(req.params.get('page', '1')))
            limit = max(1, min(100, int(req.params.get('limit', '10'))))
        except ValueError:
            raise ValueError("Los parámetros 'page' y 'limit' deben ser números enteros")

        start_date = req.params.get('startDate')
        end_date = req.params.get('endDate')

        try:
            start_date = start_date if start_date else None
            end_date = end_date if end_date else None
        except (ValueError, TypeError):
            raise ValueError("Formato de fecha inválido. unixtime")

        return cls(page=page, limit=limit, start_date=start_date, end_date=end_date)