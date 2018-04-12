import sqlite3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# get chapter information for asoiaf project
url = "http://awoiaf.westeros.org/index.php/Chapters_Table_of_contents"

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

# start from scratch each execution
cur.executescript('DROP TABLE IF EXISTS Chapters;')

cur.execute('''CREATE TABLE IF NOT EXISTS Chapters
    (id INTEGER UNIQUE, name TEXT, pov TEXT,
     book TEXT, position INTEGER, url TEXT, characters TEXT)''')


req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urlopen(req).read()
    print('got characters: ' + str(len(html)))
    soup = BeautifulSoup(html, "html.parser")
    tables = soup('table')
    for book in tables[1:]:
        print('---new book---')
        # find the h2 right before this table
        booktitletag = book.find_previous('h2')
        booktitle = (booktitletag.string)
        headerRow = False
        for chapter in book.find_all('tr'):
            if headerRow is False:
                # skip first row of each table
                headerRow = True
                continue
            attrs = chapter.find_all('td')
            if len(attrs) > 1 and attrs[1].a:
                #print('book: ', booktitle ,'position: ', attrs[0].string,' name: ', attrs[1].a.string, ' pov: ', attrs[2].a.string)
                infoLink = 'http://awoiaf.westeros.org' + attrs[1].a.get('href')
                # print(infoLink)
                cur.execute('''INSERT OR IGNORE INTO Chapters
                    (book, position, name, pov, url) VALUES (?, ?, ?, ?, ?)''',
                    (booktitle, int(attrs[0].string), attrs[1].a.string, attrs[2].a.string, infoLink))


except KeyboardInterrupt:
    print('')
    print('Program interrupted by user...')
except Exception as e:
    print("Unable to retrieve or parse page", url)
    print("Error", e)

conn.commit()
conn.close()
