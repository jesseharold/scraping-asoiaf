import sqlite3
from urllib.request import Request, urlopen

baseurl = "http://www.anapioficeandfire.com/api/"

input_type = None
while input_type not in ["c", "h", "b"]:
    input_type = input("Get [c]haracters, [b]ooks, [h]ouses? ")
how_many = input("Get how many items? ")

data_types = {"c": "Characters", "b": "Books", "h": "Houses"}
data_type = data_types[input_type]

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()
# start from scratch each execution while testing
# cur.executescript('DROP TABLE IF EXISTS Characters;')

cur.execute('''CREATE TABLE IF NOT EXISTS Characters
    (id INTEGER UNIQUE, url TEXT, name TEXT, gender TEXT,
     culture TEXT, born TEXT, died TEXT, titles TEXT,
     aliases TEXT, father TEXT, mother TEXT, spouse TEXT,
     allegiances TEXT, books TEXT, povBooks TEXT, tvSeries TEXT,
     playedBy TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Houses
    (id INTEGER UNIQUE, url TEXT, name TEXT, region TEXT,
     coatOfArms TEXT, words TEXT, titles TEXT,
     seats TEXT, currentLord TEXT, heir TEXT, overlord TEXT,
     founded TEXT, founder TEXT, diedOut TEXT, ancestralWeapons TEXT,
     cadetBranches TEXT, swornMembers TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Books
    (id INTEGER UNIQUE, url TEXT, name TEXT, isbn TEXT,
     authors TEXT, numberOfPages TEXT, publisher TEXT,
     country TEXT, mediaType TEXT, released TEXT, characters TEXT,
     povCharacters TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS failedUrls
    (id INTEGER, type TEXT, url TEXT UNIQUE)''')

# Pick up where we left off
start = None
cur.execute('SELECT max(id) FROM ' + data_type)
try:
    row = cur.fetchone()
    if row is None :
        start = 0
    else:
        start = row[0]
except:
    start = 0

if start is None : start = 0

# start with one more than the largest one in the table
current = start + 1
stop = start + int(how_many)
# end of the character api
if stop > 2138:
    stop = 2138
fail = 0

while current <= stop:
    url = baseurl + data_type + '/' + str(current) + '/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        result = urlopen(req).read()
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page", url)
        print("Error", e)
        fail = fail + 1
        if fail > 5:
            print("too many failures, giving up on this url.")
            # break
            # save all the URLs with no data, to perhaps try again
            cur.execute('''INSERT OR IGNORE INTO failedUrls (id, type, url)
             VALUES ( ?, ?, ? )''',
                (int(current), data_type, url))
            current = current + 1
        continue

    data_dict = eval(result)

    print("retrieved ", data_type, current, data_dict['name'])

    if data_type == "Characters":
        # create joined strings for values that come in as arrays:
        titles_str = ", ".join(data_dict['titles'])
        aliases_str = ", ".join(data_dict['aliases'])
        allegiances_str = ", ".join(data_dict['allegiances'])
        books_str = ", ".join(data_dict['books'])
        povBooks_str = ", ".join(data_dict['povBooks'])
        tvSeries_str = ", ".join(data_dict['tvSeries'])
        playedBy_str = ", ".join(data_dict['playedBy'])

        cur.execute('''INSERT OR IGNORE INTO Characters (id, url, name, gender, culture,
        born, died, titles, aliases, father, mother, spouse,
         allegiances, books, povBooks, tvSeries, playedBy)
         VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
            (int(current), data_dict['url'],
            data_dict['name'], data_dict['gender'], data_dict['culture'],
            data_dict['born'], data_dict['died'], titles_str,
            aliases_str, data_dict['father'], data_dict['mother'],
            data_dict['spouse'], allegiances_str, books_str,
            povBooks_str, tvSeries_str, playedBy_str))

    elif data_type == "Houses":
        # create joined strings for values that come in as arrays:
        titles_str = ", ".join(data_dict['titles'])
        seats_str = ", ".join(data_dict['seats'])
        ancestralWeapons_str = ", ".join(data_dict['ancestralWeapons'])
        cadetBranches_str = ", ".join(data_dict['cadetBranches'])
        swornMembers_str = ", ".join(data_dict['swornMembers'])

        cur.execute('''INSERT OR IGNORE INTO Houses (id, url, name, region,
         coatOfArms, words, titles, seats, currentLord, heir, overlord,
         founded, founder, diedOut, ancestralWeapons,
         cadetBranches, swornMembers)
         VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
            (int(current), data_dict['url'],
            data_dict['name'], data_dict['region'], data_dict['coatOfArms'],
            data_dict['words'], titles_str,
            seats_str, data_dict['currentLord'], data_dict['heir'],
            data_dict['overlord'], data_dict['founded'], data_dict['founder'],
            data_dict['diedOut'], ancestralWeapons_str, cadetBranches_str, swornMembers_str))

    elif data_type == "Books":
        # create joined strings for values that come in as arrays:
        authors_str = ", ".join(data_dict['authors'])
        povCharacters_str = ", ".join(data_dict['povCharacters'])
        characters_str = ", ".join(data_dict['characters'])

        cur.execute('''INSERT OR IGNORE INTO Books (id, url, name, isbn,
         authors, numberOfPages, publisher, country, mediaType, released,
         characters, povCharacters)
         VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
            (int(current), data_dict['url'],
            data_dict['name'], data_dict['isbn'], authors_str,
            data_dict['numberOfPages'], data_dict['publisher'],
            data_dict['country'], data_dict['mediaType'], data_dict['released'],
            characters_str, povCharacters_str))

    print("stored ", data_type, current, data_dict['name'])

    current = current + 1
    if current % 5 == 0:
        conn.commit()

conn.commit()
cur.close()
