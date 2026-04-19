import logging
from azure.cosmos import CosmosClient
from src.models.search_model import Search
from src.interfaces.cosmosdb_interface import CosmosdbInterface

class CosmosdbRepository(CosmosdbInterface):
    def __init__(self, connection_string, database_name, container_name):
        self.client = CosmosClient.from_connection_string(connection_string)
        self.container = self.client.get_database_client(database_name).get_container_client(container_name)        

    def save(self, search: Search):
        try:
            item = {
            "id": search.id,
            "request":{
            "numberOperation": search.numberOperation,
            },
            "response": [],
            "status": search.status,
            "isActive": search.isActive,
            "createdAt": search.createdAt,
            "updatedAt": search.updatedAt,
            }
            response = self.container.create_item(item)
            logging.info("[CosmosdbRepository - save] - cosmosDB_response: ", response)
            return response
        except Exception as e:
            logging.error(f"Error al ejecutar cosmosdb: {str(e)}")
            raise ValueError(f"[CosmosdbRepository - save] - Error: {str(e)}")

    def get_all(self, start_date, end_date, skip, limit):
        try:
            query = f"SELECT * FROM analysis WHERE analysis.isActive = true"
            if start_date:
                query += f" AND analysis.createdAt >= {start_date}"

            if end_date:
                query += f" AND analysis.createdAt <= {end_date}"

            query += f" ORDER BY analysis.createdAt DESC OFFSET {skip} LIMIT {limit}"
            logging.info(f"QUERY: {query}")
            items = list(self.container.query_items(query=query,enable_cross_partition_query=True))
            return items
        except Exception as e:
            logging.error(f"[CosmosdbRepository - get_all] - Error: {str(e)}")
            raise ValueError(f"[CosmosdbRepository - get_all] - Error: {str(e)}")
    
    def get_one(self, id: str):
        logging.info(f"id: {id}")
        try:
            items = self.container.read_item(item=id,partition_key=id)
            return items
        except Exception as e:
            logging.error(f"[CosmosdbRepository - get_one] - Error: {str(e)}")
            raise ValueError(f"[CosmosdbRepository - get_one] - Error: {str(e)}")

    def update(self, id:str, search: Search):
        try:
            response = self.container.replace_item(item=id, body=search)
            logging.info("[CosmosdbRepository - update] - cosmosDB_response: ", response)
            return response
        except Exception as e:
            logging.error(f"Error al ejecutar cosmosdb: {str(e)}")
            raise ValueError(f"[CosmosdbRepository - update] - Error: {str(e)}")
        
    def active_count(self, start_date, end_date):
        try:
            query = "SELECT VALUE COUNT(1) FROM analysis WHERE analysis.isActive = true"
            if start_date:
                query += f" AND analysis.createdAt >= {start_date}"

            if end_date:
                query += f" AND analysis.createdAt <= {end_date}"
            logging.info(f"QUERY: {query}")
            items = list(self.container.query_items(query=query,enable_cross_partition_query=True))
            count = items[0]
            logging.info(f"count: {count}")
            return count
        except Exception as e:
            logging.error(f"[CosmosdbSearchRepository - active_count] - Error: {str(e)}")
            raise ValueError(f"[CosmosdbRepository - active_count] - Error: {str(e)}")

    def get_last_finished_row(self):
        try:
            query = "SELECT * FROM analysis WHERE analysis.isActive = true AND analysis.status = 'FINISHED' ORDER BY analysis.createdAt DESC OFFSET 0 LIMIT 1"
            items = list(self.container.query_items(query=query,enable_cross_partition_query=True))
            return items[0]
        except Exception as e:
            logging.error(f"[CosmosdbSearchRepository - get_last_finished_row] - Error: {str(e)}")
            raise ValueError(f"[CosmosdbRepository - get_last_finished_row] - Error: {str(e)}")