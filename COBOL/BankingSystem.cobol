       IDENTIFICATION DIVISION.
       PROGRAM-ID. SimpleBankingSystem.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT BankAccountFile ASSIGN TO 'accounts.dat'
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  BankAccountFile.
       01  AccountRecord.
           05  AccountID         PIC 9(5).
           05  AccountHolderName  PIC X(30).
           05  Balance            PIC 9(9)V99.

       WORKING-STORAGE SECTION.
       01  WS-TotalAccounts      PIC 9(5) VALUE 0.
       01  WS-TransactionAmount   PIC 9(9)V99.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           OPEN INPUT BankAccountFile
           PERFORM UNTIL EOF(BankAccountFile)
               READ BankAccountFile INTO AccountRecord
                   AT END
                       MOVE 'Y' TO EOF-Flag
                   NOT AT END
                       DISPLAY 'Processing Account: ' AccountHolderName
                       DISPLAY 'Current Balance: $' Balance
                       PERFORM ProcessTransaction
                       ADD 1 TO WS-TotalAccounts
               END-READ
           END-PERFORM
           CLOSE BankAccountFile
           PERFORM DisplaySummary
           STOP RUN.

       ProcessTransaction.
           DISPLAY 'Enter transaction amount (negative for withdrawal): '
           ACCEPT WS-TransactionAmount
           COMPUTE Balance = Balance + WS-TransactionAmount
           DISPLAY 'New Balance: $' Balance.

       DisplaySummary.
           DISPLAY 'Total Accounts Processed: ' WS-TotalAccounts
           DISPLAY '-----------------------------'.

       EOF-Flag VALUE 'N'.
       01  EOF-Flag          PIC X(1) VALUE 'N'.
