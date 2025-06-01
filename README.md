# Simple Baby Tracker

![Welcome to Simple Baby Tracker](assets/images/BabyTracker.png)

Simple Baby Tracker is an interactive command-line baby tracking application implemented in Python and deployed via Code Institute's Heroku Terminal.

The app is designed for new parents to easily log and monitor their baby's daily activities (Sleep, Feed, Diaper Changes), growth progress (weight and height) and development milestones, with a structured interface and personalized feedback, using Google Sheets backend.

## Objective
The objective of the application is to help new parents who want a simple, non-app-based solution to track their baby's daily needs and development progress using just their computer and Google account.

## User Stories

### Site Owner Goal

The primary goal of the site owner is to empower new parents by offering a reliable, user-friendly tool to track their baby’s daily habits and developmental progress. This baby tracker app serves as a digital companion during the early, often overwhelming stages of parenthood. As a parent of a newborn, I found it challenging to keep track of my baby’s daily needs and milestones while adjusting to a new routine. To solve this problem, I created a tool that not only helps other new parents, but also supports me in monitoring and understanding my baby's growth.

- **Easy Access to Data**: I want all logs to be saved automatically and securely, giving parents access to their data anytime, anywhere.

- **Better Awareness**: I want to help parents recognize patterns in sleep, feeding, diaper changes, and growth.

- **Milestone Monitoring**: I want to enable users to track important firsts and developmental achievements.

- **Personal Insights**: I provide summaries to help users make informed decisions and spot irregularities.

- **Daily Consistency**: I want to encourage regular input to create a detailed, long-term record of their baby’s needs and progress.

- **Reduced Mental Load**: I want to support parents during a busy and emotional phase of life by simplifying the tracking process.

- **Returning Users Login System**: I want enable returning users to access their past logs through a simple username and password login system.

- **Application Structure**: I want straightforward, well-structured questions that are easy for users to understand and answer.

### Site User Goals

#### First-time users

- **Understand the App’s Purpose**: I want to quickly grasp that the app helps parents track their baby's daily needs and development.

- **See the Benefits**: I want to learn how the app reduces stress by organizing data and offering helpful summaries and feedback.

- **Know It’s Beginner-Friendly**: I want to feel reassured that no advanced technical skills are needed to use the app.

- **Trust the Data Safety**: I want to gain confidence that data is securely stored in Google Sheets and easily accessible.

#### Returning users

- I want to feel supported by having one simple, organized place to manage my baby’s routine.
- I want to view summaries of sleep, feeding, and diaper data to spot patterns and track consistency.
- I want to update milestones as my baby reaches new developments.
- I want to log daily baby activities quickly using my username and password to protect my information.

## Features

### User Registration

1. Google Sheets Integration

**Secure Access**: Uses gspread with Google Service Account credentials to connect securely to your Google Sheets backend.
**Multi-Sheet Support**: Stores different data categories in separate sheets:
- user_info — Stores registered users and their babies’ info.
- daily_logs — Tracks daily sleep, feeding, and diaper counts.
- growth — Logs baby’s growth metrics (weight, height).
- milestones — Records baby developmental milestones.
- summary — Aggregates weekly summaries for each user.

This structure keeps user's data organized and easily extendable.

2. User Registration

**Unique Usernames**: Checks if the chosen username already exists to avoid duplicates.
**Baby Information**: Collects baby name, date of birth (validated to ensure proper date format), birth weight, and height.
**Age Calculation**: Automatically computes baby age in months from date of birth.
**Data Storage**: Saves all this info in the user_info worksheet.
**Input Validation**: Ensures all fields are entered correctly before saving, prompting users to correct mistakes.

This ensures accurate baseline data for each baby.

3. User Login System

**Username & Password Authentication**: Users log in with their username and password.
**Error Handling**: Gives clear feedback if username does not exist or password is incorrect.
**User-friendly Navigation**: Users can type q to quit or b to go back during input.
**Session Management**: Once logged in, user session data is loaded for personalized interactions.

This keeps data secure and users clearly informed.

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
- - Baby’s weight (kg)
Baby’s height (cm)

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

- Allow users to create profiles for multiple babies under the same account.
- Auto-save progress every few inputs to prevent data loss if the program closes unexpectedly.
- Record the exact time for each data entry, not just the date.
- Add password reset option.
- Allow users to export their baby’s logged data as CSV or simple text reports.


## Fixed Bugs 

* BUG:'Back'Option - When I typed 'b' to go back during data input (e.g., while entering sleep hours), the app exited the whole function instead of returning to the previous step. The 'b' input wasn’t being intercepted properly and was treated like any invalid input or passed through without a return handler.
**FIX**: I added input checking for 'b' in each step. When detected, the function now returns a 'back' signal, and the main loop handles re-displaying the previous prompt.

* BUG: Daily Logs Date Association - Daily logs stored in the Google Sheet did not contain a clear date, making it difficult to analyze trends or retrieve entries for a specific day.The append_row() function did not include a timestamp by default.
**FIX**: I introduced a timestamp using Python’s datetime module and prepended it to each row before storing.

* BUG: Invalid Input (e.g., Typing 'ten') - Entering non-numeric values for numeric questions (e.g., "ten" instead of 10) I caused a ValueError and crashed the app. int() or float() conversion was not wrapped in error handling logic.
**Fix**: I wrapped all numeric conversions in try/except blocks and looped until the user provided a valid value.

* BUG: "None" Milestone - When I entered None in the milestone input, the app still counted it as a valid milestone entry in the summary, inflating the count.The milestone logging function did not properly validate user input. The input 'None' was being appended to the milestone log and later included in summary statistics.
**FIX**: I added input validation to check for 'None' before saving a milestone.

## Unfixed Bugs

There are no fixed bugs according to me.

