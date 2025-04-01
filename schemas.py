# Sample schemas for MongoDB collections

# User Schema - Basic user information
user_schema = {
    "name": str,  # User's full name
    "email": str,  # Unique email address
    "age": int,    # User's age
    "created_at": "datetime",  # Account creation timestamp
    "address": {   # Nested document example
        "street": str,
        "city": str,
        "country": str
    },
    "interests": [str]  # Array example
}

# Product Schema - E-commerce example
product_schema = {
    "name": str,
    "price": float,
    "description": str,
    "category": str,
    "in_stock": bool,
    "tags": [str],
    "supplier": {
        "name": str,
        "contact": str
    },
    "reviews": [{  # Array of nested documents
        "user_id": "ObjectId",  # Reference to User collection
        "rating": int,
        "comment": str,
        "date": "datetime"
    }]
}

# Order Schema - Demonstrates relationships
order_schema = {
    "user_id": "ObjectId",  # Reference to User collection
    "status": str,
    "items": [{
        "product_id": "ObjectId",  # Reference to Product collection
        "quantity": int,
        "price": float
    }],
    "total_amount": float,
    "shipping_address": {
        "street": str,
        "city": str,
        "country": str
    },
    "order_date": "datetime",
    "payment_status": str
}

"""
Note: These are just schema definitions for reference.
In MongoDB, schemas are flexible and not strictly enforced like in SQL databases.
Types shown here are Python types, in MongoDB they would be BSON types.
ObjectId references are shown as strings here but would be actual ObjectId in MongoDB.
"""