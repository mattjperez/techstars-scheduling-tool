

# techstars-scheduling-tool
Automates matchmaking of mentors and founders by availability and preference.
Goal: Automate processes for staff (Program Associate and Program Manager) to reduce time spent on matching startups to mentors.

# Requirements
- Constraints
	- Mentor is not booked with two companies at same time
	- Startup not booked with more than one mentor at same time
- MVP
	- Yields tentative schedule according to constraints

# Current Solution
- Giant, color-coded google sheets
- 2-person job (Associate with Manager supervising)
- 10-day turnaround
- done yearly
- edge cases:
	- rescheduling/canceling shortly before meeting

# My Solution
Slackbot that accepts the input file via direct message and returns output file with supplemental information.

## Strengths
- Speed and Accuracy
	- This solution yields a tentative schedule that is guaranteed not to double book times or mentors and companies.
- Seamless Integration
	- The slackbot is easily accessible. Results can easily be forwarded to relevant channels and users.
	- Can easily be ported as additional functionality of existing slack bot
- Potential
	- Can expand functionality to assist in sending meeting invitations to mentors and companies.
	- Provides base for an internal tool.
	- User-Specific Commands
		- ex. Only Mary(Slack ID:23849) can utilize the "Send Meeting Invitations" command
- Flexibility
	- Includes command-line tool for immediate usage or until slack bot becomes fully functional.

## Weaknesses
- Algorithm / Data Processing
	- Is not a complete solution, however yields actionable results much faster than traditional state space search methods and provides additional information to assist users in completing the task.
		- Could possibly be replaced with graph-based algorithm or Machine-Learning alternative.
	- Isn't currently optimized for even distribution of mentors to companies.
	- The current implementation has space complexity of O(~20n) when data is expanded, not including cost of pandas's operations.
		- Not a big problem due to scale of the data having natural limitations (# of companies in incubator)
- Slackbot
	- Needs dev/tech support for initial setup
	- Requires server to run continuously
		- would be justifiable if slack bot expands functionality to include automation of sending meeting invitations
		- could be added to company's existing bot, if any
## Future Features
- google sheets integration 
	- Direct slack-google solution
	- Zapier interface
- Meeting Details automation (program manager only)
	- takes csv and uses user's credentials to 
	- add mentor zoom information
	- google calendar api tie-in
	- single-use for initial batch
# Data Processing
1. create single company entries
	- John, Tu, AM, Co1, Co2, Co3 ->
		- John, Tu, AM, Co1
		- John, Tu, AM, Co2
		- John, Tu, AM, Co3
2. Expand to include combination columns
	- John, Tu, AM, Co1, John-Co1, John-Tu-AM, Co1-Tu-AM
3. Use sieve approach to wittle list so no Mentors or Companies are double booked
	- df['Mentor-Schedule'].drop_duplicates()
	- df['Company-Schedule'].drop_duplicates()
4. Sort by Day and Time, export to csv
5. Return csv, # of meetings per company, unassigned mentors, and companies without meetings

# Why nots
## Google Sheets API
- Similar setup admin requirements as slack bot, and could interface with workflow better.
- Isn't as flexible as pandas and coded algorithms
- Code can't be reused or ported to other interfaces easily.

## Webapp
- needs front-end skills
- still needs tech skills for initial setup for users
- interrupts user's current workflow
- not as convenient as cli tool for fast one-time use

# Steps
- [x] Create bot
- [x] parse Direct Message to bot 
	- [x] private_link
	- [x] channels
	- [x] filename
	- [x] filetype
- [x] use requests to download csv
- [x] route csv through data pipeline (pandas)
- [x] wrangle data
- [x] yield results (minimum)
	- [x] reformat output without expanded data
	- [x] put results in clean format (groupby 'Day', 'AM/PM')
- [x] return csv
- [x] create post keys
	- [x] filename
	- [x] filetype
	- [x] channels
	- [x] auth
- [x] Write instructions
- [x] Create requirements.txt
- [x] Write report