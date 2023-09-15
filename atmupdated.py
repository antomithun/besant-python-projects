import mysql.connector
import time as t
from decimal import Decimal

# Connect to the MySQL database
atmupdated = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="atm_db"  # Specify your default database name here
)

cursor = atmupdated.cursor()

# Create a table to store user accounts if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_number VARCHAR(255) PRIMARY KEY,
        pin INT,
        balance DECIMAL(10, 2),
        name VARCHAR(255)
    )
''')

atmupdated.commit()

def create_account(account_number, pin, name, initial_balance=0.0):
    try:
        cursor.execute('INSERT INTO accounts (account_number, pin, balance, name) VALUES (%s, %s, %s, %s)', (account_number, pin, initial_balance, name))
        atmupdated.commit()
        print("Account created successfully!")
    except mysql.connector.Error as err:
        print(f"Error creating account: {err}")

# Call the create_account function to create a new account
create_account('8546549754', 6383, 'anto mithun', 10000.00)

def get_account(account_number):
    try:
        cursor.execute('SELECT * FROM accounts WHERE account_number = %s', (account_number,))
        account = cursor.fetchone()
        if account:
            print(f"Account found: {account}")
        else:
            print(f"Account not found for account number: {account_number}")
        return account
    except mysql.connector.Error as err:
        print(f"Error retrieving account: {err}")


def update_balance(account_number, amount):
    """
    Update the balance of an account.
    """
    try:
        cursor.execute('UPDATE accounts SET balance = balance + %s WHERE account_number = %s', (amount, account_number))
        atmupdated.commit()
    except mysql.connector.Error as err:
        print(f"Error updating balance: {err}")

def delete_account(account_number):
    """
    Delete an account based on the account number.
    """
    try:
        cursor.execute('DELETE FROM accounts WHERE account_number = %s', (account_number,))
        atmupdated.commit()
    except mysql.connector.Error as err:
        print(f"Error deleting account: {err}")

# Welcome message for ATM users
def welcome_message(username, user_balance):
    """
    Display a welcome message for the user.
    """
    print(f"Welcome, {username}!")
    print(f"Your account balance: Rs. {user_balance:.2f}\n")

# ATM functions
def view_balance(username, user_balance):
    """
    Display the account balance.
    """
    print(f"Account Holder: {username}")
    print(f"Account Balance: Rs. {user_balance:.2f}\n")

def withdraw_cash(account_number, username, user_balance):
    """
    Withdraw cash from the account.
    """
    while True:
        try:
            withdraw_amt = Decimal(input("Enter the amount you wish to withdraw: Rs. "))
            if withdraw_amt > user_balance:
                print("Insufficient balance. Please enter a lower amount.")
            else:
                confirm = input(f"Confirm withdrawal of Rs. {withdraw_amt}? (Y/N): ")
                if confirm.lower() == 'y':
                    update_balance(account_number, -withdraw_amt)
                    user_balance -= withdraw_amt
                    print(f"Withdrew Rs. {withdraw_amt}")
                    welcome_message(username, user_balance)
                    break
                else:
                    print("Withdrawal canceled.")
                    break
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

def deposit_cash(account_number, username, user_balance):
    """
    Deposit cash into the account.
    """
    while True:
        try:
            deposit_amt = Decimal(input("Enter the amount you wish to deposit: Rs. "))
            if deposit_amt <= 0:
                print("Invalid deposit amount. Please enter a positive amount.")
            else:
                confirm = input(f"Confirm deposit of Rs. {deposit_amt}? (Y/N): ")
                if confirm.lower() == 'y':
                    update_balance(account_number, deposit_amt)
                    user_balance += deposit_amt
                    print(f"Deposited Rs. {deposit_amt}")
                    welcome_message(username, user_balance)
                    break
                else:
                    print("Deposit canceled.")
                    break
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

def change_pin(account_number):
    """
    Change the PIN of the account.
    """
    while True:
        try:
            new_pin = int(input("Enter your new 4-digit PIN: "))
            if 1000 <= new_pin <= 9999:
                confirm = input(f"Confirm changing PIN to {new_pin} (YES/NO): ")
                if confirm.lower() == 'y':
                    cursor.execute('UPDATE accounts SET pin = %s WHERE account_number = %s', (new_pin, account_number))
                    atmupdated.commit()
                    print("PIN changed successfully!")
                    break
                else:
                    print("PIN change canceled.")
                    break
            else:
                print("Invalid PIN. Please enter a 4-digit PIN.")
        except ValueError:
            print("Invalid input. Please enter a valid 4-digit PIN.")

def return_card():
    """
    Return the ATM card.
    """
    print("Returning your ATM Card...")
    t.sleep(1)
    print("Card returned successfully!\n")

# ATM user information
account_number = 8546549754  # Replace with the user's account number
user_pin = 6383  # Replace with the user's PIN

# Request the user to insert their ATM card
input("Please insert your ATM card and press Enter to continue...")

# Retrieve the user's account information
# Retrieve the user's account information
user_account = get_account(account_number)
if user_account:
    user_balance = Decimal(user_account[2])  # Extract the balance from the account data
    user_name = user_account[3]  # Extract the name from the account data

    while True:
        # Display the ATM menu
        print("\nATM display:")
        print("1. View Balance")
        print("2. Withdraw Cash")
        print("3. Deposit Cash")
        print("4. Change PIN")
        print("5. Return Card")
        print("0. Exit")
        
        preference = input("Enter your preference: ")

        if preference == '1':
            view_balance(user_name, user_balance)
        elif preference == '2':
            withdraw_cash(account_number, user_name, user_balance)
        elif preference == '3':
            deposit_cash(account_number, user_name, user_balance)
        elif preference == '4':
            change_pin(account_number)
        elif preference == '5':
            return_card()
            break
        elif preference == '0':
            print("Exiting ATM. Have a pleasant day!")
            break
        else:
            print("Invalid choice. Please try again.")
atmupdated.close()


