"""
Student Model Schema
Demonstrates MongoDB document structure and field validations using Python classes.
"""
from datetime import datetime
from typing import List, Optional, Dict

class Student:
    """
    Student Schema Definition
    Demonstrates various MongoDB data types and nested documents
    """
    def __init__(
        self,
        name: str,
        email: str,
        age: int,
        courses: List[str] = None,
        address: Dict = None,
        created_at: datetime = None,
        grades: Dict[str, float] = None,
        active: bool = True
    ):
        self.name = name
        self.email = email
        self.age = age
        self.courses = courses or []
        self.address = address or {}
        self.created_at = created_at or datetime.utcnow()
        self.grades = grades or {}
        self.active = active

    def to_dict(self) -> dict:
        """Convert Student object to dictionary for MongoDB storage"""
        return {
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "courses": self.courses,
            "address": self.address,
            "created_at": self.created_at,
            "grades": self.grades,
            "active": self.active
        }

    @staticmethod
    def from_dict(data: dict) -> 'Student':
        """Create Student object from MongoDB document"""
        return Student(
            name=data["name"],
            email=data["email"],
            age=data["age"],
            courses=data.get("courses", []),
            address=data.get("address", {}),
            created_at=data.get("created_at", datetime.utcnow()),
            grades=data.get("grades", {}),
            active=data.get("active", True)
        )

    # MongoDB collection configuration
    COLLECTION_NAME = "students"
    INDEXES = [
        ("email", {"unique": True}),  # Unique index on email
        ("name", {}),                 # Regular index on name
        ("created_at", {})            # Index for timestamp-based queries
    ]