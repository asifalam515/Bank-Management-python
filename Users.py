from abc import ABC, abstractmethod
import random

class Account(ABC):
    accounts = []
    transactions = []
    total_balance = 0
    total_loans = 0
    loan_feature_enabled = True

    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_no = random.randint(1000, 9999)  
        self.loans_taken = 0  
        Account.accounts.append(self)
        Account.total_balance += self.balance

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            Account.total_balance += amount
            self.transactions.append(f"Deposited ${amount}. New balance: ${self.balance}")
            print(f"\n--> Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Invalid deposit amount")

    @abstractmethod
    def withdraw(self, amount):
        pass

    def check_balance(self):
        print(f"\n--> Available balance: ${self.balance}")

    def check_transaction_history(self):
        print("\n--> Transaction History:")
        for transaction in self.transactions:
            print(transaction)

    def take_loan(self, amount):
        if self.loans_taken < 2:
            if Account.loan_feature_enabled:
                self.balance += amount
                Account.total_loans += amount
                self.loans_taken += 1
                self.transactions.append(f"Loan taken: ${amount}. New balance: ${self.balance}")
                print(f"\n--> Loan of ${amount} taken. New balance: ${self.balance}")
            else:
                print("\n--> Loan feature is currently disabled by the bank.")
        else:
            print("\n--> Maximum number of loans reached. Cannot take more loans.")

    def transfer_amount(self, recipient, amount):
        if recipient in Account.accounts:
            if amount >= 0 and amount <= self.balance:
                self.balance -= amount
                recipient.balance += amount
                self.transactions.append(f"Transferred ${amount} to {recipient.name}. New balance: ${self.balance}")
                print(f"\n--> Transferred ${amount} to {recipient.name}. New balance: ${self.balance}")
            elif amount > self.balance:
                print("\n--> Transfer amount exceeded. Insufficient funds.")
            else:
                print("\n--> Invalid transfer amount")
        else:
            print("\n--> Account does not exist. Transfer failed.")

    @abstractmethod
    def show_info(self):
        pass

class SavingsAccount(Account):
    def __init__(self, name, email, address, interest_rate):
        super().__init__(name, email, address, "savings")
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * (self.interest_rate / 100)
        self.deposit(interest)
        print("\n--> Interest applied!")

    def withdraw(self, amount):
        if amount > 0 and (self.balance - amount) >= 0:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount}. New balance: ${self.balance}")
            print(f"\n--> Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Invalid withdrawal amount or insufficient funds.")

    def show_info(self):
        print(f"\nInfos of {self.account_type} account of {self.name}:\n")
        print(f"\tAccount Type: {self.account_type}")
        print(f"\tName: {self.name}")
        print(f"\tAccount No: {self.account_no}")
        print(f"\tCurrent Balance: ${self.balance}\n")

class CurrentAccount(Account):
    def __init__(self, name, email, address, overdraft_limit):
        super().__init__(name, email, address, "current")
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and (self.balance - amount) >= -self.overdraft_limit:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount}. New balance: ${self.balance}")
            print(f"\n--> Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Invalid withdrawal amount or overdraft limit reached")

    def show_info(self):
        print(f"\nInfos of {self.account_type} account of {self.name}:\n")
        print(f"\tAccount Type: {self.account_type}")
        print(f"\tName: {self.name}")
        print(f"\tAccount No: {self.account_no}")
        print(f"\tCurrent Balance: ${self.balance}\n")

class Admin:
    def create_account(self,name, email, address, account_type, interest_rate=None, overdraft_limit=None):
        if account_type == "savings":
            return SavingsAccount(name, email, address, interest_rate)
        elif account_type == "current":
            return CurrentAccount(name, email, address, overdraft_limit)
        else:
            print("Invalid account type. Please choose 'savings' or 'current'.")

    def delete_account(self,account):
        if account in Account.accounts:
            Account.accounts.remove(account)
            Account.total_balance -= account.balance
            print("\n--> Account deleted successfully.")
        else:
            print("\n--> Account not found.")

    def view_all_accounts(self):
        print("\n--> All User Accounts:")
        for account in Account.accounts:
            print(f"Account No: {account.account_no}, Name: {account.name}, Balance: ${account.balance}")

    def check_total_balance(self):
        print(f"\n--> Total Available Balance in the Bank: ${Account.total_balance}")

    def check_total_loans(self):
        print(f"\n--> Total Loan Amount in the Bank: ${Account.total_loans}")

    def toggle_loan_feature(self,enable):
        Account.loan_feature_enabled = enable
        status = "enabled" if enable else "disabled"
        print(f"\n--> Loan feature {status} by the bank.")


