# Standard libraries
import sys
from datetime import datetime, timedelta

# Third party libraries
import gspread
from google.oauth2.service_account import Credentials
from colorama import init, Fore, Style

# ANSI escape sequences for bold formatting
BOLD = "\033[1m"
RESET = "\033[0m"

# Reset text color after each print
init(autoreset=True)

# Required Google API scopes
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from the service account
CREDS = Credentials.from_service_account_file('creds.json')

# Apply the required access scopes to credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Authorize a gspread client using the scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Open the Google Sheet for reading and writing
SHEET = GSPREAD_CLIENT.open('simple_baby_tracker')

# Access to the worksheets
user_info = SHEET.worksheet('user_info')
daily_logs = SHEET.worksheet('daily_logs')
growth = SHEET.worksheet('growth')
milestones = SHEET.worksheet('milestones')
summary_sheet = SHEET.worksheet('summary')


# Prevent duplicate log entries
def log_exists(sheet, username, log_date):
    records = sheet.get_all_values()[1:]
    for row in records:
        if row[0] == username and row[1] == log_date:
            return True
    return False


def user_input(prompt, allow_back=True, allow_quit=True):

    suffix = ""
    # Build the input suffix message based on allowed actions
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

    # Prompt the user with the message and suffix, strip extra spaces
    response = input(prompt.rstrip(": ") + suffix).strip()

    # Handle quit command if allowed
    if allow_quit and response.lower() in ['q', 'quit', 'exit']:
        print(
            Fore.BLUE + BOLD +
            "Exiting the program. Goodbye!" +
            RESET + Style.RESET_ALL
        )

        # Return the user's input
        sys.exit()

    # Handle back command if allowed
    if allow_back and response.lower() == 'b':
        return 'b'
    return response


def calculate_age_months(dob_str):
    # Convert the date of birth string to a datetime object
    dob = datetime.strptime(dob_str, '%Y-%m-%d')

    # Get the current date
    today = datetime.today()

    # Calculate the age in months
    age_months = (today.year - dob.year) * 12 + (today.month - dob.month)

    # Return the total number of months
    return age_months


def is_username_taken(username):
    # Check if the username exists in the user_info worksheet
    return username in user_info.col_values(1)


def verify_password(username, password):
    # Get all records from the user_info worksheet
    records = user_info.get_all_values()[1:]

    for row in records:
        if row[0] == username and row[1] == password:
            return True
    return False


def add_new_user():

    # Introductory message with instructions
    print(
        Fore.CYAN
        + "\n" + "_" * 66
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + BOLD
        + "\n👋 Welcome, new user!"
        + RESET
        + Style.RESET_ALL
    )
    print(Fore.YELLOW + "\n🍼 Let's get you set up." + Style.RESET_ALL)
    print(
        Fore.YELLOW
        + "We’ll ask a few quick questions to register you and your baby."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "Make sure you have your baby's date of birth "
        + "and birth stats ready."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "Type 'q' to quit at any point, or 'b' to go back to "
        + "a prior input."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "Once registered, "
        + "simply log in to view your profile and summary."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "Continue by adding "
        + "new data or check your existing info anytime."
        + Style.RESET_ALL
    )

    print(Fore.YELLOW + "\n🎬 Let's begin!" + Style.RESET_ALL)
    print(
        Fore.CYAN
        + "\n" + "_" * 66
        + Style.RESET_ALL
    )

    # Setup questions for user registration
    steps = [
        {"key": "username", "prompt": "Username", "allow_back": False},
        {"key": "baby_name", "prompt": "Baby Name"},
        {"key": "baby_dob", "prompt": "Baby DOB (YYYY-MM-DD)"},
        {"key": "birth_weight", "prompt": "Birth Weight (kg)"},
        {"key": "birth_height", "prompt": "Birth Height (cm)"}
    ]

    data = {}
    current_step = 0

    # Loop through each step of the form
    while current_step < len(steps):
        step = steps[current_step]
        key = step["key"]
        prompt = step["prompt"]
        allow_back = step.get("allow_back", True)

        # Get user input for the current step
        response = user_input(prompt, allow_back=allow_back)

        # Handle 'back' option
        if response == 'b':
            if current_step > 0:
                current_step -= 1
            else:
                print(Fore.RED + "Cannot go back further." + Style.RESET_ALL)
            continue

        # Validation for username: ensure it's unique
        if key == "username":
            if is_username_taken(response):
                print(
                    Fore.RED
                    + "Username already taken. Please try another."
                    + Style.RESET_ALL
                )
                continue

        # Validation for date: must match YYYY-MM-DD
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

        # Validation for numeric weight/height
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

        # Save valid input
        data[key] = response
        current_step += 1

    # Calculate baby's age in months and prepare row for worksheet
    baby_age_months = calculate_age_months(data["baby_dob"])
    new_row = [
        data["username"],
        data["baby_name"],
        data["baby_dob"],
        str(baby_age_months),
        data["birth_weight"],
        data["birth_height"]
    ]
    user_info.append_row(new_row)

    # Confirmation message
    print(Fore.GREEN + "\n✅ Registration successful!" + Style.RESET_ALL)

    print(
        Fore.CYAN
        + "\n" + "_" * 66
        + Style.RESET_ALL
    )
    print()
    print(Fore.CYAN + f"\nHello, {data['username']}! 🎉" + Style.RESET_ALL)
    print(
        Fore.CYAN
        + "Now that you've entered the details about your baby, "
        + "we can move on to daily logs. "
        + Style.RESET_ALL
    )

    return data["username"]


