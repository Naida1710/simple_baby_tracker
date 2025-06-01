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

1. User Registration

Register new users with unique usernames.

Collect user details including:
- Username and password
- Baby’s name
- Baby’s date of birth (DOB)
- Baby’s birth weight and height

Validate input formats (e.g., date format YYYY-MM-DD, numeric input for weight/height).
Prevent duplicate usernames.
Calculate baby’s current age in months based on DOB.


2. User Login

Login with username and password.
Validate credentials against stored user data.
Friendly error messages for invalid username or password.
Option to quit or go back during login.


3. Daily Baby Data Logging

Log daily details for a specific date:
Sleep hours (float)
Feed amount in milliliters (float)
Number of wet diapers (integer)
Number of dirty diapers (integer)
Validate input formats and allow going back to correct entries.
Save daily logs to the Google Sheets daily_logs worksheet.

4. Growth Data Logging

Record baby’s growth measurements on a given date:
Weight in kilograms (float)
Height in centimeters (float)
Validate input formats and allow navigation back during input.
Save growth data to the growth worksheet.

5. Milestone Logging

Log developmental milestones with:
Date of milestone
Description of milestone
Validate date format and allow going back in inputs.
Save milestone entries to the milestones worksheet.

6. User Profile Display

View registered user profile including:
Username
Baby’s name
DOB and age in months
Birth weight and height

7. Summary Display

Show a user-specific summary from the summary worksheet.
Displays various tracked metrics and notes.

8. Summary Sheet Update

Generate weekly summaries for all users including:
Total sleep hours logged in the past 7 days.
Average feed amount (ml) over the past week.
Number of milestones achieved.
Latest recorded weight and height.
Clear and recreate the summary sheet each time it is updated.

9. User Input Handling

Input prompts with support for:
Quitting anytime by typing 'q'.
Going back to previous input by typing 'b'.
Input validation with user-friendly error messages.
Use of colored terminal output for better user experience (via colorama).

10. Security and Usability

Password verification during login.
Input sanitization and validation.
Friendly navigation allowing users to correct mistakes.



