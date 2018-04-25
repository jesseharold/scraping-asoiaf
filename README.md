# scraping-asoiaf

uses python, beautiful soup, sqlite

part of learning python and web data collection, creating a visualization of George R. R. Martin's A Song of Ice And Fire book series.

retrieves and stores information about thousands of characters, 6 books, and hundreds of houses from http://www.anapioficeandfire.com/api/
scrapes information about book chapters from westeros.org's wiki

## to do:
1. make tables relate to each other using unique IDs instead of names, which aren't unique
2. organize the data in visualization
  * region, house, character, relationships
  * book, chapter, character, relationships - done
  * all characters with connections based on family, house, allegiance, and chapter appearance
3. add summaries to chapter boxes
