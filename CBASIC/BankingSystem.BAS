10 REM Simple Banking System
20 DIM BALANCE
30 DIM AMOUNT

40 BALANCE = 1000  REM Initial balance
50 PRINT "Welcome to the Banking System"

60 DO
70   PRINT "Current Balance: "; BALANCE
80   PRINT "1. Deposit"
90   PRINT "2. Withdraw"
100  PRINT "3. Exit"
110  INPUT CHOICE

120  IF CHOICE = 1 THEN
130    PRINT "Enter deposit amount:"
140    INPUT AMOUNT
150    IF AMOUNT > 0 THEN
160      BALANCE = BALANCE + AMOUNT
170      PRINT "Deposited: "; AMOUNT
180    ELSE
190      PRINT "Invalid amount."
200    END IF
210  END IF

220  IF CHOICE = 2 THEN
230    PRINT "Enter withdrawal amount:"
240    INPUT AMOUNT
250    IF AMOUNT > 0 AND AMOUNT <= BALANCE THEN
260      BALANCE = BALANCE - AMOUNT
270      PRINT "Withdrawn: "; AMOUNT
280    ELSE
290      PRINT "Invalid amount or insufficient funds."
300    END IF
310  END IF

320 LOOP UNTIL CHOICE = 3

330 PRINT "Thank you for using the Banking System."
340 END
