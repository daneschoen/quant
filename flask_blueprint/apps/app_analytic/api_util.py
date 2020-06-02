"""
UTILS for java api interactions

Optional parameters tend to be easier to put in the query string.

If you want to return a 404 error when the parameter value does not correspond to an existing resource then I would tend towards a path segment parameter. e.g. /customer/232 where 232 is not a valid customer id.

If however you want to return an empty list then when the parameter is not found then I suggest using query string parameters. e.g. /contacts?name=dave

If a parameter affects an entire subtree of your URI space then use a path segment. e.g. a language parameter  /en/document/foo.txt versus /document/foo.txt?language=en

I prefer unique identifiers to be in a path segment rather than a query parameter.


http://example.com/products -- all products
http://example.com/products/{id} -- specific one
http://example.com/products/?country=united-sites -- filtered


http://localhost/findbyproductcode/4xxheua BETTER THAN:
http://localhost/findbyproductcode?productcode=4xxheua

stackoverflow.com/questions
stackoverflow.com/questions/tagged/rest
stackoverflow.com/questions/3821663

GET /tickets - Retrieves a list of tickets
GET /tickets/12 - Retrieves a specific ticket
POST /tickets - Creates a new ticket
PUT /tickets/12 - Updates ticket #12
PATCH /tickets/12 - Partially updates ticket #12
DELETE /tickets/12 - Deletes ticket #12

Relations
GET /tickets/12/messages - Retrieves list of messages for ticket #12
GET /tickets/12/messages/5 - Retrieves message #5 for ticket #12
POST /tickets/12/messages - Creates a new message in ticket #12
PUT /tickets/12/messages/5 - Updates message #5 for ticket #12
PATCH /tickets/12/messages/5 - Partially updates message #5 for ticket #12
DELETE /tickets/12/messages/5 - Deletes message #5 for ticket #12
"""

from urllib.request import urlopen, Request # retrieve, urlencode, error
from urllib.error import URLError
import urllib.parse
import requests


def verifie_javaserverapi_test():
    # wget -O out "http://localhost:8007/api/import?instr=es---da---us"
    # wget -q -O - "$@" "http://localhost:8007/api/import?instr=es---da---us"
    
    # ps -ef | grep ServerApi
    return "to do"


def api_get(url_endpoint, **param):
    
    if param:
        url_endpoint += '?' + urllib.parse.quote_plus(param)
    
    request_url = Request(url_endpoint)
        
    try:
      response = urlopen(request_url)
      response_byte = response.read()
      return response_byte.decode("utf-8")
    except URLError as e:
      return "ERROR - Calling API: ServerApi OR url formation, parameters: " + str(e)


def download_file(url_endpoint):
    pass
    """
    import wget
    file_url = 'http://johndoe.com/download.zip'
    file_name = wget.download(file_url)
    
    
    testfile = urllib.URLopener()
    testfile.retrieve("http://randomsite.com/file.gz", "file.gz")
    
    
    urllib.request.urlretrieve ("http://randomsite.com/file.gz", "file.gz")
    
    # Download the file from `url`, save it in a temporary directory and get the
    # path to it (e.g. '/tmp/tmpb48zma.txt') in the `file_name` variable:
    file_name, headers = urllib.request.urlretrieve(url)
    
    
    
    r = requests.post('http://httpbin.org/post', files={'report.xls': open('report.xls', 'rb')})
    
    Content-Type header accordingly and respecting the Accept header sent by the client, you're free to return any format you want. You can just have a view that returns your binary data with the application/octet-stream content type.
    """
