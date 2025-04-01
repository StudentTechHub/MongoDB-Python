from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from connection import get_database

# Get database instance
db = get_database()

def create_operations():
    """Demonstrating Create operations in MongoDB"""
    
    # Get collection (creates if doesn't exist)
    users = db.users
    
    # insertOne() - Insert a single document
    new_user = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "created_at": datetime.now()
    }
    result = users.insert_one(new_user)
    print(f"Inserted user with id: {result.inserted_id}")
    
    # insertMany() - Insert multiple documents
    multiple_users = [
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "age": 25,
            "created_at": datetime.now()
        },
        {
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "age": 35,
            "created_at": datetime.now()
        }
    ]
    result = users.insert_many(multiple_users)
    print(f"Inserted {len(result.inserted_ids)} users")

def read_operations():
    """Demonstrating Read operations in MongoDB"""
    
    users = db.users
    
    # find_one() - Get a single document
    user = users.find_one({"name": "John Doe"})
    print("Found user:", user)
    
    # find() - Get multiple documents
    # Returns a cursor - iterate to get documents
    all_users = users.find()
    print("\nAll users:")
    for user in all_users:
        print(user)
    
    # Query with conditions
    young_users = users.find({"age": {"$lt": 30}})
    print("\nUsers under 30:")
    for user in young_users:
        print(user)

def update_operations():
    """Demonstrating Update operations in MongoDB"""
    
    users = db.users
    
    # updateOne() - Update first matching document
    result = users.update_one(
        {"name": "John Doe"},  # filter
        {
            "$set": {"age": 31},  # update operator
            "$currentDate": {"last_modified": True}  # automatically set current date
        }
    )
    print(f"Modified {result.modified_count} document")
    
    # updateMany() - Update all matching documents
    result = users.update_many(
        {"age": {"$lt": 30}},  # filter
        {
            "$inc": {"age": 1}  # increment age by 1
        }
    )
    print(f"Modified {result.modified_count} documents")

def delete_operations():
    """Demonstrating Delete operations in MongoDB"""
    
    users = db.users
    
    # deleteOne() - Delete first matching document
    result = users.delete_one({"name": "John Doe"})
    print(f"Deleted {result.deleted_count} document")
    
    # deleteMany() - Delete all matching documents
    result = users.delete_many({"age": {"$gt": 50}})
    print(f"Deleted {result.deleted_count} documents")

if __name__ == "__main__":
    # Execute all operations in sequence
    print("=== Create Operations ===")
    create_operations()
    
    print("\n=== Read Operations ===")
    read_operations()
    
    print("\n=== Update Operations ===")
    update_operations()
    
    print("\n=== Delete Operations ===")
    delete_operations()

"""
Documentation References:
- CRUD Operations: https://www.mongodb.com/docs/manual/crud/
- Update Operators: https://www.mongodb.com/docs/manual/reference/operator/update/
- Query Operators: https://www.mongodb.com/docs/manual/reference/operator/query/
"""