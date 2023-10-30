from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    account_counter = 1  # Used to generate automatic account numbers

    def __init__(self, name, email, address, account_type, password):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.password = password
        self.balance = 0
        self.accountNo = Account.account_counter
        Account.account_counter += 1
        self.transaction_history = []
        self.loans_taken = 0
        Account.accounts.append(self)

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
            print(f"\n--> Withdrew ${amount}. New balance: ${self.balance}")
        elif amount > self.balance:
            print("\n--> Withdrawal amount exceeded. Insufficient funds.")
        else:
            print("\n--> Invalid withdrawal amount")

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            print(f"\n--> Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Invalid deposit amount")

    def show_balance(self):
        print(f"\n--> Available Balance: ${self.balance}")

    def show_transaction_history(self):
        print(f"\n--> Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

    def request_loan(self, amount):
        if self.loans_taken < 2 and amount > 0:
            self.balance += amount
            self.loans_taken += 1
            self.transaction_history.append(f"Loan taken: ${amount}")
            print(f"\n--> Loan of ${amount} approved. New balance: ${self.balance}")
        else:
            print("\n--> Loan request rejected. Maximum two loans allowed or invalid loan amount.")

    def transfer(self, recipient_account, amount):
        if recipient_account in Account.accounts:
            if amount > 0 and amount <= self.balance:
                self.balance -= amount
                recipient_account.balance += amount
                self.transaction_history.append(f"Transferred ${amount} to account {recipient_account.accountNo}")
                print(f"\n--> Transferred ${amount} to account {recipient_account.accountNo}. New balance: ${self.balance}")
            else:
                print("\n--> Invalid transfer amount or insufficient funds.")
        else:
            print("\n--> Account does not exist.")

    @abstractmethod
    def show_info(self):
        pass

class SavingsAccount(Account):
    def __init__(self, name, email, address, password, interest_rate):
        super().__init__(name, email, address, "savings", password)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * (self.interest_rate / 100)
        self.deposit(interest)
        print("\n--> Interest applied!")

    def show_info(self):
        print(f"Infos of {self.account_type} account of {self.name}:\n")
        print(f'\tAccount Type : {self.account_type}')
        print(f'\tName : {self.name}')
        print(f'\tEmail : {self.email}')
        print(f'\tAccount No : {self.accountNo}')
        print(f'\tCurrent Balance : {self.balance}\n')

class CurrentAccount(Account):
    def __init__(self, name, email, address, password, overdraft_limit):
        super().__init__(name, email, address, "current", password)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and (self.balance - amount) >= -self.overdraft_limit:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
            print(f"\n--> Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Invalid withdrawal amount or overdraft limit reached")

    def show_info(self):
        print(f"Infos of {self.account_type} account of {self.name}:\n")
        print(f'\tAccount Type : {self.account_type}')
        print(f'\tName : {self.name}')
        print(f'\tEmail : {self.email}')
        print(f'\tAccount No : {self.accountNo}')
        print(f'\tCurrent Balance : {self.balance}\n')

# Main program
currentUser = None

while True:
    if currentUser is None:
        print("\n--> No user logged in !")
        ch = input("\n--> Register/Login (R/L) : ")
        if ch == "R":
            name = input("Name:")
            email = input("Email:")
            address = input("Address:")
            password = input("Password:")
            account_type = input("Account Type (savings/current): ")
            if account_type == "savings":
                ir = float(input("Interest rate:"))
                currentUser = SavingsAccount(name, email, address, password, ir)
            elif account_type == "current":
                lm = float(input("Overdraft Limit:"))
                currentUser = CurrentAccount(name, email, address, password, lm)
            else:
                print("Invalid account type")
        elif ch == "L":
            acc_no = int(input("Account Number:"))
            for account in Account.accounts:
                if account.accountNo == acc_no:
                    currentUser = account
                    break
    else:
        print(f"\nWelcome {currentUser.name} !\n")
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Show Balance")
        print("4. Show Transaction History")
        print("5. Request Loan")
        print("6. Transfer Money")
        print("7. Logout\n")

        op = int(input("Choose Option:"))

        if op == 1:
            amount = float(input("Enter withdrawal amount:"))
            currentUser.withdraw(amount)
        elif op == 2:
            amount = float(input("Enter deposit amount:"))
            currentUser.deposit(amount)
        elif op == 3:
            currentUser.show_balance()
        elif op == 4:
            currentUser.show_transaction_history()
        elif op == 5:
            amount = float(input("Enter loan amount:"))
            currentUser.request_loan(amount)
        elif op == 6:
            recipient_acc_no = int(input("Enter recipient's account number:"))
            recipient_account = next((acc for acc in Account.accounts if acc.accountNo == recipient_acc_no), None)
            if recipient_account:
                amount = float(input("Enter transfer amount:"))
                currentUser.transfer(recipient_account, amount)
            else:
                print("\n--> Recipient account does not exist.")
        elif op == 7:
            currentUser = None
        else:
            print("Invalid Option")
