import pandas as pd
import io


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

    try:
        company_schedule['Full'].to_csv('./matches.csv', index=False)
        return True
    except:
        print("Failed to write file from pipeline")
        return False


# For making list of pending mentors
#undefined = df[(df['Day'] == 'Undefined') | (df['AM/PM'] == 'Undefined ')]

# for showing how many mentors each company has
# matches = company_schedule['Company'].value_counts()
# matches

# for making list of all companies that have been assigned
#co_list = post_split['Company'].drop_duplicates()
