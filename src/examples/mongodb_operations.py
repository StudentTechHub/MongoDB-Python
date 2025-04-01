"""
MongoDB Operations Examples
This module demonstrates various MongoDB operations using the Student model.
"""
from pymongo import DESCENDING
from ..crud.student_operations import StudentOperations
from ..models.student import Student

def demonstrate_basic_operations():
    """Demonstrate basic CRUD operations"""
    student_ops = StudentOperations()

    print("1. Creating a new student")
    new_student = Student(
        name="Test Student",
        email="test.student@example.com",
        age=20,
        courses=["Python", "MongoDB"],
        grades={"Python": 95.0}
    )
    result = student_ops.insert_one(new_student)
    print(f"Inserted student ID: {result.inserted_id}")

    print("\n2. Finding a student by email")
    found_student = student_ops.find_one({"email": "test.student@example.com"})
    print(f"Found student: {found_student.name}")

    print("\n3. Updating student's grade")
    update_result = student_ops.update_one(
        {"email": "test.student@example.com"},
        {"$set": {"grades.MongoDB": 88.5}}
    )
    print(f"Modified {update_result.modified_count} document")

    print("\n4. Finding students with various filters")
    # Find students aged 20 or older
    students = student_ops.find_many(
        {"age": {"$gte": 20}},
        sort_by=[("age", DESCENDING)]
    )
    print(f"Students aged 20 or older: {len(students)}")

    # Find students taking Python
    python_students = student_ops.find_many({"courses": "Python"})
    print(f"Students taking Python: {len(python_students)}")

def demonstrate_advanced_operations():
    """Demonstrate advanced MongoDB operations"""
    student_ops = StudentOperations()

    print("\n5. Aggregation Pipeline Examples")
    
    # Calculate average grades by course
    pipeline = [
        {"$project": {
            "grades": {"$objectToArray": "$grades"}
        }},
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$grades.k",
            "averageGrade": {"$avg": "$grades.v"},
            "numberOfStudents": {"$sum": 1}
        }}
    ]
    grade_stats = student_ops.find_with_aggregation(pipeline)
    print("\nGrade Statistics by Course:")
    for stat in grade_stats:
        print(f"{stat['_id']}: Avg Grade = {stat['averageGrade']:.2f}, "
              f"Students = {stat['numberOfStudents']}")

    # Find course popularity
    pipeline = [
        {"$unwind": "$courses"},
        {"$group": {
            "_id": "$courses",
            "studentCount": {"$sum": 1},
            "averageAge": {"$avg": "$age"}
        }},
        {"$sort": {"studentCount": -1}}
    ]
    course_stats = student_ops.find_with_aggregation(pipeline)
    print("\nCourse Statistics:")
    for stat in course_stats:
        print(f"{stat['_id']}: Students = {stat['studentCount']}, "
              f"Avg Age = {stat['averageAge']:.1f}")

def demonstrate_batch_operations():
    """Demonstrate batch operations"""
    student_ops = StudentOperations()

    print("\n6. Batch Update Operations")
    # Update all active students' age
    result = student_ops.update_many(
        {"active": True},
        {"$inc": {"age": 1}}
    )
    print(f"Updated age for {result.modified_count} active students")

    # Add a new course to all students with high grades
    result = student_ops.update_many(
        {"grades.Python": {"$gte": 90}},
        {"$push": {"courses": "Advanced Python"}}
    )
    print(f"Added Advanced Python course to {result.modified_count} students")

def run_all_examples():
    """Run all MongoDB operation examples"""
    print("=== MongoDB Operations Examples ===")
    demonstrate_basic_operations()
    demonstrate_advanced_operations()
    demonstrate_batch_operations()

if __name__ == "__main__":
    run_all_examples()