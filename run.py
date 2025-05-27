import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

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
summary_sheet = SHEET.worksheet('summary')


def calculate_age_months(dob_str):
    dob = datetime.strptime(dob_str, '%Y-%m-%d')
    today = datetime.today()
    age_months = (today.year - dob.year) * 12 + (today.month - dob.month)
    return age_months


def is_username_taken(username):
    all_usernames = user_info.col_values(1)
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
    print("✅ User added successfully!")


def log_daily_baby_data(username):
    print("\n--- Log Daily Baby Data ---")

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


def update_log_date(username):
    print("\n--- Update Daily Log Date ---")

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

    for i, row in enumerate(records[1:], start=2):
        if row[0] == username and row[1] == old_date:
            daily_logs.update_cell(i, 2, new_date)
            updated = True
            print(f"✅ Updated date from {old_date} to {new_date} in row {i}.")
            break

    if not updated:
        print("❌ No matching record found.")


def log_growth_data(username):
    print("\n--- Log Growth Data ---")

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


def log_milestones(username):
    print("\n--- Log Baby Milestone ---")

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


def update_summary():
    print("\n--- Updating summary sheet ---")

    summary_sheet.clear()

    headers = ["Username", "Total Sleep This Week", "Average Feed (ml)",
               "Milestones Achieved", "Notes", "Latest Weight",
               "Latest Height"]
    summary_sheet.append_row(headers)

    today = datetime.today()
    week_ago = today - timedelta(days=7)

    user_rows = user_info.get_all_values()[1:]
    daily_rows = daily_logs.get_all_values()[1:]
    milestone_rows = milestones.get_all_values()[1:]
    growth_rows = growth.get_all_values()[1:]

    for user_row in user_rows:
        username = user_row[0]

        sleep_sum = 0
        feed_values = []
        for d_row in daily_rows:
            if d_row[0] == username:
                try:
                    log_date = datetime.strptime(d_row[1], "%Y-%m-%d")
                except ValueError:
                    continue
                if log_date >= week_ago:
                    sleep_sum += float(d_row[2])
                    feed_values.append(float(d_row[3]))

        avg_feed = round(sum(feed_values)
                         / len(feed_values), 2) if feed_values else 0

        user_milestones = set()
        for m in milestone_rows:
            if m[0] == username:
                milestone_text = m[2].strip().lower()
                if milestone_text and "none" not in milestone_text:
                    user_milestones.add(milestone_text)

        milestones_count = len(user_milestones)
        notes = ""

        user_growth = [g for g in growth_rows if g[0] == username]
        latest_weight = ""
        latest_height = ""

        if user_growth:
            user_growth.sort(key=lambda x:
                             datetime.strptime(x[1], "%Y-%m-%d"), reverse=True)
            latest_weight = user_growth[0][2]
            latest_height = user_growth[0][3]

        new_summary_row = [username, sleep_sum, avg_feed, milestones_count,
                           notes, latest_weight, latest_height]
        summary_sheet.append_row(new_summary_row)

    print("✅ Summary sheet updated!")


def main():
    print("👶 Welcome to Simple Baby Tracker!\n")

    is_new = input("Are you a new user? (yes/no): ").strip().lower()

    if is_new == "yes":
        add_new_user()
        return

    elif is_new == "no":
        username = input("Enter your username: ").strip()

        if not is_username_taken(username):
            print("❌ Username not found. Please register first.")
            return

        stored_users = user_info.get_all_values()
        stored_password = None
        for row in stored_users:
            if row[0] == username:
                stored_password = row[1]
                break

        password = input("Enter your password: ").strip()
        if password != stored_password:
            print("❌ Incorrect password.")
            return

        print(f"\n✅ Welcome back, {username}!")

        while True:
            print("\nChoose an option:")
            print("1. Log Daily Baby Data")
            print("2. Update Daily Log Date")
            print("3. Log Growth Data")
            print("4. Log Milestones")
            print("5. Update Summary Sheet")
            print("6. Quit")

            choice = input("Enter 1–6: ").strip()

            if choice == '1':
                log_daily_baby_data(username)
            elif choice == '2':
                update_log_date(username)
            elif choice == '3':
                log_growth_data(username)
            elif choice == '4':
                log_milestones(username)
            elif choice == '5':
                update_summary()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("Invalid option. Please enter a number between 1 and 6.")
    else:
        print("❗ Please type 'yes' or 'no'.")


if __name__ == "__main__":
    main()
