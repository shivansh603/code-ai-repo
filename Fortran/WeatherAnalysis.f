      PROGRAM WeatherDataAnalysis
      IMPLICIT NONE

      INTEGER, PARAMETER :: MAX_DAYS = 365
      INTEGER :: DaysRecorded, I
      REAL :: Temperatures(MAX_DAYS)
      REAL :: TotalTemperature, AverageTemperature
      INTEGER :: AboveAverageCount

      ! Initialize variables
      TotalTemperature = 0.0
      AboveAverageCount = 0

      ! Prompt user for the number of recorded days
      PRINT *, 'Enter the number of days recorded (1 to ', MAX_DAYS, '):'
      READ *, DaysRecorded

      ! Input temperature data
      DO I = 1, DaysRecorded
          PRINT *, 'Enter temperature for day ', I, ':'
          READ *, Temperatures(I)
          TotalTemperature = TotalTemperature + Temperatures(I)
      END DO

      ! Calculate average temperature
      AverageTemperature = TotalTemperature / DaysRecorded
      PRINT *, 'Average Temperature: ', AverageTemperature

      ! Count days above average
      DO I = 1, DaysRecorded
          IF (Temperatures(I) > AverageTemperature) THEN
              AboveAverageCount = AboveAverageCount + 1
          END IF
      END DO

      ! Display result
      PRINT *, 'Number of days above average: ', AboveAverageCount

      END PROGRAM WeatherDataAnalysis
