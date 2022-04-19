import re
import pandas as pd
from datetime import datetime
import datefinder
import numpy as np

# Create function that reads the letter and returns it as a string 
def readletter(lettertext):
    rletter = open(lettertext, 'r', errors='ignore')
    letter = rletter.read()
    rletter.close()
    return str(letter) 

releaseletter = readletter('release.txt')
noreleaseletter = readletter('norelease.txt')

# remove the footer and new page regex's 
def removefooter(letter):
    splitletter = letter.split('\n')
    for string in splitletter:
        for result in re.findall('info@paroleboard', string):
            splitletter.remove(string)
    joinletter = '\n'.join(splitletter)
    joinletter = joinletter.replace('\n\n\n\x0c', ' ')
    return joinletter

releaseletter = removefooter(releaseletter)
noreleaseletter = removefooter(noreleaseletter)

# ANONYMISATION
# Replace Months and Years with numeric dates 
date_regex = re.compile(r"(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})")

def replace_dates(s):
    new_s = s
    for match in date_regex.finditer(s):
        # First group is the whole match
        date_str = match[0]
        # Parse date, assume long month
        dt = datetime.strptime(date_str, "%B %Y")
        short_date_str = dt.strftime("%m/%Y")
        new_s = new_s.replace(date_str, short_date_str)
    return new_s

rel_date = replace_dates(releaseletter)
norel_date = replace_dates(noreleaseletter)

# Remove all examples of name but keep title 
def remove_name(letter):
    first_split = letter.split(":",1)[1]
    second_split = first_split.split('Decision')[0].strip()
    full_name = second_split.split(' ',1)[1]

    no_name_letter1 = letter.replace(full_name, 'X')
    no_name_letter2 = no_name_letter1.replace(full_name.split()[0], 'X')
    no_name_letter3 = no_name_letter2.replace(full_name.split()[1], 'X')
    
    return no_name_letter3

rel_anon = remove_name(rel_date)
norel_anon = remove_name(norel_date)


# EXTRACTION

def extract_letter_info(full_letter):
    # Divide letter into sections
    split_letter = 'HEADER ' + full_letter.replace('INTRODUCTION', '\nINTRODUCTION').replace('SENTENCE DETAILS', '\nSENTENCE DETAILS').replace('RISK ASSESSMENT', '\nRISK ASSESSMENT').replace('DECISION', '\nDECISION')
    letter = split_letter.split('\n')

    # Define required objects to be used throughout function 
    title_female = ['Miss', 'Mrs', 'Ms']
    title_male = ['Mr', 'Master']
    section_0 = letter[0]
    section_1 = letter[1]
    section_2 = letter[2]
    pattern_date = re.compile(r'\d{2}\/\d{4}')
    pattern_vps = re.compile(r'[Vv]ictim [Pp]ersonal [Ss]tatement|VPS')
    types = []

    # Save gender value
    split1 = section_0.split(':',1)[1]
    split2 = split1.split('Decision',1)[0].strip().split()[0]
    for title in title_female:
        if split2 == title:
            gender = 'Female'
        else: 
            for title in title_male:
                if split2 == title:
                    gender = 'Male'

    # Decision
    decision = section_0.split('Decision:',1)[1].strip()

    # Date of current hearing
    hearing_dates = pattern_date.findall(section_1)
    date_of_hearing = hearing_dates[0]

    # Multiple hearings? 
    if len(hearing_dates) == 1:
        hearing_amount = 'No'
    elif len(hearing_dates) >1:
        hearing_amount = 'Yes'
    else:
        hearing_amount = np.nan 

    # Previous hearing(s) date
    if len(hearing_dates) == 1:
        prev_hearing_dates = 'No previous hearing'
    elif len(hearing_dates) > 1 :
        prev_hearing_dates = hearing_dates[1:]
    else:
        prev_hearing_dates = np.nan

    # VPS
    vps_eg = pattern_vps.findall(section_1)
    if len(vps_eg) != 0:
        vps = 'Yes'
    else:
        vps = 'No'

    # Sentence date
    sentence_date = pattern_date.findall(section_2)[0]

    # Sentence type
    if 'life sentence' in letter[2].lower():
        types.append('life')
    if 'determinate' in letter[2].lower():
        types.append('determinate')
    if 'indeterminate' in letter[2].lower():
        types.append('indeterminate')
    # Add more as necessary
    sentence_type = types

    data = {'Gender': gender, 'Decision': decision, 'Hearing_date': date_of_hearing, \
        'Multiple_hearings': hearing_amount, 'Previous_hearing_date': prev_hearing_dates, \
        'VPS': vps, 'Conviction_date': sentence_date, 'Sentence_type': sentence_type}

    return data

all_letters = [rel_date, norel_date]

def turn_into_df(letter_list):
    results = [extract_letter_info(letter) for letter in letter_list]
    data = pd.DataFrame.from_records(results)
    return data















