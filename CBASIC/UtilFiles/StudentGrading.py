# Student Grading System

def grading_system():
    max_students = 50
    student_names = []
    grades = []

    num_students = int(input("Enter the number of students (max 50): "))
    if num_students > max_students:
        print(f"Number of students cannot exceed {max_students}.")
        return

    for i in range(num_students):
        student_name = input(f"Enter the name of student {i + 1}: ")
        grade = float(input(f"Enter the grade of {student_name}: "))
        student_names.append(student_name)
        grades.append(grade)

    total = sum(grades)
    average = total / num_students

    print(f"Average Grade: {average:.2f}")
    print("Student Grades:")
    
    for i in range(num_students):
        letter_grade = ""
        if grades[i] >= 90:
            letter_grade = "A"
        elif grades[i] >= 80:
            letter_grade = "B"
        elif grades[i] >= 70:
            letter_grade = "C"
        elif grades[i] >= 60:
            letter_grade = "D"
        else:
            letter_grade = "F"

        print(f"{student_names[i]}: {grades[i]} - {letter_grade}")

# Run the grading system
grading_system()
