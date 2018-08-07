# Web-Scraper
Building on top of bs4 library, for finding files in a webpage and its children.

Files are found using two methods and then added together:

1- Using Google Search Results
Since we can specify which types of files we are looking for when we search in Google, this methos scrapes these results.
But this method is not complete. Google search works based on crawlers, and sometimes they don't index properly. For example the webpage (http://www.midi.gouv.qc.ca/publications/en/planification/) has three pdf files at the moment (Aug 7 2018), but when we use google search to find them it finds only two (https://www.google.com/search?q=site%3Ahttp%3A%2F%2Fwww.midi.gouv.qc.ca%2Fpublications%2Fen%2Fplanification%2F+filetype%3Apdf)
