# get all problem codes from a kattis contest:
import requests
from bs4 import BeautifulSoup
import re

# set link to kattis contest 'problems' page
problem_page = 'https://open.kattis.com/contests/asoyyf/problems'
response = requests.get(problem_page)
problemCodes = []

def getProblemTable(soup):
    # find the problem table
    attrName = 'data-cy'
    attrValue = 'problem-table'
    table = soup.find('table', {'data-cy': 'problem-table'})
    if not table:
        print("Table not found on the webpage.")
    return table


def getContestName(soup):
    attrName = 'class'
    attrValue = 'flex justify-between items-center mb-8 mt-4'
    tag = soup.find('div', {attrName: attrValue})
    title = tag.find('h1')
    return title.text


if response.status_code == 200:        # if retrieval was successful:
    soup = BeautifulSoup(response.text, 'html.parser')  # get BS object
    contestName = getContestName(soup)
    targetTable = getProblemTable(soup)
    colIndex = 0  # Replace with the column index you want
    rows = targetTable.find_all('tr')[1:]
    numProblems = len(rows)
    for rowIndex in range(numProblems):
        columns = rows[rowIndex].find_all('td')
        if colIndex < len(columns):
            targetCell = columns[colIndex]
            link = targetCell.find('a')
            letter = targetCell.find('th')
            if link:
                href = link.get('href')
                problemCodes.append(href.split('/')[-1])
            else:
                print("No link found in the specified cell.")
        else:
            print(f"Column index {colIndex} out of range.")

else:
    print(
        f"Failed to retrieve the webpage. Status code: {response.status_code}")

print(f'Problems from "{contestName}":')
print('\n'.join(problemCodes))
