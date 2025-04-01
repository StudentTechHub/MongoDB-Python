from connection import get_database
from pymongo import ASCENDING, DESCENDING, TEXT

# Get database instance
db = get_database()
users = db.users
products = db.products

def index_operations():
    """Demonstrating MongoDB index operations"""
    
    # Create a single field index
    users.create_index([("email", ASCENDING)], unique=True)
    print("Created unique index on email field")
    
    # Create a compound index
    users.create_index([
        ("age", ASCENDING),
        ("created_at", DESCENDING)
    ])
    print("Created compound index on age and created_at fields")
    
    # Create a text index for text search
    users.create_index([("description", TEXT)])
    print("Created text index on description field")
    
    # List all indexes on a collection
    print("\nCurrent indexes on users collection:")
    for index in users.list_indexes():
        print(index)

def basic_aggregation():
    """Demonstrating basic aggregation operations"""
    
    # Calculate average age of users
    pipeline = [
        {
            "$group": {
                "_id": None,
                "avgAge": {"$avg": "$age"},
                "totalUsers": {"$sum": 1}
            }
        }
    ]
    result = list(users.aggregate(pipeline))
    print("\nAge statistics:", result)
    
    # Group users by country and count
    pipeline = [
        {
            "$group": {
                "_id": "$address.country",
                "userCount": {"$sum": 1}
            }
        },
        {
            "$sort": {"userCount": -1}
        }
    ]
    result = list(users.aggregate(pipeline))
    print("\nUsers by country:", result)

def advanced_aggregation():
    """Demonstrating advanced aggregation operations"""
    
    # Complex pipeline with multiple stages
    pipeline = [
        # Match stage - filter documents
        {
            "$match": {
                "age": {"$gte": 18}
            }
        },
        # Group stage - group and calculate
        {
            "$group": {
                "_id": {
                    "country": "$address.country",
                    "premium": "$premium_member"
                },
                "count": {"$sum": 1},
                "avgAge": {"$avg": "$age"}
            }
        },
        # Sort stage
        {
            "$sort": {"count": -1}
        },
        # Project stage - reshape output
        {
            "$project": {
                "_id": 0,
                "country": "$_id.country",
                "premium_status": "$_id.premium",
                "user_count": "$count",
                "average_age": {"$round": ["$avgAge", 1]}
            }
        }
    ]
    
    result = list(users.aggregate(pipeline))
    print("\nDetailed user statistics:", result)

def lookup_example():
    """Demonstrating $lookup operation (like JOIN in SQL)"""
    
    # Find all orders and include user details
    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_details"
            }
        },
        {
            "$unwind": "$user_details"
        },
        {
            "$project": {
                "order_id": 1,
                "amount": 1,
                "user_name": "$user_details.name",
                "user_email": "$user_details.email"
            }
        }
    ]
    
    result = list(db.orders.aggregate(pipeline))
    print("\nOrders with user details:", result)

if __name__ == "__main__":
    print("=== Index Operations ===")
    index_operations()
    
    print("\n=== Basic Aggregation ===")
    basic_aggregation()
    
    print("\n=== Advanced Aggregation ===")
    advanced_aggregation()
    
    print("\n=== Lookup Example ===")
    lookup_example()

"""
Documentation References:
- Indexes: https://www.mongodb.com/docs/manual/indexes/
- Aggregation Pipeline: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
- Aggregation Operators: https://www.mongodb.com/docs/manual/reference/operator/aggregation/
- $lookup: https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/
"""