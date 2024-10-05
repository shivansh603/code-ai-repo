// Fitness Tracker

function fitnessTracker() {
    const calories = new Array(7);  // Array to store calories for 7 days
    let totalCalories = 0;

    console.log("Fitness Tracker");
    console.log("Log your calories burned for the week");

    for (let i = 0; i < 7; i++) {
        let validInput = false;

        while (!validInput) {
            let input = prompt(`Enter calories burned for day ${i + 1}:`);
            let caloriesBurned = parseFloat(input);

            if (isNaN(caloriesBurned) || caloriesBurned < 0) {
                console.log("Invalid input. Please enter a non-negative number.");
            } else {
                calories[i] = caloriesBurned;
                validInput = true;  // Valid input; exit the loop
            }
        }

        totalCalories += calories[i];
    }

    console.log(`Total calories burned this week: ${totalCalories}`);
    console.log(`Average calories burned per day: ${(totalCalories / 7).toFixed(2)}`);
}

// Run the fitness tracker
fitnessTracker();
