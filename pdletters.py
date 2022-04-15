import re

# Create function that reads the letter and 
def readletter(lettertext):
    rletter = open(lettertext, 'r', errors='ignore')
    letter = rletter.read()
    rletter.close()
    return str(letter) 

releaseletter = readletter('release.txt')
noreleaseletter = readletter('norelease.txt')

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




