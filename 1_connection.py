from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database():
    """
    Creates a connection to MongoDB and returns the database instance.
    You can use either:
    1. Local MongoDB instance
    2. MongoDB Atlas (cloud) instance
    """
    
    # Option 1: Connect to local MongoDB
    # client = MongoClient('mongodb://localhost:27017/')
    
    # Option 2: Connect to MongoDB Atlas
    # Replace with your MongoDB Atlas connection string
    # Format: mongodb+srv://<username>:<password>@<cluster-url>/
    connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    
    try:
        # Create a new client and connect to the server
        client = MongoClient(connection_string, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        
        # Get the database instance
        # If the database doesn't exist, MongoDB will create it
        db = client['sample_db']
        return db
    
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

if __name__ == "__main__":
    # Test the connection
    db = get_database()
    print(f"Connected to database: {db.name}")
    
"""
Documentation References:
- MongoDB Connection Guide: https://www.mongodb.com/docs/drivers/python/current/usage-examples/connect/
- Connection String Format: https://www.mongodb.com/docs/manual/reference/connection-string/
- MongoDB Atlas Connection: https://www.mongodb.com/docs/atlas/driver-connection/
"""