from connection import get_database

# Get database instance
db = get_database()
users = db.users
products = db.products

def comparison_operators():
    """Demonstrating MongoDB comparison operators"""
    
    # Greater than
    result = users.find({"age": {"$gt": 30}})
    print("Users older than 30:", list(result))
    
    # Less than or equal
    result = users.find({"age": {"$lte": 25}})
    print("\nUsers 25 or younger:", list(result))
    
    # Not equal
    result = users.find({"status": {"$ne": "inactive"}})
    print("\nActive users:", list(result))
    
    # In array
    result = users.find({"interests": {"$in": ["reading", "sports"]}})
    print("\nUsers interested in reading or sports:", list(result))

def logical_operators():
    """Demonstrating MongoDB logical operators"""
    
    # AND condition
    result = users.find({
        "$and": [
            {"age": {"$gt": 25}},
            {"interests": "technology"}
        ]
    })
    print("Tech-interested users over 25:", list(result))
    
    # OR condition
    result = users.find({
        "$or": [
            {"age": {"$lt": 20}},
            {"premium_member": True}
        ]
    })
    print("\nYoung or premium users:", list(result))
    
    # NOT condition
    result = users.find({
        "status": {"$not": {"$eq": "banned"}}
    })
    print("\nNon-banned users:", list(result))

def sorting_and_limiting():
    """Demonstrating sorting and limiting results"""
    
    # Sort by age ascending
    result = users.find().sort("age", 1)
    print("Users sorted by age (ascending):", list(result))
    
    # Sort by multiple fields
    result = users.find().sort([
        ("premium_member", -1),  # descending
        ("name", 1)             # ascending
    ])
    print("\nUsers sorted by premium status and name:", list(result))
    
    # Limit results
    result = users.find().limit(5)
    print("\nFirst 5 users:", list(result))
    
    # Skip and limit (pagination)
    result = users.find().skip(5).limit(5)
    print("\nNext 5 users (pagination):", list(result))

def advanced_queries():
    """Demonstrating advanced query operations"""
    
    # Element exists
    result = users.find({"phone": {"$exists": True}})
    print("Users with phone numbers:", list(result))
    
    # Regular expression
    result = users.find({"email": {"$regex": "@gmail.com$"}})
    print("\nUsers with Gmail:", list(result))
    
    # Array operations
    result = users.find({"interests": {"$size": 2}})
    print("\nUsers with exactly 2 interests:", list(result))
    
    # Complex conditions
    result = users.find({
        "$and": [
            {"age": {"$gte": 18}},
            {"status": "active"},
            {"$or": [
                {"premium_member": True},
                {"referrals": {"$gt": 5}}
            ]}
        ]
    })
    print("\nActive adult users who are premium or have >5 referrals:", list(result))

if __name__ == "__main__":
    print("=== Comparison Operators ===")
    comparison_operators()
    
    print("\n=== Logical Operators ===")
    logical_operators()
    
    print("\n=== Sorting and Limiting ===")
    sorting_and_limiting()
    
    print("\n=== Advanced Queries ===")
    advanced_queries()

"""
Documentation References:
- Query Operators: https://www.mongodb.com/docs/manual/reference/operator/query/
- Regular Expressions: https://www.mongodb.com/docs/manual/reference/operator/query/regex/
- Array Query Operators: https://www.mongodb.com/docs/manual/reference/operator/query-array/
"""