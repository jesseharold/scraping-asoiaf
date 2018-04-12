import sqlite3

fileh = open("pub/asoiaf_nodes_test.js", "w+")
#fileh2 = open("pub/asoiaf_edges_test.js", "w+")

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

fileh.write("var nodes = new vis.DataSet([")
#fileh2.write("var edges = new vis.DataSet([")

cur.execute('SELECT * FROM Characters')
rows = cur.fetchall()
count = 0
for char in rows:
    name = char[2].replace("'", "\\'")
    fileh.write("{id: " + str(count) + ", label: '" + name + "'},\n")
    count = count + 1

fileh.write("]);")
#fileh2.write("]);")

fileh.close()
#fileh2.close()
conn.close()
