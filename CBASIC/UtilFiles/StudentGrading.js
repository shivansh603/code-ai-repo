// Student Grading System

function gradingSystem() {
    const maxStudents = 50;
    const studentNames = [];
    const grades = [];
    
    let numStudents = parseInt(prompt("Enter the number of students (max 50):"), 10);
    if (numStudents > maxStudents) {
        console.log(`Number of students cannot exceed ${maxStudents}.`);
        return;
    }

    for (let i = 0; i < numStudents; i++) {
        let studentName = prompt(`Enter the name of student ${i + 1}:`);
        let grade = parseFloat(prompt(`Enter the grade of ${studentName}:`));
        studentNames.push(studentName);
        grades.push(grade);
    }

    let total = grades.reduce((acc, grade) => acc + grade, 0);
    let average = total / numStudents;

    console.log(`Average Grade: ${average.toFixed(2)}`);
    console.log("Student Grades:");

    for (let i = 0; i < numStudents; i++) {
        let letterGrade = "";
        if (grades[i] >= 90) {
            letterGrade = "A";
        } else if (grades[i] >= 80) {
            letterGrade = "B";
        } else if (grades[i] >= 70) {
            letterGrade = "C";
        } else if (grades[i] >= 60) {
            letterGrade = "D";
        } else {
            letterGrade = "F";
        }

        console.log(`${studentNames[i]}: ${grades[i]} - ${letterGrade}`);
    }
}

// Run the grading system
gradingSystem();
