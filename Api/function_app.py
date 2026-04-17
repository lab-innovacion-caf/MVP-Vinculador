import logging
from src.services.notifications_service import NotificationsService
from src.interfaces.cosmosdb_interface import CosmosdbInterface
from src.utils.get_epoch_time import format_epoch_time

class ReminderService:
    def __init__(self, notifications_service: NotificationsService, cosmosdb_repository: CosmosdbInterface):
        self.notifications_service = notifications_service
        self.cosmosdb_repository = cosmosdb_repository
    
    def send_notification(self):
        try:
            last_row = self.cosmosdb_repository.get_last_finished_row()
            analysis_for_review = []
            for row in last_row['response']:
                if row['isQualified'] and row['isApprovedByUser'] == None:
                    analysis_for_review.append({
                                    "Proyecto": row['project'],
                                    "Aliado": row['ally'],
                                    "Cantidad de compatibilidad": row['compatibilityCount']
                    })
            
            if len(analysis_for_review) == 0:
                return
            
            data = {
                    "idProject": "VINCULADOR_DMAF",
                    "typeNotification": "EMIAL",
                    "notification": "WEEKLY_REMINDER",
                    "data": [
                        {
                            "label":"{{id}}",
                            "value": last_row['id']
                        },
                                    {
                            "label":"{{createdAt}}",
                            "value": format_epoch_time(last_row['createdAt'], "America/Bogota")
                        }
                    ],
                    "table": analysis_for_review
                }
            self.notifications_service.send(data=data)
            logging.info("Reminder sended success!")
            analysis_text = "\n".join([
            f"Proyecto: {item['Proyecto']}, Aliado: {item['Aliado']}, Cantidad de compatibilidad: {item['Cantidad de compatibilidad']}"
            for item in analysis_for_review
            ])
            return analysis_text
        except Exception as e:
            raise e
