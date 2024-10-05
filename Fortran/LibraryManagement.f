      PROGRAM LibraryManagementSystem
      IMPLICIT NONE

      INTEGER, PARAMETER :: MAX_BOOKS = 100

      TYPE :: Book
          CHARACTER(LEN=30) :: Title
          CHARACTER(LEN=30) :: Author
          INTEGER :: Year
          LOGICAL :: Available
      END TYPE Book

      TYPE(Book), DIMENSION(MAX_BOOKS) :: Books
      INTEGER :: BookCount
      INTEGER :: Choice, I

      BookCount = 0

      INTERFACE
          SUBROUTINE AddBook(Books, BookCount)
              TYPE(Book), DIMENSION(:), INTENT(INOUT) :: Books
              INTEGER, INTENT(INOUT) :: BookCount
          END SUBROUTINE AddBook

          SUBROUTINE DisplayBooks(Books, BookCount)
              TYPE(Book), DIMENSION(:), INTENT(IN) :: Books
              INTEGER, INTENT(IN) :: BookCount
          END SUBROUTINE DisplayBooks

          SUBROUTINE SearchBook(Books, BookCount)
              TYPE(Book), DIMENSION(:), INTENT(IN) :: Books
              INTEGER, INTENT(IN) :: BookCount
          END SUBROUTINE SearchBook
      END INTERFACE

      ! Main program loop
      DO
          PRINT *, '1. Add Book'
          PRINT *, '2. Display Books'
          PRINT *, '3. Search Book by Title'
          PRINT *, '4. Exit'
          PRINT *, 'Choose an option:'
          READ *, Choice

          SELECT CASE (Choice)
          CASE (1)
              CALL AddBook(Books, BookCount)
          CASE (2)
              CALL DisplayBooks(Books, BookCount)
          CASE (3)
              CALL SearchBook(Books, BookCount)
          CASE (4)
              PRINT *, 'Exiting the program.'
              EXIT
          CASE DEFAULT
              PRINT *, 'Invalid choice. Please choose again.'
          END SELECT
      END DO

      CONTAINS

      SUBROUTINE AddBook(Books, BookCount)
          TYPE(Book), DIMENSION(:), INTENT(INOUT) :: Books
          INTEGER, INTENT(INOUT) :: BookCount

          IF (BookCount < MAX_BOOKS) THEN
              PRINT *, 'Enter Book Title:'
              READ *, Books(BookCount + 1)%Title
              PRINT *, 'Enter Author Name:'
              READ *, Books(BookCount + 1)%Author
              PRINT *, 'Enter Publication Year:'
              READ *, Books(BookCount + 1)%Year
              Books(BookCount + 1)%Available = .TRUE.
              BookCount = BookCount + 1
          ELSE
              PRINT *, 'Book limit reached.'
          END IF
      END SUBROUTINE AddBook

      SUBROUTINE DisplayBooks(Books, BookCount)
          TYPE(Book), DIMENSION(:), INTENT(IN) :: Books
          INTEGER, INTENT(IN) :: BookCount
          INTEGER :: I

          PRINT *, 'Available Books:'
          DO I = 1, BookCount
              IF (Books(I)%Available) THEN
                  PRINT *, 'Title: ', Books(I)%Title, ', Author: ', Books(I)%Author, ', Year: ', Books(I)%Year
              END IF
          END DO
      END SUBROUTINE DisplayBooks

      SUBROUTINE SearchBook(Books, BookCount)
          TYPE(Book), DIMENSION(:), INTENT(IN) :: Books
          INTEGER, INTENT(IN) :: BookCount
          CHARACTER(LEN=30) :: SearchTitle
          INTEGER :: I, Found

          PRINT *, 'Enter the title of the book to search:'
          READ *, SearchTitle
          Found = 0

          DO I = 1, BookCount
              IF (TRIM(Books(I)%Title) == TRIM(SearchTitle)) THEN
                  PRINT *, 'Book Found: Title: ', Books(I)%Title, ', Author: ', Books(I)%Author, ', Year: ', Books(I)%Year
                  Found = 1
              END IF
          END DO

          IF (Found == 0) THEN
              PRINT *, '
              PRINT *, 'Book not found.'
          END IF
      END SUBROUTINE SearchBook

      END PROGRAM LibraryManagementSystem
