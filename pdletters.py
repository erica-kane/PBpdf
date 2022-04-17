import re
from datetime import datetime
import datefinder

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

# Information to extract:

# From header - 
# Name (remove)
# Gender
# Decision 

# From Introduction - 
# Date of hearing(s) 
# Victim personal statement 

# From Sentence details - 
# Sentence type(s)
# Sentence length(s)

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
# Regex for everything between 'Name: title' and 'Decision:'
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

# Split string into sections (header, introudction, sentence details, risk assessment, decision)
def split_letter_sections(letter):
    split_letter = 'HEADER ' + letter.replace('INTRODUCTION', '\nINTRODUCTION').replace('SENTENCE DETAILS', '\nSENTENCE DETAILS').replace('RISK ASSESSMENT', '\nRISK ASSESSMENT').replace('DECISION', '\nDECISION')
    section_letter = split_letter.split('\n')
    return section_letter

split_rel = split_letter_sections(rel_anon)
split_norel = split_letter_sections(norel_anon)


# Use title for gender 
def get_gender(letter):
    title_female = ['Miss', 'Mrs', 'Ms']
    title_male = ['Mr', 'Master']
    eg = letter[0]
    split1 = eg.split(':',1)[1]
    split2 = split1.split('Decision',1)[0].strip().split()[0]

    for title in title_female:
        if split2 == title:
            gender = 'female'
        else: 
            for title in title_male:
                if split2 == title:
                    gender = 'male'

    return gender

get_gender(split_rel)

# Decision
def get_decision(letter):
    eg = letter[0]
    split = eg.split('Decision:',1)[1].strip()
    return split

get_decision(split_norel)

# Date of hearing 
# regex for 2 numbers slash 4 numbers 
pattern = re.compile(r'\d{2}\/\d{4}')
pattern.findall(split_rel[1])


# Previous hearing 









