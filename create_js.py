import sqlite3

fileh = open("pub/asoiaf_characters.js", "w+")
fileh2 = open("pub/asoiaf_chapters.js", "w+")

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

fileh.write("var characters = [")

cur.execute('SELECT id, name FROM Characters')
rows = cur.fetchall()
for char in rows:
    name = char[1].replace("'", "\\'")
    fileh.write("{id: " + str(char[0]) + ", name: '" + name + "'},\n")

fileh.write("];")

fileh2.write("var chapters = [")

cur.execute('SELECT name, pov, book, position, characters FROM Chapters')
rows = cur.fetchall()
count = 0
for chap in rows:
    name = chap[0].replace("'", "\\'")
    characters = chap[4].split(",")
    char_array = ""
    for item in characters:
        char_array = char_array + "'" + item.replace("'", "\\'") + "', "
    char_array = char_array[:-2]

    fileh2.write("{id: " + str(count)
        + ", label: '" + name
        + "', book: '" + chap[2]
        + "', position: '" + str(chap[3])
        + "',\ncharacters: ["
        + char_array
        + "]},\n")
    count = count + 1

fileh2.write("];")

fileh.close()
fileh2.close()
conn.close()
