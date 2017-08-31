'''
Required input settings for web service:  

'''
service_id = "ws_9"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi"

input_settings = [{'method': "GET", 'path': "/genome_species", 'weight': 0.3, 'input_data': {'taxon': "Panthera"} }, 
		{'method': "GET", 'path': "/genome_species" ,'weight': 0.7, 'input_data': {'taxon': "Rodentia"} }
		]

