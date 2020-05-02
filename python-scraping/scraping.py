from collections import namedtuple
import csv
import requests
from bs4 import BeautifulSoup

# US state codes; add territory codes here if desired
REGION_CODES = {
    'Alabama' : 'AL',
    'Alaska' : 'AK',
    'Arizona' : 'AZ',
    'Arkansas' : 'AR',
    'California' : 'CA',
    'Colorado' : 'CO',
    'Connecticut' : 'CT',
    'Delaware' : 'DE',
    'District of Columbia' : 'DC',
    'Florida' : 'FL',
    'Georgia' : 'GA',
    'Hawaii' : 'HI',
    'Idaho' : 'ID',
    'Illinois' : 'IL',
    'Indiana' : 'IN',
    'Iowa' : 'IA',
    'Kansas' : 'KS',
    'Kentucky' : 'KY',
    'Louisiana' : 'LA',
    'Maine' : 'ME',
    'Maryland' : 'MD',
    'Massachusetts' : 'MA',
    'Michigan' : 'MI',
    'Minnesota' : 'MN',
    'Mississippi' : 'MS',
    'Missouri' : 'MO',
    'Montana' : 'MT',
    'Nebraska' : 'NE',
    'Nevada' : 'NV',
    'New Hampshire' : 'NH',
    'New Jersey' : 'NJ',
    'New Mexico' : 'NM',
    'New York' : 'NY',
    'North Carolina' : 'NC',
    'North Dakota' : 'ND',
    'Ohio' : 'OH',
    'Oklahoma' : 'OK',
    'Oregon' : 'OR',
    'Pennsylvania' : 'PA',
    'Rhode Island' : 'RI',
    'South Carolina' : 'SC',
    'South Dakota' : 'SD',
    'Tennessee' : 'TN',
    'Texas' : 'TX',
    'Utah' : 'UT',
    'Vermont' : 'VT',
    'Virginia' : 'VA',
    'Washington' : 'WA',
    'West Virginia' : 'WV',
    'Wisconsin' : 'WI',
    'Wyoming' : 'WY'
}

BASE_URL_PREFIX = 'http://www.uspto.gov/web/offices/ac/ido/oeip/taf/stcteca/'
BASE_URL_SUFFIX = 'stcl_gd.htm'

MASTER_LIST = []
StateRow = namedtuple('StateRow', 'state_name tech_code year value')

# for each state code, generate the target URL and pull the data
for state in sorted(REGION_CODES):
    print('Processing data for ' + state)
    path = BASE_URL_PREFIX + REGION_CODES[state].lower() + BASE_URL_SUFFIX
    r = requests.get(path)
    soup = BeautifulSoup(r.text, "html.parser")

    # skip first and last rows, which are headers and totals respectively
    for table_row in soup.find_all('tr')[1:-1]:
        tech_code = table_row.find('td', style=' text-align: left; ').string.strip()
        year = 1963
        # skip the last element, which is a total; we can aggregate the data ourselves
        for value in table_row.find_all('td', {'style': None})[:-1]:
            row = StateRow(state, tech_code, year, value.string.strip())
            MASTER_LIST.append(row)
            year = year + 1
            break
        break
    break

#SCRAPING TECH CODES AND NAMES
URL = 'http://www.uspto.gov/web/patents/classification/selectnumwithtitle.htm'
TECH_CODES = []
ClassRow = namedtuple('ClassRow', 'class_code class_name')

#SCRAPING TECH CODE TABLE
#We pass the URL we defined to requests and parse through Beautiful Soup. We now loop through HTML table tags and pull values based on our named tuple function.
REQUEST = requests.get(URL)
SOUP = BeautifulSoup(REQUEST.text, "html.parser")

print('Scraping data')
for table_row in SOUP.find_all('tr'):
    class_code_tag = table_row.find('td', width='27')

    # not a class_code + name row. skip
    if class_code_tag is None:
        continue

    class_code = class_code_tag.string
    class_name = table_row.find('td', width='532').string
    TECH_CODES.append(ClassRow(class_code, class_name))

#EXPORTING TO CSV
# write out to csv
with open('./state_tech.csv', 'w', newline='') as out:
    print('Writing data to ' + out.name)
    CSV_FILE = csv.writer(out, delimiter=',')
    CSV_FILE.writerow(['Region', 'Tech Class Code', 'Year', 'Utility Patent Count'])
    CSV_FILE.writerows(MASTER_LIST)
    
with open('./tech_code.csv', 'w', newline='') as out:
    print('Writing data to ' + out.name)
    CSV_FILE = csv.writer(out, delimiter=',')
    CSV_FILE.writerow(['Class Code', 'Class Name'])
    CSV_FILE.writerows(TECH_CODES)
    