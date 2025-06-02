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


def log_exists(sheet, username, log_date):
    records = sheet.get_all_values()[1:]  # skip header
    for row in records:
        if row[0] == username and row[1] == log_date:
            return True
    return False


def user_input(prompt, allow_back=True, allow_quit=True):
    BOLD = "\033[1m"
    RESET = "\033[0m"
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
        print(
            Fore.BLUE
            + BOLD + "Exiting the program. Goodbye!"
            + RESET + Style.RESET_ALL
        )
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
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(
        Fore.CYAN
        + "\n________________________________________________________________"
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + BOLD + "\n👋 Welcome, new user!"
        + RESET + Style.RESET_ALL
    )
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
        "simply log in to view your profile and summary."
        + Style.RESET_ALL
        )
    print(
        Fore.YELLOW
        + "Continue by adding "
        "new data or check your existing info anytime."
        + Style.RESET_ALL
    )
    print(Fore.YELLOW + "\n🎬 Let's begin!" + Style.RESET_ALL)
    print(
        Fore.CYAN
        + "\n________________________________________________________________"
        + Style.RESET_ALL
    )

    steps = [
        {"key": "username", "prompt": "Username", "allow_back": False},
        {"key": "password", "prompt": "Password"},
        {"key": "baby_name", "prompt": "Baby Name"},
        {"key": "baby_dob", "prompt": "Baby DOB (YYYY-MM-DD)"},
        {"key": "birth_weight", "prompt": "Birth Weight (kg)"},
        {"key": "birth_height", "prompt": "Birth Height (cm)"}
    ]

    data = {}
    current_step = 0

    while current_step < len(steps):
        step = steps[current_step]
        key = step["key"]
        prompt = step["prompt"]
        allow_back = step.get("allow_back", True)

        response = user_input(prompt, allow_back=allow_back)

        if response == 'b':
            if current_step > 0:
                current_step -= 1
            else:
                print(Fore.RED + "Cannot go back further." + Style.RESET_ALL)
            continue

        if key == "username":
            if is_username_taken(response):
                print(
                    Fore.RED
                    + "Username already taken. Please try another."
                    + Style.RESET_ALL
                )
                continue
        elif key == "baby_dob":
            try:
                datetime.strptime(response, "%Y-%m-%d")
            except ValueError:
                print(
                    Fore.RED
                    + "Invalid date format. Please use YYYY-MM-DD."
                    + Style.RESET_ALL
                )
                continue
        elif key == "birth_weight" or key == "birth_height":
            try:
                float(response)
            except ValueError:
                print(
                    Fore.RED
                    + "Please enter a valid number."
                    + Style.RESET_ALL
                )
                continue

        data[key] = response
        current_step += 1

    baby_age_months = calculate_age_months(data["baby_dob"])
    new_row = [
        data["username"],
        data["password"],
        data["baby_name"],
        data["baby_dob"],
        str(baby_age_months),
        data["birth_weight"],
        data["birth_height"]
    ]
    user_info.append_row(new_row)

    print(Fore.GREEN + "\n✅ Registration successful!" + Style.RESET_ALL)
    print(Fore.CYAN + f"\nHello, {data['username']}! 🎉" + Style.RESET_ALL)
    print(
        Fore.CYAN
        + "Now that you've entered the details about your baby, "
          "we can move on to daily logs. "
          + Style.RESET_ALL
    )

    return True


def login():
    BOLD = "\033[1m"
    RESET = "\033[0m"
    print(
        Fore.CYAN
        + "\n________________________________________________________________"
        + Style.RESET_ALL
    )
    print()
    print(Fore.CYAN + "Please log in:" + Style.RESET_ALL
          )
    while True:
        username = user_input("Username", allow_back=False, allow_quit=True)
        if username == 'b':
            return False
        if not is_username_taken(username):
            print(
                Fore.RED
                + "Username not found. Please try again."
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
                + "\n"
                + "________________________________________________"
                + "________________"
                + Style.RESET_ALL
            )
            print()
            print(
                Fore.GREEN + BOLD
                + "Login successful!"
                + RESET + Style.RESET_ALL
            )
            print(
                Fore.CYAN
                + BOLD
                + f"\nHello, {username}, welcome back!"
                + RESET
                + Style.RESET_ALL
            )
            print(Fore.CYAN + "Let’s take a look at your profile "
                  "and current summary sheet." + Style.RESET_ALL)
            return username
        else:
            print(
                Fore.RED
                + "Incorrect password. Please try again."
                + Style.RESET_ALL
            )


