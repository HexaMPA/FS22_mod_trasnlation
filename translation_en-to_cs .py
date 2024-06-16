import re
from xml.etree import cElementTree as ET  
import requests
import json

API_KEY = "API-Key"
SECRET_KEY = "Secret_Key"

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=" + get_access_token()

def baidutrans(eng_text):
    
    payload = json.dumps({
        "q":eng_text,
        "from":"en",
        "to": "zh"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return eval(response.text)
 
class CommentedTreeBuilder(ET.TreeBuilder):
    def __init__(self, *args, **kwargs):
        super(CommentedTreeBuilder, self).__init__(*args, **kwargs)
 
    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)
 
 
parser  = ET.XMLParser(target=CommentedTreeBuilder())

tree = ET.parse("./translation_en.xml",parser = parser) 
root=tree.getroot()
print(tree)

for text_elem in root.iter('text'):  
    original_text = text_elem.get('text') 
    print(original_text)
    # 查找并替换翻译  
    translated_text=baidutrans(original_text).get("result").get('trans_result')[0].get('dst')
    print(translated_text)
    text_elem.set('text', translated_text)  
     
tree.write('translation_cs.xml',encoding="utf-8",xml_declaration=True)