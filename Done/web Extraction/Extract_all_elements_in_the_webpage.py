import requests # Extract all the data in the elements of the webpage
URL = 'http://google.com' # Change the link to anything that u want
data = (requests.get(URL)).text
print(data)
