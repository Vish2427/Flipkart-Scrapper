import pymongo
import pandas as pd
import json




class MongoDBmanagement:

    def __init__(self, username, password):
        """This function sets URL"""
        try:
            self.username = username
            self.password = password
            self.url = "mongodb+srv://{}:{}@practice.lgq8z4v.mongodb.net/?retryWrites = true&w = majority".format(self.username, self.password)
        except Exception as e:
            raise Exception(f"(__init__):Something wrong with initiation\n" + str(e))

    def MongoBDClientObject(self):
        """This function creates client object for connection purpose"""
        try:
            mongo_client = pymongo.MongoClient(self.url)
            return mongo_client
        except Exception as e:
            raise Exception(f"(MongoBDClientObject): Something went wrong on creation with client object\n" + str(e))

    def MongoDBclose(self, mongo_client):
        """This function is to close mongodb"""
        try:
            mongo_client.close()
        except Exception as e:
            raise Exception(f"(MongoDBclose): Something went wrong in closing mongodb\n" + str(e))

    def isDataBasePresent(self, db_name):
        """This function check if database is present or not"""
        try:
            mongo_client = self.MongoBDClientObject()
            if db_name in mongo_client.list_database_names():
                mongo_client.close()
                return True
            else:
                mongo_client.close()
                return False
        except Exception as e:
            raise Exception(f"(sDataBasePresent):Failed to check if data base is present or not \n" + str(e))

    def createdatabase(self, db_name):
        """This function creates database"""
        try:
            mongo_client = self.MongoBDClientObject()
            database = mongo_client[db_name]
            mongo_client.close()
            return database
        except Exception as e:
            raise Exception(f"(createdatabase): Failed to create database \n" + str(e))

    def dropdatabase(self, db_name):
        """This function delete database"""
        try:
            mongo_client = self.MongoBDClientObject()
            if db_name in mongo_client.list_database_name():
                mongo_client.drop_database(db_name)
                mongo_client.close()
                return True
        except Exception as e:
            raise Exception(f"(dropdatabase): Failed to delete database {db_name}\n" + str(e))

    def getdatabase(self, db_name):
        """Returns database"""
        try:
            mongo_client = self.MongoBDClientObject()
            mongo_client.close()
            return mongo_client[db_name]
        except Exception as e:
            raise Exception(f"(getdatabase): Failed to find database \n" + str(e))

    def getcollection(self, collection_name, db_name):
        """Returns collection"""
        try:
            database = self.getdatabase(db_name)
            return database[collection_name]
        except Exception as e:
            raise Exception(f"(getcollection): Failed to find collection\n" + str(e))

    def iscollectionpresent(self, collection_name, db_name):
        """Check if collection is present"""
        try:
            database_status = self.isDataBasePresent(db_name=db_name)
            if database_status:
                database = self.getdatabase(db_name=db_name)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(f"(iscollectionpresent): Failed to check collection \n" + str(e))

    def cratecollection(self, collection_name, db_name):
        """Creates collection"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                database = self.getdatabase(db_name)
                collection = database[collection_name]
                return collection
        except Exception as e:
            raise Exception(f"(cratecollection): Failed to create collection \n"+str(e))

    def dropcollection(self, collection_name, db_name):
        """Drops collection"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                database = self.getdatabase(db_name=db_name)
                database.drop()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(dropcollection): Failed to drop the collection \n"+str(e))

    def insertRecord(self, collection_name, db_name, record):
        """Insert Record into DB"""
        try:

            collection = self.getcollection(collection_name=collection_name, db_name=db_name)
            collection.insert_one(record)
            sum  = 0
            return f"row inserted"
        except Exception as e:
            raise Exception(f"(innsertRecord): Inserting record failed \n"+str(e))


    def insertRecords(self, collection_name, db_name, record):
        """Insert many record into DB"""
        try:
            collection = self.getcollection(collection_name=collection_name, db_name=db_name)
            record = list(record.values())
            collection.insert_many(record)
            sum  = 0
            return f"row inserted"
        except Exception as e:
            raise Exception(f"(innsertRecord): Inserting record failed \n"+str(e))

    def findfirstrecord(self, collection_name, db_name, query = None):
        """This function gives first record"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                collection = self.getcollection(collection_name=collection_name, db_name=db_name)
                firstrecord = collection.find_one(query)
                return firstrecord
        except Exception as e:
            raise Exception(f"(findfirstrecord): Didn't found record\n"+str(e))

    def findallRecords(self, collection_name, db_name):
        """This function returns all record"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                collection = self.getcollection(collection_name=collection_name, db_name=db_name)
                allrecord = collection.find()
                return allrecord
        except Exception as e:
            raise Exception(f"(findallRecords): Didn't found record\n"+str(e))

    def findonequary(self, collection_name, db_name, query):
        """Thus function return the query"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                collection = self.getcollection(collection_name=collection_name, db_name=db_name)
                quary = collection.find(query)
                return quary
        except Exception as e:
            raise Exception(f"(findallRecords): Didn't found record for given query\n" + str(e))

    def updateonerecord(self, collection_name, db_name, query):
        """Updates one record"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                collection = self.getcollection(collection_name=collection_name, db_name=db_name)
                previous_record = self.findallRecords(collection_name=collection_name, db_name=db_name)
                new_record = query
                updated_record = collection.update_one(previous_record, new_record)
                return updated_record
        except Exception as e:
            raise Exception(f"(updateonerecord): Failed to update the record \n"+str(e))

    def updatemanyrecords(self, collection_name, db_name, query):
        """Updates many record"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                collection = self.getcollection(collection_name=collection_name, db_name=db_name)
                previous_record = self.findallRecords(collection_name=collection_name, db_name=db_name)
                new_record = query
                updated_record = collection.update_many(previous_record, new_record)
                return updated_record
        except Exception as e:
            raise Exception(f"(updatemanyrecord): Failed to update the record \n"+str(e))

    def deleteonerecord(self, collection_name, db_name, query):
        """Delete one record"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                collection = self.getcollection(collection_name=collection_name, db_name=db_name)
                collection.delete_one(query)
                return "1 row deleted"
        except Exception as e:
            raise Exception(f"(deleteonerecord): Failed to delete record \n"+str(e))

    def deletemanyrecord(self, collection_name, db_name, query):
        """Delete one record"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                collection = self.getcollection(collection_name=collection_name, db_name=db_name)
                collection.delete_many(query)
                return "1 row deleted"
        except Exception as e:
            raise Exception(f"(deletemanyrecord): Failed to delete record \n"+str(e))

    def getDataframeofCollection(self, collection_name, db_name):
        """Makes Dataframe of the given collection"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            if collection_status:
                record = self.findallRecords(collection_name=collection_name, db_name=db_name)
                dataframe = pd.DataFrame(record)
                return dataframe
        except Exception as e:
            raise Exception(f"(getDataframeofCollection): Failed to get dataframe from collection and database \n"+str(e))

    def SaveDataframeintoCollection(self, collection_name, db_name, dataframe):
        """Saves record in collection"""
        try:
            collection_status = self.iscollectionpresent(collection_name=collection_name, db_name=db_name)
            dataframe_dict = json.loads(dataframe.T.to_json())
            if collection_status:
                self.insertRecords(collection_name=collection_name, db_name=db_name, record = dataframe_dict)
                return "inserted"
        except Exception as e:
            raise Exception(f"(SaveDataframeintoCollection): Failed to save dataframe into collection \n"+str(e))

    def getResulttoDisplayonBrowser(self, collection_name, db_name):
        """Gets Record to display"""
        try:
            record = self.findallRecords(collection_name=collection_name, db_name=db_name)
            result = [i for i in record]
            return result
        except Exception as e:
            raise Exception(f"(getResulttoDisplayonBrowser): Something went wrong in displaying the result \n"+str(e))





