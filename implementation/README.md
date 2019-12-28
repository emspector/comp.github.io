Name: Emily Spector
Project: a Web Hub for the WHRB Tech Comp

### User Manual ###

# Technical Information
This website can be run locally in the CS50 IDE using the following SQL, Python, HTML, and CSS files, contained in the folder "application":
- comp.db
- application.py, helpers.py
- about.html, admin.html, apology.html, assignments.html, attendance.html, index.html, layout.html, login.html, password.html, people.html, register.html, submit.html
- style.css
- .pylintrc

Design documentation is contained in DESIGN.md

# Overview
The site is designed for the Spring 2020 WHRB Tech comp class and will serve both compers and comp-directors as an organizational tool.

It will provide compers with a centralized place where they can view information about the comp, log their attendance at comp meetings and office hours,
keep track of upcoming events, check assignment descriptions, submit their work, find contact information and links to important documents and sites,
and become familiar with their peers in the comp.

The site will provide comp-directors with a centralized place in which to keep track of compers' attendance, collect all assignments in one place,
leave comments on assignments, compile a centralized list of comper contact information and addresses (for use at the end of the comp), be able to alert all
compers of new information without risking an email going unnoticed, and help the compers stay organized, making for a better, more efficient comp.

# Register and Login
Upon arriving on the site for the first time, a user should register, creating a profile for themself. Notably, there is no field to choose a password when registering,
and this is for security purposes. Only those who are verified as part of the comp will be told their default password, which they can then change after logging in.

The default password is: herbiewhrbie953

For the purpose of this assignment, if a user would like to log into an example comper profile that is already populated with assignment submissions
and attendance records, they may use the following credentials:
Email: riley@test.com
Password: comper

If a user would like to log into my comp director (admin) profile, they may use my credentials:
Email: emilyspector@college.harvard.edu
Password: compdirector

# Change Password
If the user would like to change their password, they can click "change password" on the left side of the navigation bar. There, they can affirm their authority to do so
by correctly enterring their old password, and then they may specify a new password.

# Dashboard
Once a user has logged in, they will find themselves at their # dashboard.
The top section alerts the user to upcoming assignments, meetings, and events.
The left-most and middle sections provide user-specific information: an attendance record and an assignment record.
The right-most section provides a list of useful links, including one to join the comper GroupMe chat, one to the WHRB tech activity log, one to the WHRB tech documents folder
one to the studio reservation calendar, and one to our station's professional externally facing website.

Additionally, there is a button at the bottom of the page which will create an email message to the three comp directors.

# About
The About page is a simple page providing users with an overview of the comp and a brief section at the bottom describing the site's intended uses

# Attendance
On the Attendance page, a user can mark themselves present for the meetings and office hours at which they are present.
If a user attempts to mark themself present at the same event twice, the second attempt will be discarded.
Note: each submission will be carry with it a timestamp that the comp directors will be able to view on their administrative interface.
The user's personal attendance log will appear on the page below the input field.

# Assignments
Users can find a list and description of the out-of-class work that is expected of them on the Assignments page.
However, at the top right corner of the list, users can navigate to the submission portal.

# Submit
On the Submit page, which a user can navigate to through the Assignments page, users can select the assignment they have completed from the menu and submit a
link to their work. Like attendance records, these submissions also carry with them a timestamp. If a user attempts to submit a link for an assignment to which
they've already submitted, their initial submission will be overriden and replaced with the new link.
The user's submission records will be included on the page below the input field.

# People
The People page serves as a comp directory, organizing the names, pronouns, dorms/houses, and email addresses of compers and comp directors.
For privacy's sake, phone numbers are only included for comp directors; compers' phone numbers are accessible only to the comp directors.

# Admin
Only the accounts registered to a comp director's email address can access the Admin page.
The Admin page is the page is of great use to comp directors.

The top of the page organizes the compers alphabetically, and each comper's name is followed by
their pronouns, email address, and phone number. Below that are two logs: one of their attendance and one of their assignment submissions.
The attendance log differs from that which the comper can see on their dashboard in that it includes the time stamp.
The submission log also differs from the comper's dashboard display in that it includes a short comment, to be left by a comp director, called the "evaluation."
The evaluation's default value is "TODO," and if it has not yet been altered, comp directors see a small input form into which they can enter their comments.
Upon entering a comment, the input field disappears and the comment replaces "TODO" in the submission log.
The submission log also includes the link that the comper submitted to their work as well as a time stamp marking when it was submitted.

Below all the information on the compers' profiles, attendance, and assignments is a list of their emails, formatted such that the entire list
can simply be copied and pasted into an email service. The list also includes tech@whrb.org and the comp directors' addresses.

Below the email list is a list of the compers' dorms and room addresses, so that the information is easily accessible when the comp finishes and it
is time to collect the compers from their rooms for the celebratory initiation ceremony.

Finally, the Admin page includes a form which a comp director can use to remove a comper from the comp. Since emails are verified to be unique during the
registration process, the comp director must simply enter the email address of the comper whom they wish to delete, and all records corresponding to that
comper will be removed from the databases and interface.