# web-scraper
This package include modules for findng links in a webpage and its children.

In the main module `find_links_by_extension` links are found using two sub-modules and then added together:

1. Using Google Search Results (`get_links_using_Google_search`)  
Since we can specify which types of files we are looking for when we search in Google, this methos scrapes these results.
But this method is not complete:  
* Google search works based on crawlers, and sometimes they don't index properly. For example [this][1] webpage has three pdf files at the moment (Aug 7 2018), but when we [use google search][2] to find them it finds only two  although the files were uploaded 4 years ago.  
* It doesn't work with some websites. For example [this][3] webpage  has three pdf files but google [cannot find any][4]. 
* If many requests are sent in a short period of time, Google blocks access and asks for CAPTCHA solving.

2. Using a direct method of finding all urls in the given page and following those links if they are refering to children pages and seach recursively (`get_links_directly`)  
While this method does not miss any files in pages that it gets to (in contrast to method 1 which sometimes do), it may not find all the files because:  
* Some webpages in the domain may be isolated i.e. there is no link to them in the parent pages. For these cases method 1 above works.  
* In rare cases the link to a file of type xyz may not have .xyz in the link ([example][5]). In these cases method 2 cannot detect the file (because it only relies on the extesion appearing in the links), but method 1 detects correctly in these cases.

So the two methods complete each other's gaps.

## installation 
`$ pip install web-scraper`  

**Note:** This package relies on `requests`, `bs4` and `html5lib` libraries. So You need to have them installed:  
`$ pip install requests bs4 html5lib`

## Usage  
```python
>>> import web_scraper as ws
>>> print(ws.find_links_by_extension("https://www.sfu.ca", 'pdf'))
```

## Methods
`find_links_by_extension`  
`get_links_using_Google_search`  
`get_links_directly`  

* `find_links_by_extension`  
Uses methods `get_links_using_Google_search` and `get_links_directly` to find links to files that have the given extension in the given webpage and its children.  

  ###### Keyword arguments:
  **url:** The webpage's url  
  **extension:** The file extension. Do not include dot.  
  **maxNumberOfLinksToFind:** Upper bound for number of links to find (default 30).  
  **sorted:** Whether to sort the output list (default False).  

* `get_links_using_Google_search`  
See the source file.  

* `get_links_directly`  
See the source file.

[1]: http://www.midi.gouv.qc.ca/publications/en/planification/
[2]: https://www.google.com/search?q=site%3Ahttp%3A%2F%2Fwww.midi.gouv.qc.ca%2Fpublications%2Fen%2Fplanification%2F+filetype%3Apdf
[3]: http://www.sfu.ca/~vvaezian/Summary/
[4]: https://www.google.com/search?q=site%3Ahttp%3A%2F%2Fwww.sfu.ca%2F~vvaezian%2FSummary%2F+filetype%3Apdf
[5]: http://www.sfu.ca/~robson/Random
