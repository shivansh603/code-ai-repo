10 REM Fitness Tracker
20 DIM CALORIES(7)
30 DIM TOTAL_CALORIES, I

40 TOTAL_CALORIES = 0

50 PRINT "Fitness Tracker"
60 PRINT "Log your calories burned for the week"

70 FOR I = 1 TO 7
80   PRINT "Enter calories burned for day "; I; ":"
90   INPUT CALORIES(I)
100  IF CALORIES(I) < 0 THEN
110    PRINT "Invalid input. Please enter a non-negative number."
120    PRINT "Re-enter calories for day "; I
130    INPUT CALORIES(I)
140  END IF
150  TOTAL_CALORIES = TOTAL_CALORIES + CALORIES(I)
160 NEXT I

170 PRINT "Total calories burned this week: "; TOTAL_CALORIES
180 PRINT "Average calories burned per day: "; TOTAL_CALORIES / 7
190 END