def login():
    print(
        Fore.CYAN
        + "\n" + "_" * 66
        + Style.RESET_ALL
    )
    print()
    # Prompt user to log in
    print(Fore.CYAN + "Please log in:" + Style.RESET_ALL)

    while True:
        # Get username input from user; no back option, but can quit
        username = user_input("Username", allow_back=False, allow_quit=True)
        if username == 'b':
            return False
        if not is_username_taken(username):
            # Check if the entered username exists in the user_info sheet
            print(
                Fore.RED
                + "Username not found. Please try again."
                + Style.RESET_ALL
            )
        else:
            print()
            # Successful login message and welcome greeting
            print(
                Fore.GREEN
                + "Login successful!"
                + Style.RESET_ALL
            )
            print(
                Fore.CYAN
                + "\n" + "_" * 66
                + Style.RESET_ALL
            )
            print()
            print(
                Fore.CYAN
                + f"Hello, {username}, welcome back!"
                + Style.RESET_ALL
            )
            return username


def log_daily_baby_data(current_user):
    # Print header showing which user we are logging data for
    print()
    print(f"\n--- Log Daily Baby Data for {current_user} ---")

    # Define the input steps and prompts for daily log data entry
    steps = [
        {
            "key": "log_date",
            "prompt": "Log Date (YYYY-MM-DD)",
            "allow_back": False,
        },
        {"key": "sleep_hours", "prompt": "Sleep (hours)", "allow_back": True},
        {"key": "feed_ml", "prompt": "Feed (ml)", "allow_back": True},
        {"key": "wet_diapers", "prompt": "Wet Diapers", "allow_back": True},
        {
            "key": "dirty_diapers",
            "prompt": "Dirty Diapers",
            "allow_back": True,
        },

    ]

    # Initialize data dictionary with the current username
    data = {"username": current_user}
    current_step = 0

    # Loop through all input steps until all are completed
    while current_step < len(steps):
        step = steps[current_step]
        key = step["key"]
        prompt = step["prompt"]
        allow_back = step["allow_back"]

        response = user_input(prompt, allow_back=allow_back)

        if response == 'b':
            # Handle going back to previous step, except from log_date step
            if current_step == 0:
                print(
                    Fore.RED
                    + "Cannot go back from the log date input."
                    + Style.RESET_ALL
                )
                continue
            else:
                current_step -= 1
                continue

        # Validate log_date input format and duplication
        if key == "log_date":
            try:
                datetime.strptime(response, "%Y-%m-%d")
            except ValueError:
                print(Fore.RED + "Invalid date format." + Style.RESET_ALL)
                continue

            # Check if a log for this user and date already exists
            if log_exists(daily_logs, current_user, response):
                print(
                    Fore.RED
                    + f"🚫 Daily log for {response} already exists. "
                    + "Please choose another date."
                    + Style.RESET_ALL
                )
                continue
        # Validate sleep_hours and feed_ml as valid floating-point numbers
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
        # Validate wet_diapers and dirty_diapers as valid numbers
        elif key in ["wet_diapers", "dirty_diapers"]:
            try:
                int(response)
            except ValueError:
                print(
                    Fore.RED
                    + "Please enter a valid number."
                    + Style.RESET_ALL
                )
                continue

        data[key] = response
        current_step += 1

    # Prepare a new row with all input data to append to the Google Sheet
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


