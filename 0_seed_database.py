from datetime import datetime, timedelta
from connection import get_database
from bson import ObjectId
import random

def seed_database():
    """Seed the database with sample data for demonstration"""
    
    db = get_database()
    
    # Clear existing data
    db.users.drop()
    db.products.drop()
    db.orders.drop()
    
    # Sample user data
    users = [
        {
            "_id": ObjectId(),
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "country": "USA"
            },
            "interests": ["technology", "reading"],
            "premium_member": True,
            "created_at": datetime.now(),
            "description": "Tech enthusiast and avid reader",
            "status": "active",
            "referrals": 7
        },
        {
            "_id": ObjectId(),
            "name": "Jane Smith",
            "email": "jane@gmail.com",
            "age": 25,
            "address": {
                "street": "456 Park Ave",
                "city": "London",
                "country": "UK"
            },
            "interests": ["sports", "music"],
            "premium_member": False,
            "created_at": datetime.now() - timedelta(days=30),
            "description": "Sports lover and musician",
            "status": "active",
            "referrals": 3
        },
        # Add more sample users
        {
            "_id": ObjectId(),
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "age": 35,
            "address": {
                "street": "789 Oak Rd",
                "city": "Toronto",
                "country": "Canada"
            },
            "interests": ["technology", "sports", "cooking"],
            "premium_member": True,
            "created_at": datetime.now() - timedelta(days=60),
            "description": "Food tech enthusiast",
            "status": "active",
            "referrals": 10
        }
    ]
    
    # Sample product data
    products = [
        {
            "_id": ObjectId(),
            "name": "Laptop Pro",
            "price": 1299.99,
            "category": "Electronics",
            "in_stock": True,
            "tags": ["computer", "tech", "work"],
            "supplier": {
                "name": "TechCorp",
                "contact": "supplier@techcorp.com"
            }
        },
        {
            "_id": ObjectId(),
            "name": "Running Shoes",
            "price": 89.99,
            "category": "Sports",
            "in_stock": True,
            "tags": ["shoes", "sports", "running"],
            "supplier": {
                "name": "SportGear",
                "contact": "orders@sportgear.com"
            }
        }
    ]
    
    # Sample order data
    orders = [
        {
            "user_id": users[0]["_id"],
            "items": [
                {
                    "product_id": products[0]["_id"],
                    "quantity": 1,
                    "price": products[0]["price"]
                }
            ],
            "total_amount": products[0]["price"],
            "status": "completed",
            "created_at": datetime.now() - timedelta(days=5)
        },
        {
            "user_id": users[1]["_id"],
            "items": [
                {
                    "product_id": products[1]["_id"],
                    "quantity": 2,
                    "price": products[1]["price"]
                }
            ],
            "total_amount": products[1]["price"] * 2,
            "status": "pending",
            "created_at": datetime.now()
        }
    ]
    
    # Insert the sample data
    db.users.insert_many(users)
    db.products.insert_many(products)
    db.orders.insert_many(orders)
    
    print("Database seeded successfully!")
    print(f"Inserted {len(users)} users")
    print(f"Inserted {len(products)} products")
    print(f"Inserted {len(orders)} orders")

if __name__ == "__main__":
    seed_database()