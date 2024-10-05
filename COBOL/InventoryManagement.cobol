       IDENTIFICATION DIVISION.
       PROGRAM-ID. InventoryManagement.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT InventoryFile ASSIGN TO 'inventory.dat'
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  InventoryFile.
       01  InventoryRecord.
           05  ProductID         PIC 9(5).
           05  ProductName       PIC X(30).
           05  StockLevel        PIC 9(5).
           05  SoldUnits         PIC 9(5).

       WORKING-STORAGE SECTION.
       01  WS-TotalProducts       PIC 9(5) VALUE 0.
       01  WS-TotalStockLevel     PIC 9(5) VALUE 0.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           OPEN INPUT InventoryFile
           PERFORM UNTIL EOF(InventoryFile)
               READ InventoryFile INTO InventoryRecord
                   AT END
                       MOVE 'Y' TO EOF-Flag
                   NOT AT END
                       COMPUTE StockLevel = StockLevel - SoldUnits
                       ADD 1 TO WS-TotalProducts
                       ADD StockLevel TO WS-TotalStockLevel
               END-READ
           END-PERFORM
           CLOSE InventoryFile
           PERFORM DisplayInventory
           STOP RUN.

       DisplayInventory.
           DISPLAY 'Inventory Summary'
           DISPLAY '--------------------'
           DISPLAY 'Total Products: ' WS-TotalProducts
           DISPLAY 'Total Stock Level: ' WS-TotalStockLevel
           DISPLAY '--------------------'.

       EOF-Flag VALUE 'N'.
       01  EOF-Flag          PIC X(1) VALUE 'N'.
