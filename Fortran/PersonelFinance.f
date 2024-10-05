      PROGRAM PersonalFinanceTracker
      IMPLICIT NONE

      INTEGER, PARAMETER :: MAX_EXPENSES = 100
      INTEGER :: ExpenseCount, I
      REAL :: Expenses(MAX_EXPENSES), TotalExpenses, Income, RemainingBudget

      ! Initialize variables
      ExpenseCount = 0
      TotalExpenses = 0.0

      ! Input user income
      PRINT *, 'Enter your total income:'
      READ *, Income

      ! Input expenses
      DO
          PRINT *, 'Enter an expense amount (or -1 to finish):'
          READ *, Expenses(ExpenseCount + 1)

          IF (Expenses(ExpenseCount + 1) == -1) EXIT
          IF (ExpenseCount < MAX_EXPENSES) THEN
              TotalExpenses = TotalExpenses + Expenses(ExpenseCount + 1)
              ExpenseCount = ExpenseCount + 1
          ELSE
              PRINT *, 'Maximum expense limit reached.'
          END IF
      END DO

      ! Calculate remaining budget
      RemainingBudget = Income - TotalExpenses

      ! Display results
      PRINT *, 'Total Expenses: ', TotalExpenses
      PRINT *, 'Remaining Budget: ', RemainingBudget

      IF (RemainingBudget < 0) THEN
          PRINT *, 'Warning: You have exceeded your budget!'
      ELSE
          PRINT *, 'You are within your budget.'
      END IF

      END PROGRAM PersonalFinanceTracker
