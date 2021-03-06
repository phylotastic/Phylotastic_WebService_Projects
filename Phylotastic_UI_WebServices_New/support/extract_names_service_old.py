import json
import time
import requests
import re
import ast
import urllib

api_url = "http://finder.globalnames.org/name_finder.json?"
headers = {'content-type': 'application/json'}

#get scientific names from URL
def get_sn_url(inputURL):
    payload = {
        'url': inputURL,
    }
    
    encoded_payload = urllib.urlencode(payload)
    response = requests.get(api_url, params=encoded_payload, headers=headers) 
    
    scientificNamesList = []
     
    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
    else:
        return json.dumps({'scientificNames': scientificNamesList}) 
    
    token_result = get_token_result(data_json)
    
    if token_result['total'] == 0:
         return json.dumps({'scientificNames': scientificNamesList}) 
    else:
         scientificNamesList = get_sn(token_result['names']) 
         return json.dumps({'scientificNames': scientificNamesList}) 
     
#----------------------------------------------    
#get scientific names from final api-result
def get_sn(namesList):
    snlist = []
    uclist = []    
    for sn in namesList:
        #scName = element['scientificName'].replace(' ', '+')
        scName = sn['scientificName']       
        if is_ascii(scName): #check if there is any string with unicode character
            snlist.append(str(scName))    
        else:         
            uclist.append(scName)
    
    return snlist; 

#------------------------------------------------
def is_ascii(str_val):
    return bool(re.match(r'[\x00-\x7F]+$', str_val))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#get the final-api result using the token
def get_token_result(response_json):
        
    #get the token value from token url
    token_url = response_json['token_url']
    tokenURL, token = token_url.split('=', 1)
    str_token = str(token);
        
    #print "Waiting for the token to be activated"    
    #time.sleep(20)
    
    payload = {
        'token': str_token,
    }
    
    encoded_payload = urllib.urlencode(payload)
    
    while True:
        token_result = requests.get(api_url, params=encoded_payload, headers=headers)
        result_json = json.loads(token_result.text)
        if token_result.status_code == result_json['status']:
           return result_json 

#---------------------------------------------------
#get scientific names from Text
def get_sn_text(inputTEXT):
    payload = {
        'text': inputTEXT
    }
    
    encoded_payload = urllib.urlencode(payload)
    response = requests.get(api_url, params=encoded_payload, headers=headers) 
 
    scientificNamesList = []
    
    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
    else:
        return json.dumps({'scientificNames': scientificNamesList}) 
    
    token_result = get_token_result(data_json)
    
    if token_result['total'] == 0:
         return json.dumps({'scientificNames': scientificNamesList}) 
    else:
         scientificNamesList = get_sn(token_result['names']) 
         return json.dumps({'scientificNames': scientificNamesList}) 

#-----------------------------------------------------------

def extract_names_URL(inputURL): 
    final_result = get_sn_url(inputURL)    
    
    return final_result

def extract_names_TEXT(inputTEXT):
    final_result = get_sn_text(inputTEXT)    
    
    return final_result	

#--------------------------------------------

#if __name__ == '__main__':
    #inputURL = 'https://en.wikipedia.org/wiki/Aster'    
    #inputURL = 'https://en.wikipedia.org/wiki/Setophaga'
    #inputURL = 'https://species.wikimedia.org/wiki/Morganucodontidae'
    #inputURL = 'https://en.wikipedia.org/wiki/Ant'
    #inputTEXT = 'The Crabronidae are a large paraphyletic group of wasps. Ophiocordyceps, Cordyceps are genus of fungi. The Megalyroidea are a small hymenopteran superfamily that includes a single family, Megalyridae. The Apidae is the largest family within the Apoidea, with at least 5700 species of bees. Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'	
    #inputTEXT = "Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries."
    #result = extract_names_URL(inputURL)
    #result = extract_names_TEXT(inputTEXT)    
    #print result
    
