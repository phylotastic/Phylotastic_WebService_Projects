#scientific names to common names service: GNR version 1.0
import json
import requests
import time
import datetime 

#https://github.com/GlobalNamesArchitecture/gnindex/blob/master/examples/bash/example.sh
#{ "query": "query($names: [name!]!, $sources: [Int!]!)
#{ nameResolver(names: $names, dataSourceIds: $sources)
#  { responses {
#    total
#    results {
#      dataSource { id title }
#      name {value}
#      vernaculars {
#        name
#        language
#      }
#    }
#  }
#} }",
#  "variables": { "names": [{ "value": "Plantago major" },
#                           { "value": "Pica pica" } ],
#                 "sources": [1,4,9,11,179] }
#}

#https://index.globalnames.org/api/graphql

#----------------------------------------------
def match_species(speciesNamesList):
	GNR_api_url = "https://index.globalnames.org/api/graphql"    

	payload = make_payload(speciesNamesList)
	
	jsonPayload = json.dumps(payload)
	#print jsonPayload
	payload = jsonPayload
	response = requests.post(GNR_api_url, data=payload, headers={'Content-Type': 'application/json'}) 
  	
	gnr_response = {}
 	#print response.text
	
	if response.status_code == requests.codes.ok:    
		data_json = json.loads(response.text)
		response_results = data_json['data']['nameResolver']['responses']
		vernacular_names = get_vernacular_names(response_results, speciesNamesList)
		gnr_response['result'] = vernacular_names
		gnr_response['status_code'] = 200
		gnr_response['message'] = "Success"    
	else:
		gnr_response['status_code'] = response.status_code
		gnr_response['message'] = "Error: Response error from GNR while matching species names."
 
	return gnr_response

#-----------------------------------------
def make_payload(sc_names):
	base_query = "query($names: [name!]!, $sources: [Int!]!){ nameResolver(names: $names, dataSourceIds: $sources){ responses { total results { dataSource { id title } name {value} vernaculars { name language } }}}}"
  
	base_query = base_query.rstrip('\n') 

	query_list = []
	for name in sc_names:
		query_list.append({"value": name})

	payload_dict = {'query': base_query, 'variables': {'names': query_list, 'sources': [1,4,9,11,179] } }
	
	return payload_dict

#--------------------------------------------
def get_vernacular_names(gnr_resp_results, searched_name_list):
	matched_name_list = []
	for index, resp in enumerate(gnr_resp_results):
		searched_name = searched_name_list[index]
		species_comm_name_list = []
		if resp['total'] != 0:
			matched_name = None
			data_source_matches = []
			for result in resp['results']:
				data_source = result['dataSource']['title']
				matched_name = result['name']['value']
				#get the common names for this datasource
				common_names = []						
				for common_name in result['vernaculars']:
					if common_name['language'] is not None and (common_name['language'].lower() == "en" or common_name['language'].lower() == "eng" or common_name['language'].lower() == "english"):
						if common_name['name'].lower() not in common_names:
							common_names.append(common_name['name'])
				if len(common_names) > 0:
					species_comm_name_list.append({'matched_name': matched_name, 'data_source': data_source, 'common_names':common_names})
		
		matched_name_list.append({'searched_name': searched_name, 'matched_results': species_comm_name_list})

	return matched_name_list

#---------------------------------------------------
def get_sci_to_comm_names(inputSpeciesList):
	start_time = time.time()
	
	gnr_response = match_species(inputSpeciesList)
	if gnr_response['status_code'] != 200:
		return gnr_response
 	
	end_time = time.time()
	execution_time = end_time-start_time    
    #service result creation time
	creation_time = datetime.datetime.now().isoformat()
 	
	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["https://index.globalnames.org"]}
	gnr_response['meta_data'] = meta_data
 	
	return gnr_response
 	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

#	inputSpecies = ["Rangifer tarandus", "Cervus elaphus"]#, "Bos taurus", "Ovis orientalis", "Suricata suricatta", "Cistophora cristata", "Mephitis mephitis"]
   
 	#start_time = time.time()    
#	print (get_sci_to_comm_names(inputSpecies))
 	#end_time = time.time()
 	
 	#print end_time-start_time
