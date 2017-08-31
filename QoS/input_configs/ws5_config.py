'''
Required input settings for web service:  

'''
service_id = "ws_5"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot"

input_settings = [{'method': "GET", 'path': "/get_tree", 'weight': 0.3, 'input_data': {'taxa': "Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens"} }, 
		{'method': "GET", 'path': "/get_tree" ,'weight': 0.7, 'input_data': {'taxa': "Alaria esculenta|Canis lupus|Caulerpa lentillifera|Chlorella vulgaris|Chondrus crispus|Cladosiphon okamuranus|Eisenia bicyclis|Equus caballus|Fucus spiralis|Gelidiella acerosa|Gracilaria edulis|Gracilaria edulis|Helianthus annus|Laminaria digitata|Magnolia laevifolia|Nostoc commune|Palmaria palmata|Rosa rugosa|Saccharina latissima|Sargassum echinocarpum|Sargassum echinocarpum|Ulva lactuca|Undaria pinnatifida"} }
		]

