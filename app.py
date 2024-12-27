from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage for simplicity
data = []
count = 0

# Route to create a new student record
@app.route('/student/create', methods=['POST'])
def create_student():
    global count
    # Check if request is JSON
    if not request.is_json:
        return jsonify({"message": "Request is not in JSON format"}), 400
    
    body = request.get_json()
    required_fields = ["name", "age", "mark"]
    
    # Validate required fields
    for field in required_fields:
        if field not in body:
            return jsonify({"message": f"The field '{field}' is missing"}), 400
    
    # Add new student data
    data.append({
        "id": count,
        "name": body["name"],
        "age": body["age"],
        "mark": body["mark"]
    })
    count += 1
    return jsonify({"message": "Student created successfully"}), 200

# Route to retrieve a student by ID
@app.route("/student/<int:id>", methods=['GET'])
def get_student_by_id(id):
    for student in data:
        if student["id"] == id:
            return jsonify({"result": student}), 200
    return jsonify({"message": "Student ID not found"}), 404

# Route to retrieve all students
@app.route("/student/all", methods=['GET'])
def get_all_students():
    return jsonify({"result": data}), 200

# Route to update a student record by ID
@app.route("/student/update/<int:id>", methods=['POST'])
def update_student(id):
    # Check if student exists
    student = next((s for s in data if s["id"] == id), None)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Check if request is JSON
    if not request.is_json:
        return jsonify({"message": "Request is not in JSON format"}), 400
    
    body = request.get_json()
    allowed_fields = ["name", "age", "mark"]
    
    # Check if at least one updatable field is provided
    if not any(field in body for field in allowed_fields):
        return jsonify({"message": "No valid fields provided for update"}), 400
    
    # Update student fields
    for field in allowed_fields:
        if field in body:
            student[field] = body[field]
    
    return jsonify({"message": "Student updated successfully"}), 200

# Route to delete a student by ID
@app.route("/student/delete/<int:id>", methods=['DELETE'])
def delete_student(id):
    for i, student in enumerate(data):
        if student["id"] == id:
            del data[i]
            return jsonify({"message": "Student deleted successfully"}), 200
    return jsonify({"message": "Student not found"}), 404

# Entry point of the application
if __name__ == "__main__":
    app.run(debug=True)