def log_daily_baby_data():
    print("\n--- Log Daily Baby Data ---")

    steps = [
        {
            "key": "username",
            "prompt": "Enter your username",
            "allow_back": False,
        },
        {
            "key": "log_date",
            "prompt": "Log Date (YYYY-MM-DD)",
            "allow_back": True,
        },

        {"key": "sleep_hours", "prompt": "Sleep (hours)", "allow_back": True},
        {"key": "feed_ml", "prompt": "Feed (ml)", "allow_back": True},
        {"key": "wet_diapers", "prompt": "Wet Diapers", "allow_back": True},
        {
            "key": "dirty_diapers",
            "prompt": "Dirty Diapers",
            "allow_back": True
        },
    ]

    data = {}
    current_step = 0

    while current_step < len(steps):
        step = steps[current_step]
        key = step["key"]
        prompt = step["prompt"]
        allow_back = step["allow_back"]

        response = user_input(prompt, allow_back=allow_back)

        if response == 'b':
            if current_step == 0:
                print(
                    Fore.RED
                    + "Cannot go back from username input."
                    + Style.RESET_ALL
                )
                continue
            else:
                current_step -= 1
                continue

        if key == "username":
            if not is_username_taken(response):
                print(
                    Fore.RED
                    + "Username not found. Please try again."
                    + Style.RESET_ALL
                )
                continue
        elif key == "log_date":
            try:
                datetime.strptime(response, "%Y-%m-%d")
            except ValueError:
                print(Fore.RED + "Invalid date format." + Style.RESET_ALL)
                continue

            if log_exists(daily_logs, data["username"], response):
                print(
                    Fore.RED
                    + f"🚫 Daily log for {response} already exists. "
                    "Please choose another date."
                    + Style.RESET_ALL
                )
                continue
        elif key in ["sleep_hours", "feed_ml"]:
            try:
                float(response)
            except ValueError:
                print(
                    Fore.RED
                    + "Please enter a valid number."
                    + Style.RESET_ALL
                )
                continue
        elif key in ["wet_diapers", "dirty_diapers"]:
            try:
                int(response)
            except ValueError:
                print(
                    Fore.RED
                    + "Please enter an integer value."
                    + Style.RESET_ALL
                )
                continue

        data[key] = response
        current_step += 1

    new_row = [
        data["username"],
        data["log_date"],
        float(data["sleep_hours"]),
        float(data["feed_ml"]),
        int(data["wet_diapers"]),
        int(data["dirty_diapers"])
    ]

    daily_logs.append_row(new_row)
    print(Fore.GREEN + "✅ Daily log saved successfully!" + Style.RESET_ALL)


def log_growth_data():
    print("\n--- Log Growth Data ---")

    username = user_input("Enter your username", allow_back=False)
    if not is_username_taken(username):
        print(
            Fore.RED
            + "Username not found. Please try again."
            + Style.RESET_ALL
        )
        return

    steps = [
        {"key": "log_date", "prompt": "Log Date (YYYY-MM-DD)"},
        {"key": "weight", "prompt": "Weight (kg)"},
        {"key": "height", "prompt": "Height (cm)"},
    ]

    data = {}
    current_step = 0

    while current_step < len(steps):
        step = steps[current_step]
        key = step["key"]
        prompt = step["prompt"]

        response = user_input(prompt, allow_back=True)

        if response == 'b':
            if current_step == 0:
                username = user_input("Enter your username", allow_back=False)
                if not is_username_taken(username):
                    print(Fore.RED + "Username not found." + Style.RESET_ALL)
                    # stay on username input
                    continue
                data = {}
                current_step = 0
                continue
            else:
                current_step -= 1
                continue

        if key == "log_date":
            try:
                datetime.strptime(response, "%Y-%m-%d")
            except ValueError:
                print(Fore.RED + "Invalid date format." + Style.RESET_ALL)
                continue
        elif key in ["weight", "height"]:
            try:
                float(response)
            except ValueError:
                print(
                    Fore.RED
                    + "Please enter numeric values."
                    + Style.RESET_ALL
                )
                continue

        data[key] = response
        current_step += 1

    new_row = [username, data["log_date"],
               float(data["weight"]), float(data["height"])]
    growth.append_row(new_row)
    print(Fore.GREEN + "✅ Growth data saved successfully!" + Style.RESET_ALL)


