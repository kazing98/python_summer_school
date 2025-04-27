from typing import Dict, Any, Set
from datetime import date
import uuid

class Course:
    def __init__(self, name: str, max_capacity: int, course_type: str,
                 difficulty_level: str = None, materials_required: Set[str] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.max_capacity = max_capacity
        self.course_type = course_type
        self.difficulty_level = difficulty_level
        self.materials_required = materials_required or set()
        self.students = set()  # Set of student IDs
        self.teacher_id = None
        self.attendance = {}  # Dictionary mapping dates to sets of present student IDs
        self.grades = {}  # Dictionary mapping student IDs to their grades
        self.validate()

    def validate(self):
        """Validate course data"""
        # TODO: Implement the validate method
        # 1. Validate that name is a non-empty string
        # 2. Validate that max_capacity is a positive integer
        # 3. Validate that course_type is either 'math' or 'art'
        # 4. For math courses:
        #    - Validate that difficulty_level is one of: 'beginner', 'intermediate', 'advanced'
        # 5. For art courses:
        #    - Validate that materials_required is a set
        #    - Validate that all materials are strings
        if not isinstance(self.name, str):
            raise ValueError("Course Name should be a String/Text !")

        if not isinstance(self.max_capacity, int):
            raise ValueError("Max Capacity needs to be an Integer !")
        if  self.max_capacity <= 0:
            raise ValueError("Max Capacity needs to be greater than 0 !")

        if self.course_type not in ['math', 'art']:
            raise ValueError("Course Type should be either math or art.")

        if self.course_type.lower() == 'math':
            if self.difficulty_level.lower() not in ['beginner', 'intermediate', 'advanced']:
                raise ValueError("Difficulty Level should be either beginner, intermediate or advanced.")
        elif self.course_type.lower() == 'art':
            if not isinstance(self.materials_required, set):
                raise ValueError("Materials Required should be a set.")
            if not all(isinstance(item, str) for item in self.materials_required):
                raise ValueError("All materials must be strings.")


    def take_attendance(self, date: date, present_student_ids: Set[str]):
        """Record attendance for a specific date"""
        # TODO: Implement the take_attendance method
        # 1. Validate that present_student_ids is a set
        # 2. Validate that all IDs in present_student_ids are strings
        # 3. Check that number of present students doesn't exceed enrolled students
        # 4. Verify all present students are enrolled in the course
        # 5. Record the attendance for the given date
        if not isinstance(present_student_ids, set):
            raise ValueError("Present Student IDs should be a set.")

        if not all(isinstance(item, str) for item in present_student_ids):
            raise ValueError("All IDs in Present Student ID should be a string/text.")


        pass

    def assign_grade(self, student_id: str, grade: float):
        """Assign a grade to a student"""
        # TODO: Implement the assign_grade method
        # 1. Check if student is enrolled in the course
        # 2. Validate that grade is a number
        # 3. Validate that grade is between 0 and 100
        # 4. Assign the grade to the student
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert course data to dictionary"""
        # TODO: Implement the to_dict method
        # 1. Create a dictionary with the course's basic information:
        #    - id, name, course_type, max_capacity, current enrollment, teacher_id
        # 2. For math courses: include difficulty_level
        # 3. For art courses: include materials_required as a list
        # 4. Return the dictionary
        base_dict = {
            "id": self.id,
            "name": self.name,
            "course_type": self.course_type,
            "max_capacity": self.max_capacity,
            "teacher_id":self.teacher_id
        }
        if self.course_type.lower() == "math":
            base_dict.update({
                "difficulty_level":self.difficulty_level
            })
        elif self.course_type.lower() == "art":
            base_dict.update({
                "materials_required": list(self.materials_required)
            })

        return base_dict