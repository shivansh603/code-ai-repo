       IDENTIFICATION DIVISION.
       PROGRAM-ID. StudentGradesManagement.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT StudentFile ASSIGN TO 'students.dat'
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  StudentFile.
       01  StudentRecord.
           05  StudentID         PIC 9(5).
           05  StudentName       PIC X(30).
           05  Grade             PIC 9(3).

       WORKING-STORAGE SECTION.
       01  WS-TotalStudents       PIC 9(5) VALUE 0.
       01  WS-PassingGrade       PIC 9(3) VALUE 60.
       01  WS-TotalGrades        PIC 9(5) VALUE 0.
       01  WS-AverageGrade       PIC 9(5)V99.

       01  WS-StudentCount        PIC 9(5) VALUE 0.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           OPEN INPUT StudentFile
           PERFORM UNTIL EOF(StudentFile)
               READ StudentFile INTO StudentRecord
                   AT END
                       MOVE 'Y' TO EOF-Flag
                   NOT AT END
                       ADD Grade TO WS-TotalGrades
                       ADD 1 TO WS-TotalStudents
                       ADD 1 TO WS-StudentCount
               END-READ
           END-PERFORM
           CLOSE StudentFile
           COMPUTE WS-AverageGrade = WS-TotalGrades / WS-TotalStudents
           PERFORM DisplayResults
           STOP RUN.

       DisplayResults.
           DISPLAY 'Student Grades Report'
           DISPLAY '------------------------'
           DISPLAY 'Total Students: ' WS-TotalStudents
           DISPLAY 'Average Grade: ' WS-AverageGrade

           IF WS-AverageGrade >= WS-PassingGrade THEN
               DISPLAY 'Overall: Passed'
           ELSE
               DISPLAY 'Overall: Failed'
           END-IF.

       EOF-Flag VALUE 'N'.
       01  EOF-Flag          PIC X(1) VALUE 'N'.
