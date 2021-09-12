from datetime import datetime

import pymongo

from config import MONGO_CONN_STRING


# Problem with SSL: https://www.mongodb.com/community/forums/t/ticket-connection-ssl-certificate-verify-failed/91943/11
class MongoDB:
    """Обёртка для работы с Mongo DB Atlas"""
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_CONN_STRING)

    def log_api_req_insert(self, api_link, status):
        db = self.client.logs
        coll = db.api_requests
        coll.insert_one({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'api_link': api_link,
            'status': status
        })
        return status
