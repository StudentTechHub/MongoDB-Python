"""
Student CRUD Operations
This module demonstrates all basic MongoDB CRUD operations with detailed examples.
"""
from typing import List, Optional, Dict, Any
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId

from ..models.student import Student
from ..database.connection import MongoDBConnection

class StudentOperations:
    def __init__(self):
        """Initialize database connection and collection"""
        self.db = MongoDBConnection.get_instance().get_database()
        self.collection = self.db[Student.COLLECTION_NAME]
        self._ensure_indexes()

    def _ensure_indexes(self):
        """Create necessary indexes for the collection"""
        for field, options in Student.INDEXES:
            self.collection.create_index([(field, ASCENDING)], **options)

    # CREATE Operations
    def insert_one(self, student: Student) -> InsertOneResult:
        """
        Insert a single student document
        
        Example:
            student = Student(name="John Doe", email="john@example.com", age=20)
            result = student_ops.insert_one(student)
            print(f"Inserted ID: {result.inserted_id}")
        """
        return self.collection.insert_one(student.to_dict())

    def insert_many(self, students: List[Student]) -> InsertManyResult:
        """
        Insert multiple student documents
        
        Example:
            students = [
                Student(name="John", email="john@example.com", age=20),
                Student(name="Jane", email="jane@example.com", age=22)
            ]
            result = student_ops.insert_many(students)
            print(f"Inserted IDs: {result.inserted_ids}")
        """
        return self.collection.insert_many([s.to_dict() for s in students])

    # READ Operations
    def find_one(self, query: Dict) -> Optional[Student]:
        """
        Find a single student document
        
        Examples:
            # Find by email
            student = student_ops.find_one({"email": "john@example.com"})
            
            # Find by ObjectId
            student = student_ops.find_one({"_id": ObjectId("...")})
            
            # Find with multiple conditions
            student = student_ops.find_one({
                "age": {"$gte": 20},
                "active": True
            })
        """
        doc = self.collection.find_one(query)
        return Student.from_dict(doc) if doc else None

    def find_many(self, 
                 query: Dict = None, 
                 sort_by: List[tuple] = None, 
                 limit: int = None) -> List[Student]:
        """
        Find multiple student documents with optional sorting and limiting
        
        Examples:
            # Find all active students
            students = student_ops.find_many({"active": True})
            
            # Find and sort by age descending
            students = student_ops.find_many(
                sort_by=[("age", DESCENDING)]
            )
            
            # Find with complex query
            students = student_ops.find_many({
                "age": {"$gte": 20, "$lte": 25},
                "courses": {"$in": ["Mathematics", "Physics"]},
                "grades.Mathematics": {"$gte": 80}
            })
            
            # Find with pagination
            students = student_ops.find_many(limit=10)
        """
        cursor = self.collection.find(query or {})
        
        if sort_by:
            cursor = cursor.sort(sort_by)
        
        if limit:
            cursor = cursor.limit(limit)
            
        return [Student.from_dict(doc) for doc in cursor]

    # UPDATE Operations
    def update_one(self, query: Dict, update_data: Dict) -> UpdateResult:
        """
        Update a single student document
        
        Examples:
            # Update age
            result = student_ops.update_one(
                {"email": "john@example.com"},
                {"$set": {"age": 21}}
            )
            
            # Add a new course
            result = student_ops.update_one(
                {"_id": ObjectId("...")},
                {"$push": {"courses": "Biology"}}
            )
            
            # Update grade
            result = student_ops.update_one(
                {"email": "john@example.com"},
                {"$set": {"grades.Mathematics": 95}}
            )
        """
        return self.collection.update_one(query, update_data)

    def update_many(self, query: Dict, update_data: Dict) -> UpdateResult:
        """
        Update multiple student documents
        
        Examples:
            # Increment age for all students
            result = student_ops.update_many(
                {},
                {"$inc": {"age": 1}}
            )
            
            # Update status for inactive students
            result = student_ops.update_many(
                {"active": False},
                {"$set": {"status": "archived"}}
            )
        """
        return self.collection.update_many(query, update_data)

    # DELETE Operations
    def delete_one(self, query: Dict) -> DeleteResult:
        """
        Delete a single student document
        
        Example:
            result = student_ops.delete_one({"email": "john@example.com"})
        """
        return self.collection.delete_one(query)

    def delete_many(self, query: Dict) -> DeleteResult:
        """
        Delete multiple student documents
        
        Examples:
            # Delete inactive students
            result = student_ops.delete_many({"active": False})
            
            # Delete students with no courses
            result = student_ops.delete_many(
                {"courses": {"$size": 0}}
            )
        """
        return self.collection.delete_many(query)

    # Advanced Queries
    def find_with_aggregation(self, pipeline: List[Dict]) -> List[Dict]:
        """
        Execute an aggregation pipeline
        
        Examples:
            # Get average age by course
            pipeline = [
                {"$unwind": "$courses"},
                {"$group": {
                    "_id": "$courses",
                    "avgAge": {"$avg": "$age"},
                    "count": {"$sum": 1}
                }}
            ]
            results = student_ops.find_with_aggregation(pipeline)
            
            # Get grade distribution
            pipeline = [
                {"$project": {
                    "grades": {"$objectToArray": "$grades"}
                }},
                {"$unwind": "$grades"},
                {"$group": {
                    "_id": "$grades.k",
                    "avgGrade": {"$avg": "$grades.v"},
                    "maxGrade": {"$max": "$grades.v"},
                    "minGrade": {"$min": "$grades.v"}
                }}
            ]
            results = student_ops.find_with_aggregation(pipeline)
        """
        return list(self.collection.aggregate(pipeline))