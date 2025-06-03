# Simple Baby Tracker

![Welcome to Simple Baby Tracker](assets/images/BabyTracker.png)

Simple Baby Tracker is an interactive command-line baby tracking application implemented in Python and deployed via Code Institute's Heroku Terminal.
The app is designed for new parents to easily log and monitor their baby's daily activities—such as sleep, feeding, and diaper changes—as well as track growth progress (weight and height) and developmental milestones. It features secure user registration and login, with built-in validation for usernames and passwords. While every parent receives recommendations from doctors about average sleep and feeding amounts per day, this app is intended solely to help parents conveniently track their baby's data. All data is securely stored using Google Sheets integration.

## Objective
The objective of the application is to help new parents who want a simple, non-app-based solution to track their baby's daily needs and development progress using just their computer and Google account.

## User Stories

### Site Owner Goal

The primary goal of the site owner is to empower new parents by offering a reliable, user-friendly tool to track their baby’s daily habits and developmental progress. This baby tracker app serves as a digital companion during the early, often overwhelming stages of parenthood. As a parent of a newborn, I found it challenging to keep track of my baby’s daily needs and milestones while adjusting to a new routine. To solve this problem, I created a tool that not only helps other new parents, but also supports me in monitoring and understanding my baby's growth.

- **Easy Access to Data**: I want all logs to be saved automatically, giving parents access to their data anytime, anywhere.

- **Better Awareness**: I want to help parents recognize patterns in sleep, feeding, diaper changes, and growth.

- **Milestone Monitoring**: I want to enable users to track important firsts and developmental achievements.

- **Personal Insights**: I provide summaries to help users make informed decisions and spot irregularities.

- **Daily Consistency**: I want to encourage regular input to create a detailed, long-term record of their baby’s needs and progress.

- **Reduced Mental Load**: I want to support parents during a busy and emotional phase of life by simplifying the tracking process.

- **Returning Users Login System**: I want enable returning users to access their past logs through a simple username login system.

- **Application Structure**: I want straightforward, well-structured questions that are easy for users to understand and answer.

### Site User Goals

#### First-time users

- **Understand the App’s Purpose**: I want to quickly grasp that the app helps parents track their baby's daily needs and development.

- **See the Benefits**: I want to learn how the app reduces stress by organizing data and offering helpful summaries and feedback.

- **Know It’s Beginner-Friendly**: I want to feel reassured that no advanced technical skills are needed to use the app.

#### Returning users

- I want to feel supported by having one simple, organized place to manage my baby’s routine.
- I want to view summaries of sleep, feeding, and diaper data to spot patterns and track consistency.
- I want to update milestones as my baby reaches new developments.
- I want to log daily baby activities quickly by just using my username.

## Features

### User Registration

1. Main welcome message

The main welcome message is the friendly introductory text displayed before the program asks the user whether they are a new user or not. It helps set a positive tone and guides them on what to expect.

![Welcome message](assets/images/Welcome%20message.png)


1. Google Sheets Integration

**Secure Access**: Uses gspread with Google Service Account credentials to connect securely to your Google Sheets backend.
**Multi-Sheet Support**: Stores different data categories in separate sheets:
- user_info — Stores registered users and their babies’ info.
- daily_logs — Tracks daily sleep, feeding, and diaper counts.
- growth — Logs baby’s growth metrics (weight, height).
- milestones — Records baby developmental milestones.
- summary — Aggregates weekly summaries for each user.

This structure keeps user's data organized and easily extendable.

2. User Login System

When the program starts, it displays a prompt asking the user if they are a new user or a returning user. This helps guide users through the appropriate next steps.

![Login](assets/images/log%20in.png)

This user-friendly menu ensures that both new and returning users can easily access the application and manage their profiles or data accordingly.

3. New User Welcome Message

When a new user starts the app, a clear and friendly welcome message guides them through the registration process.
It explains what information they need (e.g., baby’s birth date and stats), provides instructions on how to quit or go back during input, and sets expectations for what happens after registration (logging in, viewing profile, adding data).
This feature ensures users feel supported and informed right from the start, improving onboarding and reducing confusion.

![NewUserWelcomeMessage](assets/images/welcome%20message%202.png)

4. User Registration

It checks if the chosen username already exists to avoid duplicates.
It collects baby name, date of birth (validated to ensure proper date format), birth weight, and height.
It automatically computes baby age in months from date of birth.
It saves all this info in the user_info worksheet.
It ensures all fields are entered correctly before saving, prompting users to correct mistakes.
Each input field clearly displays instructions including options to quit ('q') or go back ('b'), allowing flexible and error-tolerant data entry.
After completing the registration process, users receive an explicit success message (✅ Registration successful!) confirming their profile has been created.
This feedback reassures users that their information was saved correctly and they can proceed confidently to log in or add more data.

This ensures accurate baseline data for each baby.

