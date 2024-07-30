class ATM:
    def __init__(self):
        self.balance = 0.0
        self.pin = None

    def check_balance(self):
        print(f"Your current balance is: ${self.balance:.2f}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"${amount:.2f} has been deposited to your account")
        else:
            print("Invalid amount. Please enter a positive number")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount. Please enter a positive number")
        elif amount > self.balance:
            print("Insufficient funds. Transaction declined")
        else:
            self.balance -= amount
            print(f"${amount:.2f} has been withdrawn from your account")

    def set_pin(self, new_pin):
        if len(new_pin) == 4 and new_pin.isdigit():
            self.pin = new_pin
            print("Your PIN has been set/updated successfully")
        else:
            print("Invalid PIN. Please enter a 4-digit number")

    def validate_pin(self):
        if self.pin is None:
            print("No PIN set. Please set a PIN first")
            return False

        enter_pin = input("Please enter your PIN: ")
        if enter_pin == self.pin:
            return True
        else:
            print("Invalid PIN. Access denied")
            return False
        

def validate_number():
    while True:
        try:
            number = int(input("Please enter a number between 1 and 100: "))
            if 1 <= number <= 100:
                return True
            else:
                print("Invalid number. Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number between 1 and 100.")


def main():
    atm = ATM()

    while True:
        print("\nATM System")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Generate/Change PIN")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")


        if validate_number():
            if choice == '1':
                if atm.validate_pin():
                    atm.check_balance()
            elif choice == '2':
                if atm.validate_pin():
                    amount = float(input("Enter the amount to deposit: "))
                    atm.deposit(amount)
            elif choice == '3':
                if atm.validate_pin():
                    amount = float(input("Enter the amount to withdraw: "))
                    atm.withdraw(amount)
            elif choice == '4':
                new_pin = input("Enter a new 4-digit PIN: ")
                atm.set_pin(new_pin)
            elif choice == '5':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()










