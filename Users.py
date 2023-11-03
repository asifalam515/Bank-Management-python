import random
from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    transaction_history = {}

    def __init__(self, name, email, address, accountType):
        self.name = name
        self.email = email
        self.address = address
        self.accountType = accountType
        self.balance = 0
        self.accountNo = self.generate_account_number()
        self.loan_taken = 0
        self.loan_count = 0
        Account.accounts.append(self)

    def generate_account_number(self):
        
        return random.randint(100000, 999999)

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.add_to_transaction_history(f"Deposited ${amount}")
            print(f"\n--> Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Invalid deposit amount")

    def withdraw(self, amount):
        if amount >= 0 and amount <= self.balance:
            self.balance -= amount
            self.add_to_transaction_history(f"Withdrew ${amount}")
            print(f"\n--> Withdrew ${amount}. New balance: ${self.balance}")
        elif amount > self.balance:
            print("\n--> Withdrawal amount exceeded. Insufficient balance.")
        else:
            print("\n--> Invalid withdrawal amount")

    def check_balance(self):
        print(f"\n--> Available Balance: ${self.balance}")

    def check_transaction_history(self):
        print("\n--> Transaction History:")
        for transaction in Account.transaction_history.get(self.accountNo, []):
            print(transaction)

    def take_loan(self, amount):
        if self.loan_count < 2 and amount > 0:
            self.loan_taken += amount
            self.balance += amount
            self.loan_count += 1
            self.add_to_transaction_history(f"Loan Taken: ${amount}")
            print(f"\n--> Loan of ${amount} taken. New balance: ${self.balance}")
        else:
            print("\n--> Loan limit exceeded or invalid loan amount")

    def transfer_amount(self, recipient_account, amount):
        if recipient_account is None:
            print("\n--> Account does not exist. Transfer failed.")
        elif amount > 0 and amount <= self.balance:
            self.balance -= amount
            recipient_account.balance += amount
            self.add_to_transaction_history(f"Transferred ${amount} to {recipient_account.name}'s account")
            print(f"\n--> Transferred ${amount} to {recipient_account.name}'s account.")
        else:
            print("\n--> Invalid transfer amount or insufficient balance")

    def add_to_transaction_history(self, transaction):
        if self.accountNo in Account.transaction_history:
            Account.transaction_history[self.accountNo].append(transaction)
        else:
            Account.transaction_history[self.accountNo] = [transaction]

    @abstractmethod
    def show_info(self):
        pass


class SavingsAccount(Account):
    def __init__(self, name, email, address, interest_rate):
        super().__init__(name, email, address, "Savings")
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * (self.interest_rate / 100)
        self.deposit(interest)
        print("\n--> Interest is applied!")

    def show_info(self):
        print(f"Infos of {self.accountType} account of {self.name}:\n")
        print(f'\tAccount Type: {self.accountType}')
        print(f'\tName: {self.name}')
        print(f'\tAccount No: {self.accountNo}')
        print(f'\tEmail: {self.email}')
        print(f'\tAddress: {self.address}')
        print(f'\tCurrent Balance: ${self.balance}\n')



currentUser = None

while True:
    if currentUser is None:
        print("\n--> No user logged in!")
        ch = input("\n--> Register/Login (R/L) : ")
        if ch == "R":
            name = input("Name:")
            email = input("Email:")
            address = input("Address:")
            a = input("Savings Account or Current Account (sv/cu): ")
            if a == "sv":
                ir = float(input("Interest rate:"))
                currentUser = SavingsAccount(name, email, address, ir)
            # Additional logic for CurrentAccount if needed...
        else:
            no = int(input("Account Number:"))
            for account in Account.accounts:
                if account.accountNo == no:
                    currentUser = account
                    break
    else:
        print(f"\nWelcome {currentUser.name},Account No:{currentUser.accountNo} !\n")

        print("1. Withdraw")
        print("2. Deposit")
        print("3. Show Info")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Take Loan")
        print("7. Transfer Amount")
        print("8. Logout\n")

        op = int(input("Choose Option:"))

        if op == 1:
            amount = int(input("Enter withdraw amount:"))
            currentUser.withdraw(amount)

        elif op == 2:
            amount = int(input("Enter deposit amount:"))
            currentUser.deposit(amount)

        elif op == 3:
            currentUser.show_info()

        elif op == 4:
            currentUser.check_balance()

        elif op == 5:
            currentUser.check_transaction_history()

        elif op == 6:
            amount = int(input("Enter loan amount:"))
            currentUser.take_loan(amount)

        elif op == 7:
            recipient_account_no = int(input("Enter recipient's account number:"))
            recipient_account = next((acc for acc in Account.accounts if acc.accountNo == recipient_account_no), None)
            transfer_amount = int(input("Enter transfer amount:"))
            currentUser.transfer_amount(recipient_account, transfer_amount)

        elif op == 8:
            currentUser = None

        else:
            print("Invalid Option")
