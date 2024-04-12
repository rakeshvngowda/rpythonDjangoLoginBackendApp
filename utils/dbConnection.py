from django.db import connection
from utils.CustomError import CustomError

class DbConnection:
    def __init__(self):
        self.cusror = connection.cursor()

    def exceuteRequest(self,query,params=()):
        try:
            self.cusror.callproc(query,params)
            result = self.cusror.fetchall()
            return result
        except Exception as e:
            message = getattr(e,'messages','') or getattr(e,'args','')
            raise CustomError(message[0])
    
    def exceuteView(self,query):
        try:
            self.cusror.execute(query)
            result = self.cusror.fetchall()
            return result
        except Exception as e:
            message = getattr(e,'messages','') or getattr(e,'args','')
            raise CustomError(message[0])

    



