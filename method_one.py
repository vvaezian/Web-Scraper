import requests
from bs4 import BeautifulSoup

def get_files_using_Google_search(givenUrl, extension, maxNumOfFilesToFind=30):
  """Use Google search engine to find links to files with a specific extension in a given webpage and its children.
  
  Keyword arguments:
  givenUrl -- (string) The url to look for files in it and its children.
  extension -- (string) The type of file to look for. Do NOT include the dot (as in .pdf).
  maxNumofFilesToFind -- (int) The max number of files to find (default 30).
  """
  flag = False  # to check if maxNumberOfFilesToFind has been reached
  startingResultNum = 0  # to build the other pages of search results
  output = set()  # set of found links
  
  while True:
    url = 'https://www.google.com/search?q=site:'+ givenUrl + '+filetype:' + extension + '&start=' + str(startingResultNum)
    # Packages the request, send the request and catch the response: r
    r = requests.get(url)
    # Extract the response
    html = r.text
    soup = BeautifulSoup(html, features="html5lib")
    
    # checking to see if there is no more results
    if 'did not match any document' in soup.text: 
      break

    # checking to see if Google has blocked access becuase of too many requests
    checkForCaptcha = soup.find_all('div', class_ = 'g-recaptcha')
    if checkForCaptcha != []:
      output.add('Google blocked by CAPTCHA!')
      print('Because many requests were sent in a short period of time, Google is asking for CAPTCHA solving. You may wait some time and try again, or use a different ip.')
      break

    h3Tags = soup.find_all('h3', class_ = 'r')  # this specific class is because of the way Google shows search results
    for h3Tag in h3Tags:
      dirtyLink = h3Tag.a.get('href')  # this has some extra characters at the beginning and end which need to be striped.
      
      # Some links to desired files do not contain the extension in them although they are of the requested type.
      # So we check to see if the extension appears. If so then do the regular cleaning. If not, use & as indicator for cleaning
      try:
        link = dirtyLink[dirtyLink.lower().index('http') : dirtyLink.lower().index(extension) + len(extension)]
      except:
        link = dirtyLink[dirtyLink.index('http') : dirtyLink.index('&')]
      output.add(link)
      if len(output) >= maxNumOfFilesToFind:
        flag = True
        # get out of for loop
        break
    if flag:
      # get out of while loop
      break
    startingResultNum += 10
  
  return output

url = 'http://www.midi.gouv.qc.ca/publications/en/'
print(*get_files_using_Google_search(url, 'pdf'), sep='\n')
