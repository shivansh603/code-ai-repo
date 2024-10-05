// Simple Recipe Manager

function recipeManager() {
    const recipeName = prompt("Enter the name of the recipe:");
    const numIngredients = parseInt(prompt("Enter the number of ingredients:"));
    const ingredients = [];

    for (let i = 0; i < numIngredients; i++) {
        let ingredient = prompt(`Enter ingredient ${i + 1}:`);
        ingredients.push(ingredient);
    }

    const instructions = prompt("Enter cooking instructions:");

    // Display the recipe
    console.log(`\nRecipe for: ${recipeName}`);
    console.log("Ingredients:");
    ingredients.forEach((ingredient) => {
        console.log(`- ${ingredient}`);
    });
    console.log(`Instructions: ${instructions}`);
}

// Run the recipe manager
recipeManager();
