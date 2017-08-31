'''
Required input settings for web service:  

'''
service_id = "ws_6"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts"

input_settings = [{'method': "GET", 'path': "/all_species", 'weight': 0.3, 'input_data': {'taxon': "Panthera"} }, 
		{'method': "GET", 'path': "/all_species", 'weight': 0.7, 'input_data': {'taxon': "Felidae"} }
		]

