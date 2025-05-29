import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import sys

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
growth = SHEET.worksheet('growth')
milestones = SHEET.worksheet('milestones')
summary_sheet = SHEET.worksheet('summary')


def user_input(prompt, allow_back=True, allow_quit=True):
    suffix = ""
    if allow_quit:
        suffix += " (or type 'q' to quit"
        if allow_back:
            suffix += ", 'b' to go back): "
        else:
            suffix += "): "
    else:
        if allow_back:
            suffix += " (or type 'b' to go back): "
        else:
            suffix += ": "
    response = input(prompt.rstrip(": ") + suffix).strip()
    if allow_quit and response.lower() in ['q', 'quit', 'exit']:
        print("Exiting the program. Goodbye!")
        sys.exit()
    if allow_back and response.lower() == 'b':
        return 'b'
    return response


def calculate_age_months(dob_str):
    dob = datetime.strptime(dob_str, '%Y-%m-%d')
    today = datetime.today()
    age_months = (today.year - dob.year) * 12 + (today.month - dob.month)
    return age_months


def is_username_taken(username):
    return username in user_info.col_values(1)


def verify_password(username, password):
    records = user_info.get_all_values()[1:]
    for row in records:
        if row[0] == username and row[1] == password:
            return True
    return False


def add_new_user():
    print("Add new user info:")
    while True:
        username = user_input("Username", allow_back=False)
        if username.lower() == 'b':
            print("Cannot go back from username input here.")
            return False
        if is_username_taken(username):
            print("Username already taken. Please try another.")
        else:
            break

    while True:
        password = user_input("Password")
        if password == 'b':
            return add_new_user()
        baby_name = user_input("Baby Name")
        if baby_name == 'b':
            continue
        baby_dob = user_input("Baby DOB (YYYY-MM-DD)")
        if baby_dob == 'b':
            continue
        try:
            baby_age_months = calculate_age_months(baby_dob)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue
        birth_weight = user_input("Birth Weight (kg)")
        if birth_weight == 'b':
            continue
        birth_height = user_input("Birth Height (cm)")
        if birth_height == 'b':
            continue
        break

    new_row = [username, password, baby_name, baby_dob,
               str(baby_age_months), birth_weight, birth_height]
    user_info.append_row(new_row)
    print("User added successfully!")
    return True


def login():
    print("Please log in:")
    while True:
        username = user_input("Username", allow_back=False, allow_quit=False)
        if username == 'b':  # this won't happen because allow_back=False here
            return False
        if not is_username_taken(username):
            print("Username not found. Please register first.")
        else:
            break

    while True:
        password = user_input("Password", allow_back=False, allow_quit=False)
        if password == 'b':  # won't happen, no back allowed here
            return login()
        if verify_password(username, password):
            return True
        else:
            print("Incorrect password.")


def log_daily_baby_data():
    print("\n--- Log Daily Baby Data ---")

    while True:
        username = user_input("Enter your username")
        if username == 'b':
            return
        if not is_username_taken(username):
            print("Username not found. Please register first.")
        else:
            break

    while True:
        date = user_input("Date (YYYY-MM-DD)")
        if date == 'b':
            continue
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")
            continue
        try:
            sleep_hours = float(user_input("Sleep (hours)"))
            feed_ml = float(user_input("Feed (ml)"))
            wet_diapers = int(user_input("Wet Diapers"))
            dirty_diapers = int(user_input("Dirty Diapers"))
        except ValueError:
            print("Please enter numeric values.")
            continue
        break

    new_row = [
        username,
        date,
        sleep_hours,
        feed_ml,
        wet_diapers,
        dirty_diapers
    ]

    daily_logs.append_row(new_row)
    print("✅ Daily log saved successfully!")


def update_log_date():
    print("\n--- Update Daily Log Date ---")

    username = user_input("Enter your username")
    if username == 'b':
        return
    if not is_username_taken(username):
        print("Username not found.")
        return

    old_date = user_input("Enter the incorrect date (YYYY-MM-DD)")
    if old_date == 'b':
        return
    new_date = user_input("Enter the correct date (YYYY-MM-DD)")
    if new_date == 'b':
        return

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


