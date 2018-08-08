
import requests
from bs4 import BeautifulSoup

def get_files_recursively(url, extension, restricted=False, recursive=True, depth=2, MAXnumberOfURLsPerPage=50, maxNumOfFilesToFind=35):
  """Find all files with the given extension in the webpage with the given url and its children.
  
  Keyword arguments:
  url -- The webpage's url
  extension -- The file extension. Do not include dot.
  restricted -- Wether to search only for files that their link is superset of the url given (default False).
  recursive -- Whether to look in child-pages (default True).
  depth -- How deep follow the links. Is considered only if recursive=True (default 2).
  MAXnumberOfURLsPerPage -- This is to overcome cases where execution gets stuck in a webpage for unforseen reasons (default 50).
  maxNumOfFilesToFind -- The max number of files to find (default 30).
  """
  output = set()
  # The following is the list of extensions that getting urls from links ending at them takes too long. It is used in the page_urls method.
  extensionsDict = {'2':['.db', '.gz'], '3':['.gif', '.png', '.ico', '.htm', '.jpg', '.bmp', '.pdf', '.mp3', 'mp4', '.ogg', '.wav', '.wma', '.wmv', '.3gp', '.avi', '.bin', '.exe', '.iso', '.ppt', '.rar', '.zip', '.tar', '.tif', '.mkv', '.mov', ], '4':['.jpeg', '.gzip', '.html'] }
  try:
    extensionsDict.get(str(len(extension))).remove('.'+ extension)
  except:
    pass

  def page_urls(url, extension, restricted, MAXnumberOfURLsPerPage, extensionsDict):
    """Return the urls in the webpage as a list."""
    length = len(extension)
    try:
      # Packages the request, send the request and catch the response: r
      r = requests.get(url)
      # Extract the response
      html = r.text
    except:
      html = ''

    soup = BeautifulSoup(html, features="html5lib")
    
    # adding / at the end of url if it is an indexing page and doesn't already have / at the end
    if url[-1] != '/' and soup.title != None and 'Index' in soup.title.text:
      url += '/'
    
    # making an illegal list of those links in index pages that go to parent directory or sort by name, modified time, ...
    illegal = ['?C=N;O=D', '?C=N;O=A', '?C=M;O=D', '?C=M;O=A', '?C=S;O=A', '?C=S;O=D', '?C=D;O=A', '?C=D;O=D', '/', '']
    
    urls = []
    for tag_element in soup.find_all('a'):
      href = tag_element.get('href', '')
      # exclude links that refer to different parts of the website, or are 'mailto' links or include 'javascript:'
      if '#' in href or 'mailto:' in href or 'javascript:' in href:
        continue
      if href not in illegal:
        newUrl = url + href

        if newUrl[-3:] in extensionsDict['2'] or newUrl[-4:] in extensionsDict['3'] or newUrl[-5:] in extensionsDict['4']:
          continue
        # excluding urls that have // but not as a part of the beggining http(s)://
        if '//' in newUrl[7:] and newUrl[-(length + 1) :] != '.' + extension:
          continue
        if restricted:
          # checks whether there is another http(s):// in the url other than the one at the beginning
          if '://' in item[7:]: # item[7:] exclude the http(s):// part from the url
            continue
        if 'html' in newUrl[:-4]:
          continue
        urls.append(newUrl)
        if len(urls) >= MAXnumberOfURLsPerPage:
          break
    return urls

  def _find_by_extension(url, extension, restricted, recursive, depth, MAXnumberOfURLsPerPage, maxNumOfFilesToFind, output, extensionsDict, flag=False):
    if flag:  # if maxNumOfFilesToFind has been reached
      return
    if depth > -1:
      length = len(extension)
      urls = page_urls(url, extension, restricted, MAXnumberOfURLsPerPage, extensionsDict)
      for item in urls:
        depth_copy = depth
        if item[-(length + 1) :] == '.' + extension: # if the extension is matched
          if not restricted:
            if 'http' in item[7:]:
              output.add(item[item[7:].index('http') +7:])
            else:
              output.add(item)
          else: # if restricted
            if 'http' not in item[7:]:
              output.add(item)
          if len(output) >= maxNumOfFilesToFind:
            flag = True
            break
          continue
        # the following lines get executed only if the extension is not matched
        depth_copy -= 1
        _find_by_extension(item, extension, restricted, recursive, depth_copy, MAXnumberOfURLsPerPage, maxNumOfFilesToFind, output, extensionsDict, flag)
    else:
      return

  _find_by_extension(url, extension, restricted, recursive, depth, MAXnumberOfURLsPerPage, maxNumOfFilesToFind, output, extensionsDict)
  return output


url = 'http://www.midi.gouv.qc.ca/publications/en/'
print(*get_files_recursively(url, 'pdf', depth=4, maxNumOfFilesToFind=35), sep='\n')
