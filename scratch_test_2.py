import urllib.request
import urllib.error
import json

url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=AIzaSyB0yXizix_1m6Fli7oA8fHTZIgqqhf_UGQ'
data = json.dumps({'contents': [{'parts': [{'text': 'hi'}]}]}).encode('utf-8')
headers = {'Content-Type': 'application/json'}
req = urllib.request.Request(url, data=data, headers=headers, method='POST')

try:
    print(urllib.request.urlopen(req).read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('ERROR HTTP:', e.read().decode('utf-8'))
except Exception as e:
    print('ERROR:', str(e))
