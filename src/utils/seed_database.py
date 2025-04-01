"""
Database Seeder
This script populates the MongoDB database with sample data for demonstration purposes.
"""
from datetime import datetime, timedelta
from ..models.student import Student
from ..crud.student_operations import StudentOperations

def seed_database():
    """Seed the database with sample student data"""
    student_ops = StudentOperations()
    
    # Sample courses
    courses = [
        "Mathematics", "Physics", "Chemistry", "Biology",
        "Computer Science", "History", "Literature"
    ]
    
    # Sample students with various data patterns
    students = [
        Student(
            name="John Doe",
            email="john.doe@example.com",
            age=20,
            courses=["Mathematics", "Physics", "Computer Science"],
            address={
                "street": "123 Main St",
                "city": "Boston",
                "state": "MA",
                "zip": "02108"
            },
            grades={
                "Mathematics": 85.5,
                "Physics": 92.0,
                "Computer Science": 88.5
            }
        ),
        Student(
            name="Jane Smith",
            email="jane.smith@example.com",
            age=22,
            courses=["Chemistry", "Biology"],
            address={
                "street": "456 Park Ave",
                "city": "New York",
                "state": "NY",
                "zip": "10001"
            },
            grades={
                "Chemistry": 94.0,
                "Biology": 91.5
            }
        ),
        Student(
            name="Bob Wilson",
            email="bob.wilson@example.com",
            age=19,
            courses=["History", "Literature", "Computer Science"],
            address={
                "street": "789 Oak Rd",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94102"
            },
            grades={
                "History": 88.0,
                "Literature": 95.0,
                "Computer Science": 82.5
            }
        ),
        # Student with no courses (for filtering examples)
        Student(
            name="Alice Brown",
            email="alice.brown@example.com",
            age=21,
            courses=[],
            address={
                "street": "321 Pine St",
                "city": "Seattle",
                "state": "WA",
                "zip": "98101"
            },
            grades={}
        ),
        # Inactive student (for status filtering examples)
        Student(
            name="Charlie Davis",
            email="charlie.davis@example.com",
            age=23,
            courses=["Physics", "Mathematics"],
            active=False,
            grades={
                "Physics": 78.5,
                "Mathematics": 81.0
            }
        )
    ]
    
    try:
        # Clear existing data
        student_ops.delete_many({})
        
        # Insert new students
        result = student_ops.insert_many(students)
        print(f"Successfully inserted {len(result.inserted_ids)} students")
        
        # Demonstrate some queries
        print("\nExample Queries:")
        
        # Find active students
        active_count = len(student_ops.find_many({"active": True}))
        print(f"Active students: {active_count}")
        
        # Find students with high math grades
        math_students = student_ops.find_many({
            "grades.Mathematics": {"$gte": 85}
        })
        print(f"Students with high math grades: {len(math_students)}")
        
        # Find students taking Computer Science
        cs_students = student_ops.find_many({
            "courses": "Computer Science"
        })
        print(f"Computer Science students: {len(cs_students)}")
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")

if __name__ == "__main__":
    seed_database()