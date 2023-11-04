     if recipient_account:
            if amount > 0 and amount <= self.balance:
                self.balance -= amount
                recipient_account.balance += amount
                self.add_to_transaction_history(f"Transferred ${amount} to {recipient_account.name}'s account")
                print(f"\n--> Transferred ${amount} to {recipient_account.name}'s account.")
            else:
                print("\n--> Invalid transfer amount or insufficient balance")
        else:
            print("\n--> Recipient account does not exist. Transfer failed.")