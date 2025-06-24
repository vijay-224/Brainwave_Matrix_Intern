class ATM:
    def __init__(self):
        self.users = {
            '12345678': {'pin': '1234', 'balance': 1000, 'history': []},
            '87654321': {'pin': '4321', 'balance': 2000, 'history': []},
            '99635792': {'pin': '2242', 'balance': 3000, 'history': []}
        }
        self.current_user = None

    def login(self):
        print("----- Welcome to the ATM -----")
        attempts = 0
        while attempts < 3:
            card = input("Enter your card number: ").strip()
            pin = input("Enter your PIN: ").strip()
            if card in self.users and self.users[card]['pin'] == pin:
                print("Login successful!\n")
                self.current_user = card
                self.menu()
                return
            else:
                attempts += 1
                print(f"Invalid card or PIN. Attempts left: {3 - attempts}\n")

        print("Too many failed attempts. Exiting.")

    def menu(self):
        while True:
            print("\n--- Main Menu ---")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transaction History")
            print("5. Exit")

            choice = input("Choose an option (1-5): ")

            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                self.show_history()
            elif choice == '5':
                print("Thank you for using the ATM.")
                print("Have A nice day,come again. Bye!")
                break
            else:
                print("Invalid option. Please try again.")

    def check_balance(self):
        balance = self.users[self.current_user]['balance']
        print(f"Your current balance is: ₹{balance}")

    def deposit(self):
        try:
            amount = float(input("Enter amount to deposit: ₹"))
            if amount > 0:
                self.users[self.current_user]['balance'] += amount
                self.users[self.current_user]['history'].append(f"Deposited ₹{amount}")
                print(f"₹{amount} deposited successfully.")
                self.check_balance()
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def withdraw(self):
        try:
            amount = float(input("Enter amount to withdraw: ₹"))
            if 0 < amount <= self.users[self.current_user]['balance']:
                self.users[self.current_user]['balance'] -= amount
                self.users[self.current_user]['history'].append(f"Withdrew ₹{amount}")
                print(f"₹{amount} withdrawn successfully.")
                self.check_balance()
            else:
                print("Insufficient balance or invalid amount.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def show_history(self):
        print("\n--- Transaction History ---")
        history = self.users[self.current_user]['history']
        if history:
            for h in history:
                print("-", h)
        else:
            print("No transactions yet.")

# Run the ATM
if __name__ == "__main__":
    atm = ATM()
    atm.login()
