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
milestones = SHEET.worksheet('milestones')


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


# --- Update Daily Log Date ---
def update_log_date():
    print("\n--- Update Daily Log Date ---")

    username = input("Enter your username: ").strip()
    if not is_username_taken(username):
        print("Username not found.")
        return

    old_date = input("Enter the incorrect date (YYYY-MM-DD): ").strip()
    new_date = input("Enter the correct date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(old_date, "%Y-%m-%d")
        datetime.strptime(new_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    records = daily_logs.get_all_values()
    updated = False

    for i, row in enumerate(records[1:], start=2):  # skip header
        if row[0] == username and row[1] == old_date:
            daily_logs.update_cell(i, 2, new_date)
            updated = True
            print(f"✅ Updated date from {old_date} to {new_date} in row {i}.")
            break

    if not updated:
        print("❌ No matching record found.")


# --- Growth Entry ---
def log_growth_data():
    print("\n--- Log Growth Data ---")

    username = input("Enter your username: ").strip()
    if not is_username_taken(username):
        print("Username not found.")
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
        print("Please enter numeric values.")
        return

    new_row = [username, date, weight, height]
    growth.append_row(new_row)
    print("✅ Growth data logged successfully!")


# --- Milestone Entry ---
def log_milestones():
    print("\n--- Log Baby Milestone ---")

    username = input("Enter your username: ").strip()
    if not is_username_taken(username):
        print("Username not found.")
        return

    date = input("Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    milestone = input("Describe the milestone: ").strip()

    new_row = [username, date, milestone]
    milestones.append_row(new_row)
    print("🎉 Milestone logged successfully!")


# --- Main Menu ---
def main():
    print("Welcome to Simple Baby Tracker")

    while True:
        print("\nChoose an option:")
        print("1. Register New User")
        print("2. Log Daily Baby Data")
        print("3. Update Daily Log Date")
        print("4. Log Growth Data")
        print("5. Log Milestones")
        print("6. Quit")

        choice = input("Enter 1–6: ").strip()

        if choice == '1':
            add_new_user()
        elif choice == '2':
            log_daily_baby_data()
        elif choice == '3':
            update_log_date()
        elif choice == '4':
            log_growth_data()
        elif choice == '5':
            log_milestones()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
