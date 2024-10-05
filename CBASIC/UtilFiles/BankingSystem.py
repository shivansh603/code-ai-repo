# Simple Banking System

def banking_system():
    balance = 1000  # Initial balance
    print("Welcome to the Banking System")

    while True:
        print(f"Current Balance: {balance}")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            amount = float(input("Enter deposit amount: "))
            if amount > 0:
                balance += amount
                print(f"Deposited: {amount}")
            else:
                print("Invalid amount.")
        
        elif choice == 2:
            amount = float(input("Enter withdrawal amount: "))
            if amount > 0 and amount <= balance:
                balance -= amount
                print(f"Withdrawn: {amount}")
            else:
                print("Invalid amount or insufficient funds.")
        
        elif choice == 3:
            print("Thank you for using the Banking System.")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Run the banking system
banking_system()
