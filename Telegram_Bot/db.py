from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import ordermodel 
import usermodel 
import chatmodel 
import copy
import datetime
# Create a new client and connect to the server

class PBJ_DB:

    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host
        self.uri = "mongodb+srv://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)
        self.client = self.connectToDb(self)

    def connectToDb(self, server_api=ServerApi('1'), tls=True):
        try:
            client = MongoClient(self.uri, server_api=ServerApi('1'), tls=True)
            return client
        except Exception as e:
            print(e)
            return None

    def insertUnpaidOrder(self, obj:ordermodel.order):
        try:
            self.client['PBJ_Stand']['UnpaidOrders'].insert_one(obj)
            return True
        except Exception as e:
            print(e)
            return False

    def initalizeDB(self):
        try:
            item = copy.deepcopy(ordermodel.order)
            self.client['PBJ_Stand']['UnpaidOrders'].insert_one(item, bypass_document_validation=True)
            item = copy.deepcopy(usermodel.user)
            self.client['PBJ_Stand']['Users'].insert_one(item, bypass_document_validation=True)
            item = copy.deepcopy(chatmodel.chat)
            self.client['PBJ_Stand']['Chats'].insert_one(item, bypass_document_validation=True)
            return True
        except Exception as e:
            print(e)
            return False

    def upsertUser(self, obj:usermodel.user):
        try:
            self.client['PBJ_Stand']['Users'].find_one_and_update({'chatId': obj['chatId']}, {'$set':obj}, upsert=True)
            return True
        except Exception as e:
            print(e)
            return False
        
    def upsertChat(self, obj:usermodel.user):
        try:
            self.client['PBJ_Stand']['Chats'].find_one_and_update({'chatId': obj['chatId']}, {'$set':obj}, upsert=True)
            return True
        except Exception as e:
            print(e)
            return False

    def findUser(self, obj:usermodel.user):
        try:
            return self.client['PBJ_Stand']['Users'].find_one({"chatId": obj['chatId']})
        except Exception as e:
            print(e)
            return False

    def findOrder(self, orderId):
        try:
            self.client['PBJ_Stand']['UnpaidOrders'].find({"orderId":orderId})
        except Exception as e:
            print(e)
            return False   
        
    def logActivity(self, time: datetime, activity: dict):
        try:
            date = time.strftime("%x") 
            document = self.client['PBJ_Stand']['ActivityLog'].find_one({"date": date})
            date = {'date': date}
            if (document is None):
                self.client['PBJ_Stand']['ActivityLog'].insert_one(date)
                document = self.client['PBJ_Stand']['ActivityLog'].find_one({"date": date['date']})
            document['Activity'] = activity
            self.client['PBJ_Stand']['ActivityLog'].find_one_and_update({'date': date['date']}, {'$set':document}, upsert=True)
        except :
            return False

    def getLogActivity(self, time: datetime):
        try:
            date = time.strftime("%x")
            document = self.client['PBJ_Stand']['ActivityLog'].find_one({"date": date})
            if (document is None):
                return dict()
            else:
                return document['Activity']
        except:
            return False