def show_user_profile(username):
    print()
    print(Fore.MAGENTA + "--- Your Profile ---" + Style.RESET_ALL)
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
    print()
    print(
        Fore.MAGENTA
        + "--- Your Summary ---"
        + Style.RESET_ALL
    )
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

    username = user_input("Enter your username", allow_back=False)
    if not is_username_taken(username):
        print(
            Fore.RED
            + "Username not found. Please try again."
            + Style.RESET_ALL
        )
        return

    steps = [
        {"key": "log_date", "prompt": "Log Date (YYYY-MM-DD)"},
        {"key": "milestone", "prompt": "Describe the milestone"}
    ]

    data = {}
    current_step = 0

    while current_step < len(steps):
        step = steps[current_step]
        key = step["key"]
        prompt = step["prompt"]

        response = user_input(prompt, allow_back=True)

        if response == 'b':
            if current_step == 0:
                print(
                    Fore.RED
                    + "Cannot go back further than this step."
                    + Style.RESET_ALL
                )
                continue
            else:
                current_step -= 1
                continue

        if key == "log_date":
            try:
                datetime.strptime(response, "%Y-%m-%d")
            except ValueError:
                print(Fore.RED + "Invalid date format." + Style.RESET_ALL)
                continue

        data[key] = response
        current_step += 1

    new_row = [username, data["log_date"], data["milestone"]]
    milestones.append_row(new_row)
    print(Fore.GREEN + "\n✅ Milestone saved successfully!" + Style.RESET_ALL)


def update_summary():
    print("\n--- LOADING SUMMARY SHEET... ---")
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
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(
        Fore.CYAN +
        "\n________________________________________________________________"
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + f"\n{BOLD}                WELCOME TO SIMPLE BABY TRACKER!{RESET}"
        + Style.RESET_ALL
    )

    print(
        Fore.YELLOW
        + "\n⭐ This app helps you track your baby's data "
        "during their 1st year."
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
        print()
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
                log_daily_baby_data()
                log_growth_data()
                log_milestones()
                print(
                    Fore.BLUE
                    + "Thank you for logging your baby's data, "
                    + "growth, and milestones. "
                    + "Goodbye!"
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
                    Fore.CYAN
                    + "\n________________________________________"
                    "________________________"
                    + Style.RESET_ALL
                )
                print()
                print(
                    Fore.GREEN
                    + "You may now access the main menu."
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
            print(Fore.BLUE + BOLD + "GOODBYE!" + RESET + Style.RESET_ALL)
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
        print()
        print(Fore.CYAN + "Choose an option:" + Style.RESET_ALL)
        print("1. Log Daily Baby Data")
        print("2. Log Growth Data")
        print("3. Log Milestones")
        print("4. Quit")

        choice = user_input("Enter 1–4", allow_back=False, allow_quit=False)

        if choice == '1':
            log_daily_baby_data()
        elif choice == '2':
            log_growth_data()
        elif choice == '3':
            log_milestones()
        elif choice == '4':
            print(Fore.BLUE + BOLD + "GOODBYE!" + RESET + Style.RESET_ALL)
            break
        else:
            print(
                Fore.RED
                + "Invalid option. Please enter a number between 1 and 5."
                + Style.RESET_ALL
                )


if __name__ == "__main__":
    main()
