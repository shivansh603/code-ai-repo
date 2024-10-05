# Fitness Tracker

def fitness_tracker():
    calories = [0] * 7  # Array to store calories for 7 days
    total_calories = 0

    print("Fitness Tracker")
    print("Log your calories burned for the week")

    for i in range(7):
        while True:
            try:
                calories[i] = float(input(f"Enter calories burned for day {i + 1}: "))
                if calories[i] < 0:
                    print("Invalid input. Please enter a non-negative number.")
                else:
                    break  # Valid input; exit the loop
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        total_calories += calories[i]

    print(f"Total calories burned this week: {total_calories}")
    print(f"Average calories burned per day: {total_calories / 7:.2f}")

# Run the fitness tracker
fitness_tracker()
