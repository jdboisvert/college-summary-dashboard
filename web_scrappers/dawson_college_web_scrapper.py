import requests
from bs4 import BeautifulSoup 
import json
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def parse_program_page(url):
    
    #This is just to make it so the request goes through and the Dawson website does not decline it 
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'referrer': 'https://google.com'
    }
    
    # URL of program page for pure and applied
    r = requests.get(url, headers=headers)
    
    if (r.status_code == requests.codes.ok):
    
        # Get HTML of the page
        html = r.text.strip()

        # Make html of page a BeautifulSoup 
        soup = BeautifulSoup(html, 'lxml')
    
        programDateMod = getDateOfMods(soup)
    
        #Page data to be returned
        pageData = {
            'date': programDateMod
        }
    
        return pageData
    else: 
        return '404'

#Get the date of when the page was last modified
def getDateOfMods(soup):
    # Get when last modified
    dateModified = soup.find(class_='page-mod-date').contents[0].strip()
    # Remove the 'Last Modified: ' field so just date is left
    dateModified = dateModified[15:]
    return dateModified

def createSoup(url):
        #This is just to make it so the request goes through and the Dawson website does not decline it 
        headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com'
        }
    
        # URL of program page for pure and applied
        r = requests.get(url, headers=headers)
    
        # Get HTML of the page
        html = r.text.strip()
    
        # Make html of page a BeautifulSoup 
        soup = BeautifulSoup(html, 'lxml')
        return soup

#Gets all the programs on the Dawson page
def getPrograms(url):
        # An array to hold all the programs retrieved
        programs = []

        soup = createSoup(url)
    
        content = soup.find(class_='entry-content')
    
        #Get all the rows
        trTags = content.find_all('tr')
    
        #Loop through each row
        for tr in trTags:
        
            #Means a program continue (not a heading)
            if(tr.find(class_='program-name')):
                #Get program url 
                programUrlEnd = tr.find(class_='program-name').find('a')['href']
                #Not an actual program 
                if programUrlEnd == '/programs/general-education':
                    continue
                programUrl = 'https://www.dawsoncollege.qc.ca/' + programUrlEnd
                #Get page info
                pageInfo = parse_program_page(programUrl)
                #Add program type
                #If 404 means page was not found so skip
                if (pageInfo == '404'):
                   continue
                if tr.find(class_='program-type'):
                    try:
                        pageInfo['type'] = tr.find(class_='program-type').contents[0].strip()
                    #Since not a program and details are not present just continue
                    except: 
                        continue
                    pageInfo['programName'] = tr.find(class_='program-name').find('a').contents[0].strip()
                    pageInfo['url'] = programUrl; 
                    programs.append(pageInfo)
        
        return programs

# Gets amount of given type
def getNumberOfType(df, wantedType):
    #Get number of programs
    mask = df['type'] == wantedType
    number = len(df[mask])
    return number

#Function get the number of students at Dawson College
def getNumberOfStudents():
    soup = createSoup('https://www.google.com/search?q=dawson+college+number+of+students&stick=H4sIAAAAAAAAAOPgE-LUz9U3MLTMKjbV0s8ot9JPzs_JSU0uyczP088vSk_My6xKBHGKrfJKc5NSixTy0xSKS0pTUvNKihexKqYklhfn5ymANaWnKmCqAQDR74rvYgAAAA&sa=X&ved=2ahUKEwjXvq6b97XjAhUaQ80KHTRfCb8Q6BMoADAgegQIGhAC&biw=1156&bih=754')
    tag = soup.find(class_='Z0LcW')
    #Get content with leading or trailing space
    content = tag.contents[0].strip()
    #Remove commas in the number and cast to an int
    contentCasted = int(content.replace(',', ''))
    return contentCasted

def getNumberOfFaculty():

    params = {"position" : "Faculty", 
            "search" : "Search"}
    head = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}

    url = "https://www.dawsoncollege.qc.ca/phone-directory"
    res = requests.post(url, data=params, headers=head)
    soup = BeautifulSoup(res.text,"html.parser")
    tags = soup.find_all('b')
    return int(tags[0].contents[0])

# Main function
def init():
    programs = getPrograms('https://www.dawsoncollege.qc.ca/programs/alphabetical-listing')

    #Getting number of students
    numberOfStudents = getNumberOfStudents()

    #Getting number of faculty 
    numberOfFaculty = getNumberOfFaculty()

    #Number of students per faculty 
    numberStudentsPerFaculty = round((numberOfStudents / numberOfFaculty), 2)

    #Convert data to dataframe for easier time for stats
    df = pd.DataFrame(programs)

    print(df)

    #Change date to actual Timestamp type
    df['date'] = pd.to_datetime(df['date'])

    #First get number of different things offered at Dawson
    totalOffered = len(df)

    #Main stats of amounts
    numberPrograms = getNumberOfType(df, 'Program')
    numberProfiles = getNumberOfType(df, 'Profile')
    numberDisciplines = getNumberOfType(df, 'Discipline')
    numberSpecial = getNumberOfType(df, 'Special Area of Study')
    numberGeneral = getNumberOfType(df, 'General Education')
    
    #Add just year to column
    year = []
    for date in df['date']:
        year.append(date.year)

    df['year'] = year

    yearCounts = df['year'].value_counts()

    #Now programs sorted by
    newest = df.sort_values(by='date', ascending=False)
    newest = (newest.drop('year', axis=1)).reset_index(drop=True)

    # Convert to json with to_json(orient='split')
    # Use the json module to load that string to a dictionary
    json_dict = json.loads(newest.to_json(orient='split'))

    # Delete the index key with del json_dict['index']
    del json_dict['index']

    # Convert the dictionary back to json with json.dump or json.dumps
    newestJSONStr = json.dumps(json_dict)

    programStats = {
    
    'Total' : totalOffered,
    'Number of Programs' : numberPrograms,
    'Number of Profiles' : numberProfiles,
    'Number of Disciplines' : numberDisciplines,
    'Number of Special' : numberSpecial,
    'Number of General' : numberGeneral,
    'Year Counts' : yearCounts.to_json(),
    'Programs ordered newest' : newestJSONStr,
    'Number of Students' : numberOfStudents,
    'Number of Faculty' : numberOfFaculty,
    'Number of Students per Faculty' : numberStudentsPerFaculty
    
    }

    with open('static/data/dawson_programs_stats.json', 'w') as f:
        json.dump(programStats, f)

if __name__ == "__main__":
    init()
