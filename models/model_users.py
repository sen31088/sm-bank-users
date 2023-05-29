from config import DB_Config

db_name = DB_Config.db_name

class Userlogin:
    collection = DB_Config.col_userlogin

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls, data):
        return dict(cls.collection.find_one(data))
    
    @classmethod
    def find_pending_users(cls):
       try:
        #data = ({'Activation_status': status}, {"userid","Name","email","Activation_status"})
        query = {'$or': [{'Activation_status': 'Pending'}, {'Activation_status': 'Suspended'}]}
        required_key = {"userid","Name","email"}
        output = cls.collection.find(query, required_key )
        if output:
            return list(output)
        else:
            return 0
       except Exception as e:
           return {'error': str(e)}
    
    @classmethod
    def update(cls, userid, status):
        current_user_id = { "userid": userid  }
        updated_user_status = { "$set": { "Activation_status": status } }
        return cls.collection.update_one(current_user_id, updated_user_status)
    
    
    @classmethod
    def get_count(cls, data, limit=None):
        count = cls.collection.count_documents(data, limit=limit)
        return count
    
    @classmethod
    def delete_data(cls, user_id):
        result = cls.collection.delete_one({'userid': user_id})
        return result.deleted_count > 0
    
    @classmethod
    def get_data_userid(cls, data):
        query = {"userid": data}
        output = cls.collection.find_one(query)
        if output:
            return dict(output)
        else:
            return 0

class Userdata:
    collection = DB_Config.col_userdata

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_acc_data(cls, data):
        output = cls.collection.find(data)
        if output:
            return list(output)
        else:
            return 0

        
    @classmethod
    def get_data(cls, data):
        return list(cls.collection.find_one(data))
    
    @classmethod
    def find_and_sort_documents(cls, sort_field='_id', sort_order= -1, limit1=1):
        cursor = cls.collection.find().sort(sort_field, sort_order).limit(limit1)
        return list(cursor)
    
    @classmethod
    def find_pending_users(cls):
       try:
        query = {'$or': [{'Activation_status': 'Pending'}, {'Activation_status': 'Suspended'}]}
        required_key = {"userid","Accno","Accbal", "Activation_status"}
        output = cls.collection.find(query, required_key )
        #output = cls.collection.find({'Activation_status': 'Pending'}, {"userid","Accno","Accbal", "Activation_status"})
        if output:
            return list(output)
        else:
            return 0
       except Exception as e:
           return {'error': str(e)}
    
    @classmethod
    def update(cls, userid, status):
        current_user_id = { "userid": userid  }
        updated_user_status = { "$set": { "Activation_status": status } }
        return cls.collection.update_one(current_user_id, updated_user_status)
    
    @classmethod
    def delete_data(cls, user_id):
        result = cls.collection.delete_one({'userid': user_id})
        return result.deleted_count > 0
    

class Carddetails:
    
    collection = DB_Config.col_carddetails

    @classmethod
    def delete_data(cls, user_id):
        result = cls.collection.delete_one({'userid': user_id})
        return result.deleted_count > 0
    

class Beneficiarydetails:
    collection = DB_Config.col_beneficiarydetails

    @classmethod
    def delete_data(cls, user_id):
        result = cls.collection.delete_many({'userid': user_id})
        return result.deleted_count > 0
    

class Usertranscation():
    def __init__(self):
        self.db = db_name

    def get_data(self, collection_name):
        collection = self.db[collection_name]
        users = collection.find()
        return list(users)

    def save(self, collection_name, data):
        collection = self.db[collection_name]
        return collection.insert_one(data)

     
    def delete_col(self, collection_name):
        collection = self.db[collection_name]
        return collection.drop()


class Adminlogin:
    collection = DB_Config.col_adminlogin

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls, data):
        return dict(cls.collection.find_one(data))
    
    @classmethod
    def get_count(cls, data, limit=None):
        count = cls.collection.count_documents(data, limit=limit)
        return count
    @classmethod
    def find_data(cls, data):
       try:
        output = cls.collection.find_one(data)
        if output:
            return dict(output)
        else:
            return 0
       except Exception as e:
           return {'error': str(e)}


class Admindata:
    collection = DB_Config.col_admindata

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls, data):
        return dict(cls.collection.find_one(data))
    
    @classmethod
    def find_and_sort_documents(cls, sort_field='_id', sort_order= -1, limit1=1):
        cursor = cls.collection.find().sort(sort_field, sort_order).limit(limit1)
        return list(cursor)