# Web-Scraper
Building on top of bs4 library, for finding files in a webpage and its children.

Files are found using two methods and then added together:

1- Using Google Search Results  
Since we can specify which types of files we are looking for when we search in Google, this methos scrapes these results.
But this method is not complete:  
a) Google search works based on crawlers, and sometimes they don't index properly. For example the webpage (http://www.midi.gouv.qc.ca/publications/en/planification/) has three pdf files at the moment (Aug 7 2018), but when we use google search to find them it finds only two (https://www.google.com/search?q=site%3Ahttp%3A%2F%2Fwww.midi.gouv.qc.ca%2Fpublications%2Fen%2Fplanification%2F+filetype%3Apdf)  
b) It doesn't work with some websites. For example the webpage (http://www.sfu.ca/~vvaezian/Summary/) has three pdf files but google cannot find any (https://www.google.com/search?q=site%3Ahttp%3A%2F%2Fwww.sfu.ca%2F~vvaezian%2FSummary%2F+filetype%3Apdf). Apparently the ~ symbol is cause of problem.  
c) If many requests are sent in a short period of time, Google blocks access and asks for CAPTCHA solving.

2- Using a direct method of finding all urls in the given page and following those links if they are refering to childrend pages in the webpage and seach recursively.  
While this method does not miss any files in pages that it gets to, it may not find all files, because some webpages in the domain may be isolated i.e. there are no link to them in the parent pages. For these cases method 1 above works. So the two method complete each other's gaps.
