      PROGRAM EmployeeManagementSystem
      IMPLICIT NONE

      INTEGER, PARAMETER :: MAX_EMPLOYEES = 100

      TYPE :: Employee
          INTEGER :: ID
          CHARACTER(LEN=30) :: Name
          REAL :: Salary
      END TYPE Employee

      TYPE(Employee), DIMENSION(MAX_EMPLOYEES) :: Employees
      INTEGER :: EmployeeCount
      INTEGER :: Choice, I

      EmployeeCount = 0

      INTERFACE
          SUBROUTINE AddEmployee(Employees, EmployeeCount)
              TYPE(Employee), DIMENSION(:), INTENT(INOUT) :: Employees
              INTEGER, INTENT(INOUT) :: EmployeeCount
          END SUBROUTINE AddEmployee

          SUBROUTINE DisplayEmployees(Employees, EmployeeCount)
              TYPE(Employee), DIMENSION(:), INTENT(IN) :: Employees
              INTEGER, INTENT(IN) :: EmployeeCount
          END SUBROUTINE DisplayEmployees

          FUNCTION CalculateTotalSalary(Employees, EmployeeCount) RESULT(TotalSalary)
              TYPE(Employee), DIMENSION(:), INTENT(IN) :: Employees
              INTEGER, INTENT(IN) :: EmployeeCount
              REAL :: TotalSalary
          END FUNCTION CalculateTotalSalary
      END INTERFACE

      ! Main program loop
      DO
          PRINT *, '1. Add Employee'
          PRINT *, '2. Display Employees'
          PRINT *, '3. Calculate Total Salary'
          PRINT *, '4. Exit'
          PRINT *, 'Choose an option:'
          READ *, Choice

          SELECT CASE (Choice)
          CASE (1)
              CALL AddEmployee(Employees, EmployeeCount)
          CASE (2)
              CALL DisplayEmployees(Employees, EmployeeCount)
          CASE (3)
              PRINT *, 'Total Salary: ', CalculateTotalSalary(Employees, EmployeeCount)
          CASE (4)
              PRINT *, 'Exiting the program.'
              EXIT
          CASE DEFAULT
              PRINT *, 'Invalid choice. Please choose again.'
          END SELECT
      END DO

      CONTAINS

      SUBROUTINE AddEmployee(Employees, EmployeeCount)
          TYPE(Employee), DIMENSION(:), INTENT(INOUT) :: Employees
          INTEGER, INTENT(INOUT) :: EmployeeCount
          INTEGER :: NewID
          CHARACTER(LEN=30) :: NewName
          REAL :: NewSalary

          IF (EmployeeCount < MAX_EMPLOYEES) THEN
              PRINT *, 'Enter Employee ID:'
              READ *, NewID
              PRINT *, 'Enter Employee Name:'
              READ *, NewName
              PRINT *, 'Enter Employee Salary:'
              READ *, NewSalary

              Employees(EmployeeCount + 1)%ID = NewID
              Employees(EmployeeCount + 1)%Name = NewName
              Employees(EmployeeCount + 1)%Salary = NewSalary
              EmployeeCount = EmployeeCount + 1
          ELSE
              PRINT *, 'Employee limit reached.'
          END IF
      END SUBROUTINE AddEmployee

      SUBROUTINE DisplayEmployees(Employees, EmployeeCount)
          TYPE(Employee), DIMENSION(:), INTENT(IN) :: Employees
          INTEGER, INTENT(IN) :: EmployeeCount
          INTEGER :: I

          PRINT *, 'Employees List:'
          DO I = 1, EmployeeCount
              PRINT *, 'ID: ', Employees(I)%ID, ' Name: ', Employees(I)%Name, ' Salary: ', Employees(I)%Salary
          END DO
      END SUBROUTINE DisplayEmployees

      FUNCTION CalculateTotalSalary(Employees, EmployeeCount) RESULT(TotalSalary)
          TYPE(Employee), DIMENSION(:), INTENT(IN) :: Employees
          INTEGER, INTENT(IN) :: EmployeeCount
          REAL :: TotalSalary
          INTEGER :: I

          TotalSalary = 0.0
          DO I = 1, EmployeeCount
              TotalSalary = TotalSalary + Employees(I)%Salary
          END DO
      END FUNCTION CalculateTotalSalary

      END PROGRAM EmployeeManagementSystem
