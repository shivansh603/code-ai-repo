       IDENTIFICATION DIVISION.
       PROGRAM-ID. PayrollProcessing.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT EmployeeFile ASSIGN TO 'employee.dat'
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  EmployeeFile.
       01  EmployeeRecord.
           05  EmployeeID         PIC 9(5).
           05  EmployeeName       PIC X(30).
           05  HourlyRate         PIC 9(4)V99.
           05  HoursWorked        PIC 9(4).

       WORKING-STORAGE SECTION.
       01  WS-EmployeeCount          PIC 9(5) VALUE 0.
       01  WS-TotalGrossPay          PIC 9(9)V99 VALUE 0.
       01  WS-TotalDeductions        PIC 9(9)V99 VALUE 0.
       01  WS-TotalNetPay            PIC 9(9)V99 VALUE 0.
       01  WS-DeductionRate          PIC 9(3)V99 VALUE 0.15.

       01  WS-GrossPay               PIC 9(9)V99.
       01  WS-Deductions             PIC 9(9)V99.
       01  WS-NetPay                 PIC 9(9)V99.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           OPEN INPUT EmployeeFile
           PERFORM UNTIL EOF(EmployeeFile)
               READ EmployeeFile INTO EmployeeRecord
                   AT END
                       MOVE 'Y' TO EOF-Flag
                   NOT AT END
                       PERFORM ProcessEmployee
                       ADD 1 TO WS-EmployeeCount
               END-READ
           END-PERFORM
           CLOSE EmployeeFile
           PERFORM DisplaySummary
           STOP RUN.

       ProcessEmployee.
           COMPUTE WS-GrossPay = HourlyRate * HoursWorked
           COMPUTE WS-Deductions = WS-GrossPay * WS-DeductionRate
           COMPUTE WS-NetPay = WS-GrossPay - WS-Deductions

           ADD WS-GrossPay TO WS-TotalGrossPay
           ADD WS-Deductions TO WS-TotalDeductions
           ADD WS-NetPay TO WS-TotalNetPay.

       DisplaySummary.
           DISPLAY 'Payroll Summary'
           DISPLAY '------------------'
           DISPLAY 'Total Employees Processed: ' WS-EmployeeCount
           DISPLAY 'Total Gross Pay: $' WS-TotalGrossPay
           DISPLAY 'Total Deductions: $' WS-TotalDeductions
           DISPLAY 'Total Net Pay: $' WS-TotalNetPay
           DISPLAY '------------------'.
           
       EOF-Flag VALUE 'N'.
       01  EOF-Flag          PIC X(1) VALUE 'N'.
