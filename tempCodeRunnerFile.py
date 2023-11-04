Account.isBankrupt = is_bankrupt
        status = "bankrupt" if is_bankrupt else "solvent"
        print(f"\n--> The bank is now {status}.")
