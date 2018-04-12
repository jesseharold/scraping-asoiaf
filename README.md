# scraping-asoiaf

uses python, beautiful soup, sqlite

part of learning python and web data collection, creating a visualization of George R. R. Martin's A Song of Ice And Fire book series.

retrieves and stores information about thousands of characters, 6 books, and hundreds of houses from http://www.anapioficeandfire.com/api/
scrapes information about book chapters from westeros.org's wiki

## to do:
1. make tables relate to each other using unique IDs instead of names, which aren't unique
2. decide how best to organize the data in visualization
  * region, house, character, relationships
  * book, chapter, character, relationships
  * all characters with connections based on family, house, allegiance, and chapter appearance
3. decide which library if any to use for vis
4. write python to create js files and refine visualization
