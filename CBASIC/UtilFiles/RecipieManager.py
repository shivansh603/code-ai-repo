# Simple Recipe Manager

def recipe_manager():
    recipe_name = input("Enter the name of the recipe: ")
    num_ingredients = int(input("Enter the number of ingredients: "))
    ingredients = []

    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i + 1}: ")
        ingredients.append(ingredient)

    instructions = input("Enter cooking instructions: ")

    # Display the recipe
    print(f"\nRecipe for: {recipe_name}")
    print("Ingredients:")
    for ingredient in ingredients:
        print(f"- {ingredient}")
    
    print(f"Instructions: {instructions}")

# Run the recipe manager
recipe_manager()
