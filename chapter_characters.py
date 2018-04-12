import sqlite3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# get chapter character information for asoiaf project
# http://awoiaf.westeros.org/

fileh = open("notadded.txt", "w+")
ignore_these = [None, "search", "navigation", "A Game of Thrones", "A Clash of Kings", "A Storm of Swords", "A Feast for Crows", "A Dance with Dragons"]

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

cur2 = conn.cursor()
cur2.execute('SELECT name FROM Characters')
rows2 = cur2.fetchall()

def is_a_character(name):
    # print(name)
    if name in ignore_these:
        return False
    for charname in rows2:
        if name == charname[0]:
            # print("match", name, charname[0])
            return True
    return False


cur.execute('SELECT * FROM Chapters')
rows = cur.fetchall()
for chap in rows:
    url = chap[5]
    # get this chapter's page
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # print("------ ", url, " ------")
    updated_chars = []
    try:
        html = urlopen(req).read()
        # print('got characters: ' + str(len(html)))
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find('div', {"id": "bodyContent"})
        links = content.find_all('a')
        for link in links:
            # check this to see if it matches the name of a character in the db
            if link.string in updated_chars or link.string is None:
                # skip repeats per chapter, and None vals
                match = False
            else:
                if is_a_character(link.string):
                    # if so, append to this chapter's "characters" col
                    updated_chars.append(link.string)
                else:
                    # dump the rejected names and chapter URLs somewhere
                    # so you can see how successful this was
                    fileh.write(link.string)
                    fileh.write("\t")
                    fileh.write(url)
                    fileh.write("\n")

        # update chapter in db with characters
        char_string = ",".join(updated_chars)
        print("adding", char_string)
        print("to", url)
        cur.execute('''UPDATE Chapters
            SET characters = ? WHERE url = ?''',
            (char_string, url))

    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
    except Exception as e:
        print("Unable to retrieve or parse page", url)
        print("Error", e)

fileh.close()
conn.commit()
conn.close()
