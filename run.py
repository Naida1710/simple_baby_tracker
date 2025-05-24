import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Google Sheets credentials and setup
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('simple_baby_tracker')

user_info = SHEET.worksheet('user_info')
daily_logs = SHEET.worksheet('daily_logs')
growth = SHEET.worksheet('growth')


# --- Helper Functions ---
def calculate_age_months(dob_str):
    dob = datetime.strptime(dob_str, '%Y-%m-%d')
    today = datetime.today()
    age_months = (today.year - dob.year) * 12 + (today.month - dob.month)
    return age_months


def is_username_taken(username):
    all_usernames = user_info.col_values(1)  # first column = Username
    return username in all_usernames


# --- User Registration ---
def add_new_user():
    print("Add new user info:")

    while True:
        username = input("Username: ").strip()
        if is_username_taken(username):
            print("Username already taken. Please try another.")
        else:
            break

    password = input("Password: ").strip()
    baby_name = input("Baby Name: ").strip()
    baby_dob = input("Baby DOB (YYYY-MM-DD): ").strip()

    try:
        baby_age_months = calculate_age_months(baby_dob)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    birth_weight = input("Birth Weight (kg or lbs): ").strip()
    birth_height = input("Birth Height (cm or inches): ").strip()

    new_row = [username, password, baby_name, baby_dob,
               str(baby_age_months), birth_weight, birth_height]
    user_info.append_row(new_row)
    print("User added successfully!")


# --- Daily Log Entry ---
def log_daily_baby_data():
    print("\n--- Log Daily Baby Data ---")

    username = input("Enter your username: ").strip()
    if not is_username_taken(username):
        print("Username not found. Please register first.")
        return

    date = input("Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    try:
        sleep_hours = float(input("Sleep (hours): "))
        feed_ml = float(input("Feed (ml): "))
        wet_diapers = int(input("Wet Diapers: "))
        dirty_diapers = int(input("Dirty Diapers: "))
    except ValueError:
        print("Please enter numeric values.")
        return

    new_row = [username, date, sleep_hours,
               feed_ml, wet_diapers, dirty_diapers]
    daily_logs.append_row(new_row)
    print("✅ Daily log saved successfully!")


# --- Growth Log Entry ---
def log_growth_data():
    print("\n--- Log Growth Data ---")

    username = input("Enter your username: ").strip()
    if not is_username_taken(username):
        print("Username not found. Please register first.")
        return

    date = input("Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    try:
        weight = float(input("Weight (kg): "))
        height = float(input("Height (cm): "))
    except ValueError:
        print("Please enter numeric values for weight and height.")
        return

    new_row = [username, date, weight, height]
    growth.append_row(new_row)
    print("✅ Growth data saved successfully!")


def main():
    print("Welcome to Simple Baby Tracker")

    while True:
        print("\nChoose an option:")
        print("1. Register New User")
        print("2. Log Daily Baby Data")
        print("3. Quit")

        choice = input("Enter 1, 2, or 3: ").strip()

        if choice == '1':
            add_new_user()
        elif choice == '2':
            log_daily_baby_data()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
