

# techstars-scheduling-tool
Automates matchmaking of mentors and founders by availability and preference.
Goal: Automate processes for staff (Program Associate and Program Manager) to reduce time spent on matching startups to mentors.

# Steps
- [x] Create bot
- [ ] parse DM for csv attachment
- [ ] get private_download link
- [x] use requests to download csv
- [ ] route csv through data pipeline (pandas)
- [x] wrangle data
- [x] yield results (minimum)
- [x] put results in clean format (groupby 'Day', 'AM/PM')
- [x] return csv or error
- [x] message on success or error
	- [ ] send attachment on success
- [ ] Write instructions
- [ ] Create requirements.txt
- [x] Write report
# Inputs
- Name (First, Last), Object
- Day of Week, Categorical
- Time of Day (AM or PM), Binary
- Company 2
- Company 3
- Company 4
- Company 5
- Company 6
- Company 7
- Company 8

> 9 companies, Excess maually input by staff

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
	- Without knowing much more about Pandas operation efficiencies, must assume not efficient.
	- Not a big problem due to scale of the data having natural limitations
- Slackbot
	- Requires initial setup
	- Requires server to run continuously
	- May not be needed continuously if the functionality is limited to just this
		- With future features, would justify having continuously active bot
	- Made c

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
## Use Google Sheets API
- needs further authentication, credential information, won't work as standalone tool
- needs access to org's google apis to make a script and give permissions
- don't know exact format of document it will be used on (in sheets)

## Host webapp interface
- needs running web server. 
- needs front-end skills
- needs 

## CLI Tool
requirements:
- copy/pasting ability
- python
- multiple steps
- 


# Future
## Change to Inputs
- Reformat to use different schema
	- Name, Day, AM/PM, Companies (single list), Mentor's Zoom link
	- will help data processing
	- zoom info can be used for meeting template feature (reduces pain of next step)

# Data Processing
convert to pandas dataframe

create single company entries
- from John, Tu, AM, Co1, Co2, Co3
	- John, Tu, AM, Co1
	- John, Tu, AM, Co2
	- John, Tu, AM, Co3
