Name: Emily Spector
Project: a Web Hub for the WHRB Tech Comp

### Design Documentation ###

# Concept
This website was built on the infrastructure of CS50 Finance and is designed to be simple and painless for compers and comp-directors to use.
I chose to create this site after hearing my compers' feedback on the comp I ran this fall and reflecting on my own experience as a comp director.
Compers said it was difficult to keep track of emails and assignments and feel like they were clear about what was going on and what they were expected to do.
My co-comp director and I felt it was similarly difficult to keep track of submissions and attendance and send emails on time.
This site should address all of those problems, allowing for one centralized place that we can all collect the information we need.

# Components
This site integrates flask applications written in python with HTML, CSS, and SQL.

It relies on a SQL database called "comp.db", which contains three tables:
profiles, with fields for user id, name, pronouns, phone number, email address, password hash, dorm or house, and room and entryway
attendance, with fields for user id, event, and timestamp
assignments: with fields for user_id, assignment name, submission link, timestamp, evaluation comment, and submission id

# Layout / Aesthetic
This site was designed to fit into the exist WHRB aesthetic, which prioritizes informal text (lowercase, comic sans) and often uses a red / maroon color scheme.
The links become bold when moused over in order to let the user know the site is alive and reactive; I've noticed that websites that don't acknowledge mouse activity
can look suspiciously inactive and cause concern of bad internet connetion.

Each page also includes an acknowledgement of which user is signed in, motivated by my confusion when I was signing in and out of different profiles trying things out.

# Register, Log In, Change Password
In order to allow the site to have personal information, I wanted to build it in such a way that it would be protected from people who shouldn't have access.
To accomplish this, users do not choose their own first password but instead have to use a default password, which they will only recieve if they are
actually enrolled in the comp. Once they register and log in for the first time, they can change their password to one of their choice.

# Dashboard
The dashboard is designed to let compers keep track of their own progress through the comp, as well as stay aware of what is coming up next, have access to useful links,
and have an easy way to send the comp directors emails as well.

The top portion of the dashboard includes hardcoded events, which comp directors will have to update weekly or as needed.
However, the attendance and submissions sections populate from the attendance and assignments SQL tables, although they provide only the name of the assignment
that was submitted or of the event that was attended in order to keep the interface clean and clear to the user.

The "email magic button" at the bottom constructs a blank email to the three comp directors when clicked using a mailto: link.

# About
Design-wise, the about page is very simple; it is just text that helps orient students both to the comp and to the site.

# Attendance
Last semester, it was extremely difficult to take attendance in an organized way that wasn't incredibly
time consuming. Additionally, not all comp-directors were present at the same events, so it was difficult to remember
to communicate which students had been at what. On this page, comper's can log their own attendance.

Compers select an event (meeting or office hours) from a drop-down menu here in order to mark themselves present. The event is then enterred into the attendance
table along with the user's user id number and a timestamp.

The timestamp is intended to allow comp directors to keep an eye on any suspicious attendance logging without compers knowing;
it would have been possible to add a special password for each event that needed to be enterred in order to log attendance,
but that seemed to be in bad faith. I decided that it was more important in the spirit of WHRB to show
compers that we trust them than to monitor them as though they are going to lie. If they did lie about attendance, comp directors would probably notice
since it isn't that large of a group, and the timestamp could tip them off too.

Also, even if a user marks themself present at the same event twice by accident, it is designed such that later attempts after the first one
will be discarded so as not to clog up the interface.

# Assignments
This is also a largely text-based page, which contains a list of all the upcoming assignments and descriptions of how to do them.

# Submit
Last semester, it was also quite difficult to keep track of compers' assignments. Some would email them in to our various email accounts, and others would use
the Google Drive portals that we set up, which ended up having a lot of trouble with clear filing name. This feature will allow the compers' assignments
to remain closely tied to their own names and will be accessible to the comp directors on the admin page.

The submit page, accessible through the assignments list, allows compers to select the appropriate assignment from the list, enter in a link
to their work, and submit it.

Below the input field, they can see a log of their submissions and the links they submitted.

If a comper resubmits an asssignment, the new link will replace the old one; this was done in order to prevent any ambiguity over which assignment was the "right" one
when the comp directors go to evaluate the compers' work.

The assignment submissions also carry timestamps with them so that the comp directors can ascertain that they were turned in on time. Additionally, the assignments
also carry with them the user's user id, of course, and also a unique submission id. This is so that the individual assignments can be easily accessed
on the admin page when the comp directors need to input evaluation comments.

# People
This directory uses information from the profiles table to populate two lists: one of comp directors and one of compers.
Since it is known who the comp directors are, their emails can be hard-coded into loops so that their profiles can be differentiated from those of the compers.
Additionally, compers' phone numbers and room numbers are withheld from this list for privacy reasons; their addresses are to only be used by comp directors
when collecting compers from their rooms at the end of the comp for initiations celebrations, and their phone numbers are only so they can be added to group chats.
However, the comp director's phone numbers will be available to the compers.

# Admin
As I mentioned when discussing the Attendance page, it was difficult last semester for multiple comp directors
to communicate regularly about which events compers were showing up to. Additionally, assignments would regularly get lost in a variety of email inboxes and Google Drives.
We also struggled to help everyone get added to a comper group chat, and rushed at the last minute to collect addresses for the end-of-comp celebration.

The Admin page is where all of the information collected comes together so that the comp directors can keep a close eye on the progress of compers
in terms of their attendance and their submissions and solve the above-mentioned logistical problems. It is accessible only to the comp directors, and verifies
their identities using their email addresses.

The page organizes each comper's attendance and submissions under a heading of their name, pronouns, email, and phone number. It displays the attendance log with
timestamps, and submissions with the title of the assignment and link to submission. submissions that haven't yet been evaluated with a short comment from the comp
directors offer a form that they can use to fill in the evaluation field.

Below the comper information blocks is an email list that includes the tech department email list and comp director email lists, formatted such that the whole list
can simply be copied and pasted into the "to:" field in an email. This will streamline the process of sending out comp emails.

Additionally, there is a list of compers and their addresses to help with dorm-storm plans at the end of the comp.

And finally there is an option for comp directors to remove a comper from the website; often, not all compers finish the comp, and when this is the case,
this feature will be helpful in cleaning up the noise of their dead profile instead of just letting it sit there. Since all the emails are verified as unique
during registeration, first the email of the comper is enterred, which can be used to locate their user id. Then that id is used to delete them from
all three (profiles, attendance, assignments) tables.

