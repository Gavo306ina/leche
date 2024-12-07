
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://nose:nose@nose.87wxfml.mongodb.net/?retryWrites=true&w=majority&appName=nose"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client['nose']
prod_col = db['leche']
"""
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)"""