import pymysql
from hashlib import sha256

# Establishing a database connection
connection = pymysql.connect(
    host='localhost',
    user='UNAME',
    password='PASSWD',
    database='DB_NAME'
)

# User registration
def register_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    with connection.cursor() as cursor:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (username, hashed_password))
        connection.commit()

# User login
def login_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    with connection.cursor() as cursor:
        sql = "SELECT id FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, hashed_password))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

# Create account
def create_account(user_id):
    with connection.cursor() as cursor:
        sql = "INSERT INTO accounts (user_id) VALUES (%s)"
        cursor.execute(sql, (user_id,))
        connection.commit()

        account_id = cursor.lastrowid
        return account_id

# Make a transaction
def make_transaction(account_id, amount):
    with connection.cursor() as cursor:
        check_balance_sql = "SELECT balance FROM accounts WHERE id = %s"
        cursor.execute(check_balance_sql, (account_id,))
        balance_result = cursor.fetchone()

        if balance_result is None:
            print("Account not found.")
            return False
        
        balance = balance_result[0]
        
        if balance >= amount:
            update_balance_sql = "UPDATE accounts SET balance = balance - %s WHERE id = %s"
            cursor.execute(update_balance_sql, (amount, account_id))
            connection.commit()
            return True
        else:
            print("Insufficient balance.")
            return False
        
def view_balance(account_id):
    with connection.cursor() as cursor:
        sql = "SELECT balance FROM accounts WHERE id = %s"
        cursor.execute(sql, (account_id,))
        balance_result = cursor.fetchone()

        if balance_result is None:
            print("Account not found.")
        else:
            balance = balance_result[0]
            print(f"Account Balance: ${balance:.2f}")

# Deposit money
def deposit_money(account_id, amount):
    with connection.cursor() as cursor:
        update_balance_sql = "UPDATE accounts SET balance = balance + %s WHERE id = %s"
        cursor.execute(update_balance_sql, (amount, account_id))
        connection.commit()

if __name__ == "__main__":
    print("Banking system initialized.")

    while True:
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
            print("User registered successfully.")

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id = login_user(username, password)
            if user_id:
                print("Login successful.")
                while True:
                    print("1. Create Account\n2. Make Transaction\n3. Deposit Money\n4. View Balance\n5. Logout.")
                    user_option = input("Enter your choice: ")

                    if user_option == "1":
                        create_account(user_id)
                        print('WELCOME TO THE BANK!')

                    elif user_option == "2":
                        account_id = int(input("Enter account ID: "))
                        amount = float(input("Enter transaction amount: "))
                        if make_transaction(account_id, amount):
                            print("Transaction successful.")
                        else:
                            print("Transaction failed.")

                    elif user_option == "3":
                        account_id = int(input("Enter account ID: "))
                        amount = float(input("Enter deposit amount: "))
                        deposit_money(account_id, amount)
                        print("Deposit successful.")

                    elif user_option == "4":
                        account_id = int(input("Enter account ID: "))
                        view_balance(account_id)
                    elif user_option == "5":
                        break

            else:
                print("Invalid username or password.")

        elif choice == "3":
            connection.close()
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please select a valid option.")
