

# techstars-scheduling-tool
Automates matchmaking of mentors and founders by availability and preference.
Goal: Automate processes for staff (Program Associate and Program Manager) to reduce time spent on matching startups to mentors.

# Steps
- [x] Create bot
- [x] parse DM 
	- [x] private_link
	- [x] channels
	- [x] filename
	- [x] filetype
- [x] use requests to download csv
- [x] route csv through data pipeline (pandas); from pipeline import process_data
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
- [ ] Take screenshots
- [x] Write report

# Minimum Output: Schedule of meetings between mentors and companies
- Schedule of meetings between mentors and companies
- They then send calendar invites for each meeting (by hand)

# Constraints
- Mentor is not booked with two companies at same time
- Startup not booked with more than one mentor at same time

# Current Solution
- Giant, color-coded google sheets
- 2-person job (Associate with Manager supervising)
- 10-day turnaround
- done yearly
- edge cases:
	- rescheduling/canceling shortly before meeting

# My Solution
## MVP
- Slackbot in collaboration channel that produces CSV in-channel for easier collaboration.
## Future Features
- google sheets integration 
	- Direct slack-google solution
	- Zapier interface
- Meeting Details automation (program manager only)
	- takes csv and uses user's credentials to 
	- add mentor zoom information
	- google calendar api tie-in
	- single-use for initial batch

## Weaknesses
- Algorithm
	- Isn't currently optimized for even distribution of mentors to companies.
	- The current implementation has space complexity of O(~20n) when data is expanded, not including cost of pandas's operations.
	- Not a big problem due to scale of the data having natural limitations (# of companies in incubator)
- Slackbot
	- Needs dev/tech support for initial setup
	- Requires server to run continuously
		- would be justifiable if slack bot expands functionality to include automation of sending meeting invitations
		- could be added to company's existing bot, if any

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
#
- retain google sheets integration for easy transition for users
- use google sheets api to get data
- process data with python
	- check if zoom-link is included or not
- Create new sheet with a proposed schedule
	- Maybe add Color-coding for finalized and unfinalized 
- PDF and sheets/csv generation

Workflow
1. Send csv to @matchmaker \<format>
	- Example:
		- `@matchmaker csv`
		- `@matchmaker pdf, csv`
2. matchmaker backtracks and finds solution
3. solution is exported and formated to desired export format
	1. csv
	2. google doc
	3. pdf
	4. json
4. links returned to user

# Why nots
## CLI Tool
- Great solution for this single task but doesn't have the same potential for future functionality as the slack bot
- Command-Line tools can scare people. Tool is useless if no one uses it or uses it only once.
- Still needs user to modify workflow for this task. 
## Use Google Sheets API
- Similar setup admin requirements as slack bot, and could interface with workflow better.
- Isn't as flexible as pandas and coded algorithms
- Code can't be reused or ported to other interfaces easily.

## Host webapp interface
- needs front-end skills
- interrupts user's current workflow (as would cli tool)