![UserInfo](assets/images/User_info.png)

5. Personalized Welcome After Registration 

![UserInfo](assets/images/User_info.png)

4. Daily Baby Data Logging

**Data Fields**: Users input daily:
- Date (validated)
- Sleep duration (hours, numeric)
- Feeding amount (ml, numeric)
- Wet diapers count (numeric)
- Dirty diapers count (numeric)

**Input Checking**: Validates every input for correct format and numeric values.
**Data Storage**: Appends data to the daily_logs worksheet.
**Flexible Input**: Users can quit or backtrack during entry.

Allows daily tracking of baby’s routine for better monitoring.

5. Growth Data Logging

Data Captured:
- Date of measurement
- Baby’s weight (kg)
- Baby’s height (cm)

**Validation**: Ensures date is formatted correctly and measurements are positive numbers.
**Storage**: Adds records to the growth worksheet.

Provides longitudinal tracking of baby’s physical growth milestones.

6. Milestone Logging

**Milestone Tracking**: Allows users to log developmental milestones with:
- Date achieved
- Description of milestone (e.g., “First smile”, “Crawling”)

**Validation**: Checks for valid date entries.
**Storage**: Saves milestones to the milestones worksheet.

Helps parents keep track of important baby achievements.

7. User Profile Display

**Overview**: Shows a summary of the logged-in user’s and baby’s details:
- Username
- Baby name
- Date of birth
- Baby’s current age (in months)
- Birth weight and height

Gives quick access to personal and baby info.

8. User Summary Display

**Summary Overview**: Pulls data from the summary worksheet to show:
- Total sleep over the past week
- Average daily feeding amount
- Number of milestones achieved recently
- Latest weight and height recorded
- Any additional notes

**Helps Parents**: Provides at-a-glance insight into the baby’s recent progress.

9. Summary Sheet Update

Automated Aggregation:
- Calculates total sleep in last 7 days
- Computes average feeding volume
- Counts milestones recorded recently
- Retrieves most recent growth measurements

**Data Refresh**: Clears previous summary data and rewrites updated figures.
**Keeps Summary Current**: Ensures parents always see up-to-date info.

This feature consolidates scattered data for meaningful insights.

10. Enhanced Input Handling

User-friendly Commands:
- q to quit from prompts at any time.
- b to go back to previous menu or input prompt.

**Clear Instructions**: Prompts display available options explicitly.

**Visual Feedback**: Uses colored console text with colorama:
- Green for success messages
- Red for errors or invalid inputs
- Yellow for warnings or info
- Blue for goodbye message
- Cyan for instructions

**Robust Validation**: Catches invalid inputs early and guides user to correct mistakes.

These improve usability and reduce frustration during data entry.

## Future Features

- I was wondering whether I should add hints about the amount of food or sleep a child needs each month so that parents would aim for that, but I decided not to include it in future plans because every child is different and each has different needs and doctor recommendations.
- Allow users to create profiles for multiple babies under the same account.
- Auto-save progress every few inputs to prevent data loss if the program closes unexpectedly.
- Record the exact time for each data entry, not just the date.
- Add password reset option.
- Allow users to export their baby’s logged data as CSV or simple text reports.
- Add the function to View Today's Summary for the Logged-in Users.

## Bugs

### Fixed Bugs 

* BUG:'Back'Option - When I typed 'b' to go back during data input (e.g., while entering sleep hours), the app exited the whole function instead of returning to the previous step. The 'b' input wasn’t being intercepted properly and was treated like any invalid input or passed through without a return handler.
**FIX**: I added input checking for 'b' in each step. When detected, the function now returns a 'back' signal, and the main loop handles re-displaying the previous prompt.

* BUG: Daily Logs Date Association - Daily logs stored in the Google Sheet did not contain a clear date, making it difficult to analyze trends or retrieve entries for a specific day.The append_row() function did not include a timestamp by default.
**FIX**: I introduced a timestamp using Python’s datetime module and prepended it to each row before storing.

* BUG: Invalid Input (e.g., Typing 'ten') - Entering non-numeric values for numeric questions (e.g., "ten" instead of 10) I caused a ValueError and crashed the app. int() or float() conversion was not wrapped in error handling logic.
**Fix**: I wrapped all numeric conversions in try/except blocks and looped until the user provided a valid value.

* BUG: "None" Milestone - When I entered None in the milestone input, the app still counted it as a valid milestone entry in the summary, inflating the count.The milestone logging function did not properly validate user input. The input 'None' was being appended to the milestone log and later included in summary statistics.
**FIX**: I added input validation to check for 'None' before saving a milestone.

