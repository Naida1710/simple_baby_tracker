import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('simple_baby_tracker')

user_info = SHEET.worksheet('user_info')
daily_logs = SHEET.worksheet('daily_logs')


def calculate_age_months(dob_str):
    dob = datetime.strptime(dob_str, '%Y-%m-%d')
    today = datetime.today()
    age_months = (today.year - dob.year) * 12 + (today.month - dob.month)
    return age_months


def is_username_taken(username):
    all_usernames = user_info.col_values(1)  # first column = Username
    return username in all_usernames


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


def main():
    # Optional: print current users
    print("Current users:")
    for row in user_info.get_all_values()[1:]:  # skip header row
        print(f"- {row[0]} (Baby: {row[2]})")

    add_new_user()


if __name__ == "__main__":
    main()