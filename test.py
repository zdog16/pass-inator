from rich.traceback import install
from rich.console import Console
import base64
import requests
import json
install()
c = Console()

url="https://api.github.com/repos/zdog16/pass-inator/contents/words.txt"
response = requests.get(url)
if response.status_code == requests.codes.ok:
    jsonResponse = response.json()  # the response is a JSON
    #the JSON is encoded in base 64, hence decode it
    content = base64.b64decode(jsonResponse['content'])
    #convert the byte stream to string
    jsonString = content.decode('utf-8')
    #finalJson = json.loads(jsonString)

out_list = jsonString.split('\n')


import generator
pswd = generator.pswd_generator()
c.print(pswd.generate_pswd())