* BUG: Duplicate log_date Prevention - In the log_milestones(), log_growth(), log_daily_baby_data() functions, a bug was fixed that previously allowed users to log multiple milestones and other information for the same date under the same username. This could lead to confusion and data inconsistencies.
**FIX**:  Now, before saving a milestone, the function checks if a milestone for the given username and date already exists. If a duplicate is found, the user is informed with a clear error message and prompted to enter a different date. This prevents accidental overwriting or multiple entries for the same milestone, growth or daily data dates, ensuring cleaner and more accurate logs.

### Unfixed Bugs

As of the latest testing, no bugs have been identified. The website is functioning as expected, to the best of my knowledge.

## Testing

### Manual Testing

See [TESTING.md](TESTING.md) for more details of manual testing.
Manual tests were carried out throughout the development process. Each feature was tested to ensure correct functionality, including error handling, user input validation, and support for multiple user accounts. This included:
- Username and Name Validation: Inputs were tested to confirm that whitespace and special characters were not allowed. The username was validated to accept only 2–10 characters.
- Password Validation: Password inputs were tested to ensure they were at least 6 characters long and contained no whitespace.
- New and Returning Users: Multiple scenarios were tested, including new user registration, returning user login, invalid entries, and quitting mid-process.

### Validation Testing

I used the [CI Python Linter](https://pep8ci.herokuapp.com/#) and followed the [PEP8 guidelines](https://peps.python.org/pep-0008/) to validate my code.

As a result of the linting process, I made the following adjustments:

1. Removed unnecessary blank lines and trailing white spaces.
2. Ensured that all lines are under 79 characters, and limited docstring lines to 72 characters as recommended.
3. Grouped imports in the correct order:
- Standard library imports
- Related third-party imports
- Local application imports

![Run Python Linter](assets/run-python-linter.png)

![Guide Python Linter](assets/guide-python-linter.png)

## Deployment

This project was deployed using the Code Institute’s mock terminal for Heroku.

Steps for deployment:
1. Add the list of requirements by writing in the terminal "pip3 freeze > requirements.txt".
2. Log into Heroku.
4. Click "NEW" in the top right-hand corner and choose the option Create new app.
5. Input a unique app name.
6. Choose Region - Europe.
7. Choose "Settings" from the menu.
8. Go to section "Config Vars" and click button "Reveal Config Vars”.
9. Add key and value. For this project I added creds.json as the key and copied the contents of this into the value.
10. Go to section "Build packs" and click "Add build pack”.
11. Go to "Deploy" in the menu bar.
12. Go to section "deployment method", choose "GitHub".
13. New section will appear "Connect to GitHub".
14. Type the name of your repository and click "search".
15. Once Heroku finds your repository - click "connect".
16. Click "Enable automatic deploys" or manually deploy by choosing "Deploy branch".
17. Click "Deploy branch".

## Local Deployment 

This project can be cloned or forked in order to make a local copy on your own system.

For either method, you will need to install any applicable packages found within the requirements.txt file.

pip3 install -r requirements.txt.
If using any confidential credentials, such as CREDS.json or env.py data, these will need to be manually added to your own newly created project as well.


## Forking and Cloning
To fork this repository:

1. Log in to your Github account.
2. Navigate to the repository page.
3. Click the "Fork" button in the top-right corner.

To Clone:

1. Go to the forked repository on Github.
2. Click the green "Code" button.
3. Copy the HTTPS link: 
4. Open your terminal and type: git clone 

## Create a Virtual Environment (using VS code)

Open the Command Palette (Ctrl + Shift + P on Windows or Cmd + Shift + P on macOS).
In the Command Palette type: Python: Create Environment.
Select Python: Create Environment from the list.
Select Venv from the drop down menu.
Check that your environment is active by editing an .py file and looking for ('venv': venv) near the bottom right hand corner of the screen.

## Technology Used

* Visual Studio Code with assistance of flake8 linter extension.
* [Github](https://github.com/) to host the repository.
* Git used for version control. (git add, git commit, git push)
* The [CI Python Linter](https://pep8ci.herokuapp.com/#) for validating the Python code.
* [Heroku](https://pep8ci.herokuapp.com/) for deploying the website.
* Flow charts from [Lucid Chart](https://lucid.app).

## Python Version, Packages and Libaries Used
The project was developed using Python 3.13.2.

I've used the following Python packages and/or external imported packages:
* datetime - Used to work with date and time, particulary to calculate recovery timelines based on number of days since surgery.
* gspread - Used to interact with Google Sheets API for reading and writing data to a spreadsheet.
* google.oauth2.service_account.Credentials - Provides secure authentication for access to Google Sheets API.
* colorama - Used to add colour to the terminal output.
* sys - used to see paths to files and exit code if necessary

## Credits

https://www.canva.com/dream-lab 
https://emojipedia.org/ 

## Acknowledgements

- I'm really grateful to my mentor, Dick Vlaanderen, for sharing helpful advice and thoughtful suggestions throughout the project.

- I’d like to thank my husband for his unwavering support, especially for patiently taking care of our nine- month-old baby while I was working on my project.



