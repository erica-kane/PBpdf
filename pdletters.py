import re
from datetime import datetime

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


# Split string into sections (header, introudction, sentence details, risk assessment, decision)
def split_letter_sections(letter):
    split_letter = 'HEADER ' + letter.replace('INTRODUCTION', '\nINTRODUCTION').replace('SENTENCE DETAILS', '\nSENTENCE DETAILS').replace('RISK ASSESSMENT', '\nRISK ASSESSMENT').replace('DECISION', '\nDECISION')
    section_letter = split_letter.split('\n')
    return section_letter

split_rel = split_letter_sections(releaseletter)
split_norel = split_letter_sections(noreleaseletter)


# Use title for gender 
# Decision regex 





