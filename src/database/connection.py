"""
MongoDB Connection Manager
This module handles the connection to MongoDB, supporting both local and Atlas connections.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MongoDBConnection:
    _instance = None
    _client = None
    
    @classmethod
    def get_instance(cls):
        """Singleton pattern to ensure single database connection"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Initialize MongoDB connection using environment variables"""
        # Priority: Atlas URI > Local URI
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
        self._client = MongoClient(mongodb_uri)
    
    def get_database(self, db_name='student_tech_hub'):
        """
        Get database instance
        Args:
            db_name (str): Name of the database to connect to
        Returns:
            Database: MongoDB database instance
        """
        return self._client[db_name]
    
    def close_connection(self):
        """Close the MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            MongoDBConnection._instance = None

# Usage example:
# db = MongoDBConnection.get_instance().get_database()