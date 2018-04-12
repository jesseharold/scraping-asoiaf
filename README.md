# scraping-asoiaf

uses python, beautiful soup, sqlite

part of learning python and web data collection, creating a visualization of George R. R. Martin's A Song of Ice And Fire book series.

retrieves and stores information about thousands of characters, 6 books, and hundreds of houses from http://www.anapioficeandfire.com/api/
scrapes information about book chapters from westeros.org's wiki

to do:
  make tables relate to each other using unique IDs instead of names, which aren't unique
  decide how best to visualize the data 
    region, house, character, relationships
    book, chapter, character, relationships
    all characters with connections based on family, house, allegiance, and chapter appearance
  write python to create js files and refine visualization