# Main program

current_user = None
admin = Admin()

while True:
    
    
    print("\n===================================")
    print("1. User Operations")
    print("2. Admin Operations")
    print("3. Exit")
    print("===================================")
    choice = int(input("Choose Option: "))
    
    

    if choice == 1:  # User Operations
        if current_user is None:
            print("\n--> No user logged in!")
            action = input("\n--> Register/Login (R/L): ")

            if action == "R":
                name = input("Name: ")
                email = input("Email: ")
                address = input("Address: ")
                account_type = input("Account Type (savings/current): ")

                if account_type == "savings":
                    ir = float(input("Interest rate: "))
                    current_user = SavingsAccount(name, email, address, ir)
                    print(f"Savings Account Created  {current_user.name} Account No:{current_user.account_no}\n")
                    
                elif account_type == "current":
                    od_limit = float(input("Overdraft Limit: "))
                    current_user = CurrentAccount(name, email, address, od_limit)
                else:
                    print("Invalid account type. Please choose 'savings' or 'current'.")
                    continue
        # print(f"Account Created  {current_user.name} Account No:{current_user.account_no}\n")
            
            elif action == "L":
                account_no = int(input("Account Number: "))
                for account in Account.accounts:
                    if account.account_no == account_no:
                        current_user = account
                        break

        else:  # User is logged in
            print(f"\nWelcome {current_user.name} Account No:{current_user.account_no}\n")
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Check Balance")
            print("4. Transaction History")
            print("5. Take Loan")
            print("6. Transfer Amount")
            print("7. Show Info")
            print("8. Logout\n")

            option = int(input("Choose Option: "))

            if option == 1:
                amount = float(input("Enter withdraw amount: "))
                current_user.withdraw(amount)

            elif option == 2:
                amount = float(input("Enter deposit amount: "))
                current_user.deposit(amount)

            elif option == 3:
                current_user.check_balance()

            elif option == 4:
                current_user.check_transaction_history()

            elif option == 5:
                loan_amount = float(input("Enter loan amount: "))
                current_user.take_loan(loan_amount)

            elif option == 6:
                recipient_account_no = int(input("Enter recipient's account number: "))
                recipient = None
                for account in Account.accounts:
                    if account.account_no == recipient_account_no:
                        recipient = account
                        break
                current_user.transfer_amount(recipient, float(input("Enter transfer amount: ")))

            elif option == 7:
                current_user.show_info()

            elif option == 8:
                current_user = None

            else:
                print("Invalid Option")

    elif choice == 2:  # Admin Operations
        print("\n1. Create Account")
        print("2. Delete Account")
        print("3. View All Accounts")
        print("4. Check Total Balance")
        print("5. Check Total Loans")
        print("6. Toggle Loan Feature")
        print("7. Back to Main Menu")

        admin_option = int(input("Choose Admin Option: "))

        if admin_option == 1:
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            account_type = input("Account Type (savings/current): ")

            if account_type == "savings":
                ir = float(input("Interest rate: "))
                admin.create_account(name, email, address, account_type, interest_rate=ir)
            elif account_type == "current":
                od_limit = float(input("Overdraft Limit: "))
                admin.create_account(name, email, address, account_type, overdraft_limit=od_limit)
            else:
                print("Invalid account type. Please choose 'savings' or 'current'.")

        elif admin_option == 2:
            account_no = int(input("Enter account number to delete: "))
            account_to_delete = None
            for account in Account.accounts:
                if account.account_no == account_no:
                    account_to_delete = account
                    break
            admin.delete_account(account_to_delete)

        elif admin_option == 3:
            admin.view_all_accounts()

        elif admin_option == 4:
            admin.check_total_balance()

        elif admin_option == 5:
            admin.check_total_loans()

        elif admin_option == 6:
            enable_loan = input("Enable or disable loan feature? (enable/disable): ").lower()
            if enable_loan == "enable":
                admin.toggle_loan_feature(True)
            elif enable_loan == "disable":
                admin.toggle_loan_feature(False)
            else:
                print("Invalid option. Please enter 'enable' or 'disable'.")

        elif admin_option == 7:
            continue

    elif choice == 3:
        print("Exiting the program. Goodbye!")
        break

    else:
        print("Invalid Choice. Please choose a valid option.")