def log_growth_data():
    print("\n--- Log Growth Data ---")

    username = user_input("Enter your username")
    if username == 'b':
        return
    if not is_username_taken(username):
        print("Username not found.")
        return

    date = user_input("Date (YYYY-MM-DD)")
    if date == 'b':
        return
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    try:
        weight = float(user_input("Weight (kg)"))
        height = float(user_input("Height (cm)"))
    except ValueError:
        print("Please enter numeric values.")
        return

    new_row = [username, date, weight, height]
    growth.append_row(new_row)
    print("✅ Growth data logged successfully!")


def log_milestones():
    print("\n--- Log Baby Milestone ---")

    username = user_input("Enter your username")
    if username == 'b':
        return
    if not is_username_taken(username):
        print("Username not found.")
        return

    date = user_input("Date (YYYY-MM-DD)")
    if date == 'b':
        return
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    milestone = user_input("Describe the milestone")
    if milestone == 'b':
        return

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

        avg_feed = (
            round(sum(feed_values) / len(feed_values), 2)
            if feed_values else 0
        )

        user_milestones = set()
        for m_row in milestone_rows:
            if m_row[0] == username:
                user_milestones.add(m_row[2])

        latest_weight = None
        latest_height = None
        latest_date = None
        for g_row in growth_rows:
            if g_row[0] == username:
                try:
                    g_date = datetime.strptime(g_row[1], "%Y-%m-%d")
                except ValueError:
                    continue
                if (latest_date is None) or (g_date > latest_date):
                    latest_date = g_date
                    latest_weight = g_row[2]
                    latest_height = g_row[3]

        notes = ""  # Placeholder for any notes, can be extended later

        summary_row = [
            username,
            sleep_sum,
            avg_feed,
            len(user_milestones),
            notes,
            latest_weight or "",
            latest_height or ""
        ]

        summary_sheet.append_row(summary_row)

    print("✅ Summary updated successfully!")


def main():
    print("\n👶🏼 Welcome to Simple Baby Tracker")
    print(
        "This app is designed for parents to track their baby's data "
        "up to 2 years of age."
        )
    print(
        "You can log daily activities, growth, and developmental "
        "milestones."
    )
    print(
        "\n🔹 Tip: Type 'q' at any point to quit, or 'b' to go back and "
        "correct a previous input or review what you entered."
    )
    print(
        "\n🔴 Once registered, "
        "you can simply log in to access and view your data."
    )

    while True:
        print("\nAre you a new user or returning user?")
        print("1. New User (Register)")
        print("2. Returning User (Login)")
        print("3. Quit")

        choice = user_input(
            "Enter 1, 2, or 3",
            allow_back=False,
            allow_quit=False
        )

        if choice == '1':
            if add_new_user():
                print("\nRegistration successful! Moving to daily logs.")
                log_daily_baby_data()
                print("Thank you for logging your baby's data. Goodbye!")
                return
            else:
                print("Registration failed. Try again.")
        elif choice == '2':
            if login():
                print("Login successful! Accessing main menu...")
                break
            else:
                print("Login failed. Please try again.")
        elif choice == '3':
            print("Goodbye!")
            return
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

    while True:
        print("\nChoose an option:")
        print("1. Log Daily Baby Data")
        print("2. Update Daily Log Date")
        print("3. Log Growth Data")
        print("4. Log Milestones")
        print("5. Update Summary Sheet")
        print("6. Quit")

        choice = user_input("Enter 1–6", allow_back=False, allow_quit=False)

        if choice == '1':
            log_daily_baby_data()
        elif choice == '2':
            update_log_date()
        elif choice == '3':
            log_growth_data()
        elif choice == '4':
            log_milestones()
        elif choice == '5':
            update_summary()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
