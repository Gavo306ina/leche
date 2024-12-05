from pymongo import MongoClient

def get_db_handle(db_name, host, port, username, password):
    client = MongoClient(
    'mongodb+srv://nose:nose@nose.87wxfml.mongodb.net/?retryWrites=true&w=majority&appName=nose')
    db_handle = client['db_name']
    return db_handle, client

 