import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import sys
from colorama import init, Fore, Style
init(autoreset=True)

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
        print(Fore.CYAN + "Exiting the program. Goodbye!" + Style.RESET_ALL)
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
    print(
        Fore.CYAN
        + "\n________________________________________________________________"
        + Style.RESET_ALL
    )
    print(Fore.YELLOW + "\n👋 Welcome, new user!" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n🍼 Let's get you set up." + Style.RESET_ALL)
    print(
        Fore.YELLOW
        + "We’ll ask a few quick questions to register you and your baby."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW + "Make sure you have your baby's date of birth "
        "and birth stats ready." + Style.RESET_ALL)
    print(
        Fore.YELLOW
        + "Type 'q' to quit at any point, or 'b' to go back to "
        "a prior input."
        + Style.RESET_ALL
        )
    print(
        Fore.YELLOW
        + "Once registered, "
        "you can simply log in to access your data."
        + Style.RESET_ALL
        )
    print(Fore.YELLOW + "\n🎬 Let's begin!" + Style.RESET_ALL)
    print(
        Fore.CYAN
        + "\n________________________________________________________________"
        + Style.RESET_ALL
    )

    while True:
        username = user_input("Username", allow_back=False, allow_quit=True)
        if username.lower() == 'b':
            print("Cannot go back from username input here.")
            return False
        if is_username_taken(username):
            print("Username already taken. Please try another.")
        else:
            break

    while True:
        password = user_input("Password", allow_back=False, allow_quit=True)
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

    print(f"\nHello, {username}! 🎉")
    print("After you have entered the details about your baby, "
          "let's record the baby's steps.\n")

    return True


def login():
    print(Fore.CYAN + "Please log in:" + Style.RESET_ALL
          )
    while True:
        username = user_input("Username", allow_back=False, allow_quit=True)
        if username == 'b':
            return False
        if not is_username_taken(username):
            print(
                Fore.RED
                + "Username not found. Please register first."
                + Style.RESET_ALL
            )
        else:
            break

    while True:
        password = user_input("Password", allow_back=False, allow_quit=True)
        if password == 'b':
            return login()
        if verify_password(username, password):
            print(
                Fore.CYAN
                + f"\nHello,{username}, welcome back!"
                + Style.RESET_ALL
            )
            return username
        else:
            print(
                Fore.RED
                + "Incorrect password. Please try again."
                + Style.RESET_ALL
            )


def log_daily_baby_data():
    print("\n--- Log Daily Baby Data ---")

    while True:
        username = user_input("Enter your username")
        if username == 'b':
            return
        if not is_username_taken(username):
            print(
                Fore.RED
                + "Username not found. Please register first."
                + Style.RESET_ALL
            )
        else:
            break

    while True:
        date = user_input("Date (YYYY-MM-DD)")
        if date == 'b':
            continue
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(Fore.RED + "Invalid date format." + Style.RESET_ALL)
            continue
        try:
            sleep_hours = float(user_input("Sleep (hours)"))
            feed_ml = float(user_input("Feed (ml)"))
            wet_diapers = int(user_input("Wet Diapers"))
            dirty_diapers = int(user_input("Dirty Diapers"))
        except ValueError:
            print(Fore.RED + "Please enter numeric values." + Style.RESET_ALL)
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
    print(Fore.GREEN + "✅ Daily log saved successfully!" + Style.RESET_ALL)


def log_growth_data():
    print("\n--- Log Growth Data ---")

    username = user_input("Enter your username")
    if username == 'b':
        return
    if not is_username_taken(username):
        print(Fore.RED + "Username not found." + Style.RESET_ALL)
        return

    date = user_input("Date (YYYY-MM-DD)")
    if date == 'b':
        return
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print(Fore.RED + "Invalid date format." + Style.RESET_ALL)
        return

    try:
        weight = float(user_input("Weight (kg)"))
        height = float(user_input("Height (cm)"))
    except ValueError:
        print(Fore.RED + "Please enter numeric values." + Style.RESET_ALL)
        return

    new_row = [username, date, weight, height]
    growth.append_row(new_row)
    print(Fore.GREEN + "✅ Growth data logged successfully!" + Style.RESET_ALL)


def show_user_profile(username):
    print("\n--- Your Profile ---")
    records = user_info.get_all_values()[1:]
    for row in records:
        if row[0] == username:
            print(f"Username: {row[0]}")
            print(f"Baby Name: {row[2]}")
            print(f"Date of Birth: {row[3]}")
            print(f"Age (months): {row[4]}")
            print(f"Birth Weight: {row[5]} kg")
            print(f"Birth Height: {row[6]} cm")
            return
    print(Fore.RED + "Profile not found." + Style.RESET_ALL)


def display_user_summary(username):
    print("\n--- Your Summary ---")
    summary_rows = summary_sheet.get_all_values()
    headers = summary_rows[0]
    for row in summary_rows[1:]:
        if row[0] == username:
            for i, value in enumerate(row):
                print(f"{headers[i]}: {value}")
            return
    print(Fore.RED + "No summary data found." + Style.RESET_ALL)


def log_milestones():
    print("\n--- Log Baby Milestone ---")

    username = user_input("Enter your username")
    if username == 'b':
        return
    if not is_username_taken(username):
        print(Fore.RED + "Username not found." + Style.RESET_ALL)
        return

    date = user_input("Date (YYYY-MM-DD)")
    if date == 'b':
        return
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print(Fore.RED + "Invalid date format." + Style.RESET_ALL)
        return

    milestone = user_input("Describe the milestone")
    if milestone == 'b':
        return

    new_row = [username, date, milestone]
    milestones.append_row(new_row)
    print(Fore.GREEN + "🎉 Milestone logged successfully!" + Style.RESET_ALL)


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

        notes = ""

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

    print(Fore.GREEN + "✅ Summary updated successfully!" + Style.RESET_ALL)


def main():
    print(
        Fore.CYAN +
        "\n___________________________________________________________________"
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "\n                WELCOME TO SIMPLE BABY TRACKER!"
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "\n⭐ This app helps parents track their baby's data "
        "up to age 2."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "\n💚 Log daily activities, growth, and developmental "
        "milestones."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "\n📊 Get weekly summaries to monitor progress and patterns."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "\n👶 Let's start tracking your little one's amazing progress!"
        + Style.RESET_ALL
    )
    print(
        Fore.CYAN
        + "\n________________________________________________________________"
        + Style.RESET_ALL
    )

    while True:
        print(
            Fore.CYAN
            + "Are you a new user or returning user?"
            + Style.RESET_ALL
        )
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
                print(
                    Fore.GREEN
                    + "Registration successful! Moving to daily logs."
                    + Style.RESET_ALL
                    )
                log_daily_baby_data()
                print(
                    Fore.BLUE
                    + "Thank you for logging your baby's data. Goodbye!"
                    + Style.RESET_ALL
                )
                return
            else:
                print(
                    Fore.RED
                    + "Registration failed. Try again."
                    + Style.RESET_ALL
                    )
        elif choice == '2':
            logged_in_user = login()
            if logged_in_user:
                show_user_profile(logged_in_user)
                update_summary()
                display_user_summary(logged_in_user)
                print(
                    Fore.GREEN
                    + "Login successful! Accessing main menu..."
                    + Style.RESET_ALL
                    )
                break
            else:
                print(
                    Fore.RED
                    + "Login failed. Please try again."
                    + Style.RESET_ALL
                    )
        elif choice == '3':
            print(Fore.BLUE + "GODDBYE!" + Style.RESET_ALL)
            return
        else:
            print(
                Fore.RED
                + "Invalid input. Please enter 1, 2, or 3."
                + Style.RESET_ALL
                )

        print(
            Fore.CYAN
            + "\n____________________________________________________________"
            + Style.RESET_ALL
        )

    while True:
        print("\nChoose an option:")
        print("1. Log Daily Baby Data")
        print("2. Log Growth Data")
        print("3. Log Milestones")
        print("4. Summary Sheet")
        print("5. Quit")

        choice = user_input("Enter 1–5", allow_back=False, allow_quit=False)

        if choice == '1':
            log_daily_baby_data()
        elif choice == '2':
            log_growth_data()
        elif choice == '3':
            log_milestones()
        elif choice == '4':
            update_summary()
        elif choice == '5':
            print(Fore.BLUE + "GOODBYE!" + Style.RESET_ALL)
            break
        else:
            print(
                Fore.RED
                + "Invalid option. Please enter a number between 1 and 5."
                + Style.RESET_ALL
                )


if __name__ == "__main__":
    main()