def log_growth_data(current_user):
    """
    Prompts the user to log their baby's growth data.
    Validates input formats, prevents duplicate entries for the same date, and
    appends the new data to the 'growth' Google Sheet. Allows navigation back
    to previous steps during input (except log date).
    """
    print(f"\n--- Log Growth Data for {current_user} ---")

    steps = [
        {
            "key": "log_date",
            "prompt": "Log Date (YYYY-MM-DD)",
            "allow_back": False,
        },

        {"key": "weight", "prompt": "Weight (kg)", "allow_back": True},
        {"key": "height", "prompt": "Height (cm)", "allow_back": True},
    ]

    data = {}
    current_step = 0

    while current_step < len(steps):
        step = steps[current_step]
        key = step["key"]
        prompt = step["prompt"]
        allow_back = step.get("allow_back", False)

        response = user_input(prompt, allow_back=allow_back)

        if response == 'b':
            if current_step == 0:
                print(
                    Fore.RED
                    + "Cannot go back from the log date input."
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

            if log_exists(growth, current_user, response):
                print(
                    Fore.RED
                    + f"🚫 Growth log for {response} already exists. "
                    + "Please choose another date."
                    + Style.RESET_ALL
                )
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

    new_row = [
        current_user,
        data["log_date"],
        float(data["weight"]),
        float(data["height"]),
    ]
    growth.append_row(new_row)
    print(Fore.GREEN + "✅ Growth data saved successfully!" + Style.RESET_ALL)


def show_user_profile(username):
    """
    Displays the user profile by fetching baby details from the
    'user_info' sheet. Shows name, birth date, age, birth weight,
    and height. If the username is not found, shows an error.
    """

    print()
    print(Fore.MAGENTA + "--- Your Profile ---" + Style.RESET_ALL)
    records = user_info.get_all_values()[1:]
    for row in records:
        if row[0] == username:
            print(f"Username: {row[0]}")
            print(f"Baby Name: {row[1]}")
            print(f"Date of Birth: {row[2]}")
            print(f"Age (months): {row[3]}")
            print(f"Birth Weight: {row[4]} kg")
            print(f"Birth Height: {row[5]} cm")
            return
    print(Fore.RED + "Profile not found." + Style.RESET_ALL)


def display_user_summary(username):
    """
    Fetches and displays the summary data for the given user from the
    'summary_sheet'. If data is found, prints each field with its
    header. Otherwise, shows a 'no summary found' message.
    """

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


def log_milestones(current_user):
    """
    Allows the user to log a milestone (e.g., crawling) for a given date.
    Validates date format, avoids duplicates, and ensures the milestone
    is not numeric-only. Adds data to the 'milestones' sheet.
    """

    print("\n--- Log Baby Milestone ---")

    username = current_user
    if not is_username_taken(username):
        print(
            Fore.RED
            + "Username not found. Please try again."
            + Style.RESET_ALL
        )
        return  # <== only return here if username not found

    steps = [
        {
            "key": "log_date",
            "prompt": "Log Date (YYYY-MM-DD)",
            "allow_back": True,
        },
        {
            "key": "milestone",
            "prompt": "Describe the milestone "
            "(e.g., babbling or 'None')",
            "allow_back": False
        }
    ]

    data = {}
    current_step = 0

    while current_step < len(steps):
        step = steps[current_step]
        key = step["key"]
        prompt = step["prompt"]

        response = user_input(prompt, allow_back=False)

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
            if log_exists(milestones, username, response):
                print(
                    Fore.RED
                    + f"🚫 A milestone log for {response} already exists. "
                    + "Please choose another date."
                    + Style.RESET_ALL
                )
                continue

        if key == "milestone":
            if response.strip().isdigit():
                print(
                    Fore.RED
                    + "Milestone cannot be numeric only. "
                    + "Please type 'None' if there are no milestones."
                    + Style.RESET_ALL
                )
                continue
        data[key] = response
        current_step += 1

    new_row = [username, data["log_date"], data["milestone"]]
    milestones.append_row(new_row)
    print(Fore.GREEN + "\n✅ Milestone saved successfully!" + Style.RESET_ALL)


def update_summary():
    """
    Updates the 'summary_sheet' with the past week's data for each user.
    This includes total sleep hours, feed volume, diaper counts,
    milestone achievements, and the latest growth records. Clears the
    sheet first, recalculates values, and appends a row per user.
    """

    print("\n--- LOADING SUMMARY SHEET... ---")
    summary_sheet.clear()

    headers = [
        "Username", "Total Sleep (hrs)", "Total Feed (ml)",
        "Milestones Achieved", "Latest Weight", "Latest Height",
        "Total Wet Diapers", "Total Dirty Diapers"
    ]
    summary_sheet.append_row(headers)

    today = datetime.today()
    week_ago = today - timedelta(days=7)

    user_rows = user_info.get_all_values()[1:]
    daily_rows = daily_logs.get_all_values()[1:]
    milestone_rows = milestones.get_all_values()[1:]
    growth_rows = growth.get_all_values()[1:]

    for user in user_rows:
        username = user[0]

        user_daily_logs = [row for row in daily_rows if row[0] == username]
        recent_logs = [
            row for row in user_daily_logs
            if datetime.strptime(row[1], '%Y-%m-%d') >= week_ago
        ]

        # Calculate total sleep and total feed (in ml)
        total_sleep = sum(
            float(row[2]) for row in recent_logs if row[2].strip()
        )
        total_feed = sum(
            float(row[3]) for row in recent_logs if row[3].strip()
        )
        total_wet_diapers = sum(
            int(row[4]) for row in recent_logs if row[4].strip()
        )
        total_dirty_diapers = sum(
            int(row[5]) for row in recent_logs if row[5].strip()
        )

        user_milestones = [
            row for row in milestone_rows if row[0] == username
        ]
        recent_milestones = [
            row for row in user_milestones
            if datetime.strptime(row[1], '%Y-%m-%d') >= week_ago
            and row[2].strip().lower() != "none"
            and row[2].strip() != ""
        ]
        milestones_count = len(recent_milestones)

        user_growth = [row for row in growth_rows if row[0] == username]
        if user_growth:
            user_growth.sort(
                key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'),
                reverse=True
            )
            latest_weight = user_growth[0][2]
            latest_height = user_growth[0][3]
        else:
            latest_weight = ""
            latest_height = ""

        # Append summary row
        summary_sheet.append_row([
            username,
            round(total_sleep, 2),
            round(total_feed, 2),
            milestones_count,
            latest_weight,
            latest_height,
            total_wet_diapers,
            total_dirty_diapers
        ])

    print(
        Fore.GREEN
        + "✅ Summary sheet updated successfully!"
        + Style.RESET_ALL
    )


def main_menu(current_user):
    """
    Displays the main menu for returning users after login.
    Allows the user to choose between logging daily data,
    growth data, milestones, or quitting the app. The selected
    option is handled via a loop and passed to the relevant function.
    """
    while True:
        print()
        print(Fore.CYAN + "Choose an option:" + Style.RESET_ALL)
        print("1. Log Daily Baby Data")
        print("2. Log Growth Data")
        print("3. Log Milestones")
        print("4. Quit")

        choice = user_input("Enter 1–4", allow_back=False, allow_quit=False)

        if choice == '1':
            log_daily_baby_data(current_user)
        elif choice == '2':
            log_growth_data(current_user)
        elif choice == '3':
            log_milestones(current_user)
        elif choice == '4':
            print(Fore.BLUE + BOLD + "GOODBYE!" + RESET + Style.RESET_ALL)
            return  # Exit menu
        else:
            print(
                Fore.RED
                + "Invalid option. Please enter a number between 1 and 4."
                + Style.RESET_ALL
            )


def main():
    """
    Entry point of the Baby Tracker app.
    Greets the user and asks whether they are new or returning.
    For new users: runs registration and initial logging steps.
    For returning users: logs them in, displays their profile,
    updates and shows the weekly summary, and opens the main menu.
    """

    print(
        Fore.CYAN
        + "\n" + "_" * 66
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
        + "during their 1st year."
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "\n💚 Log daily activities, growth, and developmental "
        + "milestones."
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
        + "\n" + "_" * 66
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
            current_user = add_new_user()
            if current_user:
                log_daily_baby_data(current_user)
                log_growth_data(current_user)
                log_milestones(current_user)
                print(
                    Fore.CYAN
                    + "\n" + "_" * 66
                    + Style.RESET_ALL
                )
                print()
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
            current_user = login()
            if current_user:
                show_user_profile(current_user)
                update_summary()
                display_user_summary(current_user)
                print(
                    Fore.CYAN
                    + "\n" + "_" * 66
                    + Style.RESET_ALL
                )
                print()  # blank line for spacing
                print(
                    Fore.GREEN
                    + "You may now access the main menu."
                    + Style.RESET_ALL
                )
                main_menu(current_user)
                return

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
            + "\n" + "_" * 66
            + Style.RESET_ALL
        )


if __name__ == "__main__":
    main()
