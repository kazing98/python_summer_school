from logging import raiseExceptions

from flask import Flask, jsonify, request
from models import University, Student, Teacher, Course

app = Flask(__name__)
university = University()

# Error handler for ValueError
@app.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({"error": str(error)}), 400

# Student endpoints
@app.route('/students', methods=['GET', 'POST'])
def handle_students():
    if request.method == 'POST':
        data = request.get_json()
        try:
            student = Student(
                name=data['name'],
                contact_info=data['contact_info']
            )
            student_id = university.add_student(student)
            return jsonify({"id": student_id}), 201
        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400
    
    # GET method
    return jsonify({
        "students": [student.to_dict() for student in university.students.values()]
    })

@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student's details"""
    # TODO: Implement get_student endpoint
    # 1. Check if student exists
    # 2. Return student data or 404 error
    if request.method == 'GET':
        try:
            student_details = [student.to_dict() for student in university.students.values() if student.id == student_id]
            if student_details:
                return jsonify(student_details), 201
            raise ValueError(f"Student with ID {student_id} not found!!")

        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400
    return None


# Teacher endpoints
@app.route('/teachers', methods=['GET', 'POST'])
def handle_teachers():
    """Handle teacher creation and listing"""
    # TODO: Implement handle_teachers endpoint
    # For POST:
    # 1. Get JSON data
    # 2. Create Teacher instance with name, contact_info, and specializations
    # 3. Add teacher to university
    # 4. Return teacher ID
    # For GET:
    # 1. Return list of all teachers
    if request.method == 'POST':
        data = request.get_json()
        try:
            teacher = Teacher(
                name=data['name'],
                contact_info=data['contact_info'],
                specializations=data['specializations']
            )
            teacher_id = university.add_teacher(teacher)
            return jsonify({"id": teacher_id}), 201
        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400

    return jsonify({
        "teachers": [teacher.to_dict() for teacher in university.teachers.values()]
    })

# Course endpoints
@app.route('/courses', methods=['GET', 'POST'])
def handle_courses():
    """Handle course creation and listing"""
    # TODO: Implement handle_courses endpoint
    # For POST:
    # 1. Get JSON data
    # 2. Extract course type and create appropriate course arguments
    # 3. Create Course instance
    # 4. Add course to university
    # 5. Return course ID
    # For GET:
    # 1. Return list of all courses
    if request.method == 'POST':
        data = request.get_json()
        try:
            course = None
            if data['course_type'] == 'math':
                course = Course(data['name'],
                                data['max_capacity'],
                                data['course_type'],
                                data['difficulty_level'])

            elif data['course_type'] == 'art':
                course = Course(data['name'],
                                data['max_capacity'],
                                data['course_type'],
                                data['difficulty_level'],
                                set(data['materials_required']))

            course_id = university.add_course(course)

            return jsonify({"course_id": course_id}), 201
        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({
        "courses": [course.to_dict() for course in university.courses.values()]
    })

# Enrollment endpoints
@app.route('/courses/<course_id>/students/<student_id>', methods=['POST', 'DELETE'])
def handle_enrollment(course_id, student_id):
    """Handle student enrollment and withdrawal"""
    # TODO: Implement handle_enrollment endpoint
    # For POST:
    # 1. Try to enroll student in course
    # 2. Return success/failure message
    # For DELETE:
    # 1. Try to withdraw student from course
    # 2. Return success/failure message
    if request.method == 'POST':
        try:
            if university.enroll_student(student_id, course_id):
                return jsonify({"enrollment": "Enrollment done successfully."}), 201
            else:
                raise ValueError("Max capacity reached. Enrollment cannot be done.")
        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400

    elif request.method == 'DELETE':
        try:
            if university.withdraw_student(student_id, course_id):
                return jsonify({"withdrawn": "Enrollment withdrawn successfully."}), 201
            else:
                raise ValueError("Student not enrolled to the course.")
        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400

    return None

# Course assignment endpoints
@app.route('/courses/<course_id>/teacher/<teacher_id>', methods=['POST'])
def assign_teacher_to_course(course_id, teacher_id):
    """Assign a teacher to a course"""
    # TODO: Implement assign_teacher_to_course endpoint
    # 1. Try to assign teacher to course
    # 2. Return success/failure message
    if request.method == 'POST':
        try:
            if university.assign_teacher(teacher_id, course_id):
                return jsonify({"assignment": f"Teacher assigned to {course_id} course_id successfully."}), 201

        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400
    return None


# Attendance endpoints
@app.route('/courses/<course_id>/attendance', methods=['POST'])
def record_attendance(course_id):
    """Record attendance for a course"""
    # TODO: Implement record_attendance endpoint
    # 1. Get JSON data with date and present students
    # 2. Try to record attendance
    # 3. Return success/failure message
    if request.method == 'POST':
        data = request.get_json()
        try:
            if course_id in university.courses:
                university.record_attendance(course_id, data["date"], set(data["present_students"]))
                return jsonify({"attendance": f"Attendance taken successfully for {data["date"]}"}), 201

        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400
    return None


# Grade endpoints
@app.route('/courses/<course_id>/grades/<student_id>', methods=['POST'])
def assign_grade(course_id, student_id):
    """Assign a grade to a student"""
    # TODO: Implement assign_grade endpoint
    # 1. Get JSON data with grade
    # 2. Try to assign grade
    # 3. Return success/failure message
    if request.method == 'POST':
        data = request.get_json()
        try:
            if course_id in university.courses and university.assign_grade(course_id, student_id, data['grade']):
                return jsonify({"grade": f"Grade updated successfully for {student_id}"}), 201
            else:
                raise ValueError("Something went wrong")
        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400
    return None

# Get all grades for a student
@app.route('/students/<student_id>/grades', methods=['GET'])
def get_all_grades(student_id):
    """Getting all grades scored in different subjects by a student"""
    if request.method == 'GET':
        try:
            if student_id in university.students:
                result = university.get_student_grades(student_id)
                return jsonify(result), 201
            else:
                raise ValueError("Student ID not found")
        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400
    return None

# Get all grades for a course
@app.route('/course/<course_id>/grades', methods=['GET'])
def get_all_course_grades(course_id):
    """Getting all grades scored in different subjects by a student"""
    if request.method == 'GET':
        try:
            if course_id in university.courses:
                return jsonify(university.get_course_grades(course_id)), 201
            else:
                raise ValueError("Course ID not found")
        except (KeyError, ValueError) as e:
            return jsonify({"error": str(e)}), 400
    return None

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)