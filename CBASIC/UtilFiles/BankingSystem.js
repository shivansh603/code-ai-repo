// Simple Banking System

function bankingSystem() {
    let balance = 1000;  // Initial balance
    console.log("Welcome to the Banking System");

    while (true) {
        console.log(`Current Balance: ${balance}`);
        console.log("1. Deposit");
        console.log("2. Withdraw");
        console.log("3. Exit");

        let choice = parseInt(prompt("Enter your choice: "), 10);

        if (choice === 1) {
            let amount = parseFloat(prompt("Enter deposit amount: "));
            if (amount > 0) {
                balance += amount;
                console.log(`Deposited: ${amount}`);
            } else {
                console.log("Invalid amount.");
            }
        } else if (choice === 2) {
            let amount = parseFloat(prompt("Enter withdrawal amount: "));
            if (amount > 0 && amount <= balance) {
                balance -= amount;
                console.log(`Withdrawn: ${amount}`);
            } else {
                console.log("Invalid amount or insufficient funds.");
            }
        } else if (choice === 3) {
            console.log("Thank you for using the Banking System.");
            break;
        } else {
            console.log("Invalid choice. Please try again.");
        }
    }
}

// Run the banking system
bankingSystem();
