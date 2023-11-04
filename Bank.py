from Users import Account
class Bank:
    def __init__(self) -> None:
        self.total_balance = 0
        self.total_loan = 0
        self.loan_status = False
        self.accounts_list = []
    def create_account(self, account_no):
        new_account = Account(account_no)
        self.accounts_list.append(new_account)
        print(f"Account {account_no} created successfully.")
        
    def delete_account(self, account_no):
      for account in self.accounts_list:
          if account.account_no == account_no:
              self.accounts_list.remove(account)
              print(f"Account {account_no} deleted successfully.")
              return
      print(f"Account {Account.acco} not found.")