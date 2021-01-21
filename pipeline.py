import pandas as pd
import io
import sys
import os



## Lambda helper functions
def day_to_num (row):
    if row['Day'] == 'Monday': 
        return 0
    elif row['Day'] == 'Tuesday':
        return 1
    elif row['Day'] == 'Wednesday':
        return 2
    elif row['Day'] == 'Thursday':
        return 3
    elif row['Day'] == 'Friday':
        return 4
    else:
        return -1

def time_to_num(row):
    if row['AM/PM'] == 'AM':
        return 0
    elif row['AM/PM'] == 'PM':
        return 1
    else:
        return -1


def process_file(file):
    df = pd.read_csv(file)
    undefined = df[(df['Day'] == 'Undefined ') | (df['AM/PM'] == 'Undefined ') | (df['Day'] == 'Undefined') | (df['AM/PM'] == 'Undefined')]
    unassigned_mentors = undefined['Name'].values.tolist()
    defined = df[(df['Day'] != 'Undefined ') & (df['AM/PM'] != 'Undefined ') & (df['Day'] != 'Undefined') & (df['AM/PM'] != 'Undefined')]
    defined = defined.fillna('Drop')
    defined["Companies"] = defined['Company 2'] + ',' + defined['Company 3'] + ',' + defined['Company 4'] + ',' + defined['Company 5'] + ',' + defined['Company 6'] + ',' + defined['Company 7'] + ',' + defined['Company 8']
    pre_split = defined[['Name', 'Day', 'AM/PM', 'Companies']].copy()
    pre_split['Companies'] = pre_split['Companies'].str.split(',')
    post_split = (pre_split
                  .set_index(['Name', 'Day', 'AM/PM'])['Companies']
                  .apply(pd.Series)
                  .stack()
                .reset_index()
                .drop('level_3', axis=1)
                .rename(columns={0:'Company'}))
    post_split = post_split[post_split['Company'] != 'Drop']
    all_companies = post_split['Company'].drop_duplicates().to_list()
    defined_mentors = post_split['Name'].drop_duplicates().to_list()
    post_split['Mentor-Company'] = post_split['Name'] + ' - ' + post_split['Company']
    post_split['Mentor-Schedule'] = post_split['Name'] + ' - ' + post_split['Day'] + ' - ' + post_split['AM/PM']
    post_split['Company-Schedule'] = post_split['Company'] + ' - ' + post_split['Day'] + ' - ' + post_split['AM/PM']
    mentor_schedule = post_split.drop_duplicates(subset=['Mentor-Schedule'])
    company_schedule = mentor_schedule.drop_duplicates(subset=['Company-Schedule'])
    col1 = company_schedule.apply(day_to_num, axis=1)
    company_schedule = company_schedule.assign(DoW=col1.values)
    col2 = company_schedule.apply(time_to_num, axis=1)
    company_schedule = company_schedule.assign(ToD=col2.values)
    company_schedule['Full'] = company_schedule['Day'] + ' - ' + company_schedule['AM/PM'] + ' - ' + company_schedule['Mentor-Company']
    company_schedule = company_schedule.sort_values(by=['DoW', 'ToD'], ascending=[True, True])
    match_stats = company_schedule['Company'].value_counts().to_dict()
    matched_companies = match_stats.keys()
    assigned_mentors = company_schedule['Name'].to_list()
    unassigned_companies = list(set(all_companies) - set(matched_companies))
    pending_mentors = unassigned_mentors + list(set(defined_mentors) - set(assigned_mentors))
    try:
        company_schedule['Full'].to_csv('./matches.csv', index=False, header=False)
        return True, match_stats, pending_mentors, unassigned_companies # Success, meeting stats as dict, unassigned mentors, unassigned companies
    except:
        print("Failed to write file from pipeline")
        return [False, {}, [], []]


if __name__=="__main__":
    fname = sys.argv[1]
    with open(fname, 'r') as f:
        processed, match_stats, pending_mentors, unassigned_companies = process_file(f)
        if processed:
            print(f'Output file location: {os.path.abspath("matches.csv")}')
        print()
        print("Meetings per company:")
        for k,v in match_stats.items():
            print(f'{k}: {v}')
        print()
        print(f"{len(pending_mentors)} Mentors Unassigned:")
        for i in pending_mentors:
            print(f'-{i}')
        print()
        if len(unassigned_companies) == 0:
            print("Unassigned Companies: None")
        else:
            print("Unassigned Companies:")
            for j in unassigned_companies:
                print(j)






# For making list of pending mentors
#undefined = df[(df['Day'] == 'Undefined') | (df['AM/PM'] == 'Undefined ')]

# for showing how many mentors each company has
# matches = company_schedule['Company'].value_counts()
# matches

# for making list of all companies that have been assigned
#co_list = post_split['Company'].drop_duplicates()
