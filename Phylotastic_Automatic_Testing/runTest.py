import web_services
import helper

########################################################
#Test Web Service 1 : Find Scientific Names on web pages
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 1 : Find Scientific Names on web pages (GNRD)"
print "========================================================="
result_ws_1 = True
ws1_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/Find_Sc_Names_Web_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
	ws1_input = input_list[0]
	#print "Case file input: " + ws1_input
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_1 = False
 		print "Could not find output file for " + f
		break;
	else:		
		ws1_output = helper.create_list_file(output_file)
		#print "Case file output: " + ws1_output
 		ws1_result = web_services.testService_FindScientificNamesOnWebPages_WS_1(ws1_input, ws1_output)
		if ws1_result:
			print "Test succeeded for Case file: " + f
			print "---------------------------------------------------------" 
		ws1_results.append(ws1_result)

for result in ws1_results:
	result_ws_1 = (result_ws_1 and result)
 	if not(result_ws_1):
		break; 

print "---------------------------------------------------------"
if len(ws1_results) == 0:
	print "No Test Cases found"
	result_ws_1 = True 
elif (result_ws_1):
    print("Success ! Web Service 1 : Find Scientific Names on web pages IS WORKING WELL")
else:
    print("Failed ! Web Service 1 : Find Scientific Names on web pages IS NOT WORKING")

########################################################
#Test Web Service 2 : Find Scientific Names on free-form text
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 2 : Find Scientific Names on free-form text"
print "========================================================="
result_ws_2 = True
ws2_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/Find_Sc_Names_Text_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	ws2_input = helper.create_content_file(f)
	#print "Case file input: " + ws2_input
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_2 = False
 		print "Could not find output file for " + f
		break		
	ws2_output = helper.create_list_file(output_file)
	#print "Case file output: " + ws2_output
 	ws2_result = web_services.testService_FindScientificNamesOnText_WS_2(ws2_input, ws2_output)
	if ws2_result:
		print "Test succeeded for Case file: " + f
		print "-----------------------------------------------------" 
	ws2_results.append(ws2_result)

for result in ws2_results:
	result_ws_2 = (result_ws_2 and result)
 	if not(result_ws_2):
		break 

print "---------------------------------------------------------"
if len(ws2_results) == 0:
	print "No Test Cases found"
	result_ws_2 = True 
elif (result_ws_2):
    print("Success ! Web Service 2 : Find Scientific Names on free-form text IS WORKING WELL")
else:
    print("Failed ! Web Service 2 : Find Scientific Names on free-form text IS NOT WORKING")

########################################################
#Test Web Service 3 : Resolve Scientific Names with Open Tree TNRS - (Both GET and Post method) 
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 3 : Resolve Scientific Names with Open Tree TNRS"
print "========================================================="
result_ws_3 = True
ws3_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/TNRS_OT_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
 	#prepare ws3 input
	separator = "|"
	ws3_input_GET = separator.join(input_list)
	#print "Case file input: " + ws3_input_GET
	ws3_input_POST = helper.prepare_json_input('{"scientificNames":[',input_list) 
	#print "Case file input: " + ws3_input_POST
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_3 = False
 		print "Could not find output file for " + f
		break		
	ws3_output = helper.create_list_file(output_file)
	#print "Case file output: " + ws2_output
 	ws3_result_GET = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_GET(ws3_input_GET, ws3_output)
	ws3_result_POST = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_POST(ws3_input_POST, ws3_output) 	
	ws3_result = ws3_result_GET and ws3_result_POST

	if ws3_result_GET and ws3_result_POST:
		print "Test succeeded for Case file: " + f
	elif ws3_result_GET:
		print "GET - method Test succeeded for Case file: " + f
	elif ws3_result_POST:
		print "POST - method Test succeeded for Case file: " + f
	print "-----------------------------------------------------" 
	ws3_results.append(ws3_result)

for result in ws3_results:
	result_ws_3 = (result_ws_3 and result)
 	if not(result_ws_3):
		break 

print "---------------------------------------------------------"
if len(ws3_results) == 0:
	print "No Test Cases found"
	result_ws_3 = True 
elif (result_ws_3):
    print("Success ! Web Service 3 : Resolve Scientific Names with Open Tree TNRS IS WORKING WELL")
else:
    print("Failed ! Web Service 3 : Resolve Scientific Names with Open Tree TNRS IS NOT WORKING")

########################################################
#Test Web Service 4 : Resolve Scientific Names with GNR TNRS - (Both GET and Post method)
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 4 : Resolve Scientific Names with GNR TNRS"
print "========================================================="
result_ws_4 = False
ws4_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/TNRS_GNR_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
 	#prepare ws3 input
	separator = "|"
	ws4_input_GET = separator.join(input_list)
	#print "Case file input: " + ws4_input_GET
	ws4_input_POST = helper.prepare_json_input('{"scientificNames":[',input_list) 
	#print "Case file input: " + ws4_input_POST
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_4 = False
 		print "Could not find output file for " + f
		break		
	ws4_output = helper.create_list_file(output_file)
	#print "Case file output: " + ws2_output
 	ws4_result_GET = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_GET(ws4_input_GET, ws4_output)
	ws4_result_POST = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_POST(ws4_input_POST, ws4_output) 	
	ws4_result = ws4_result_GET and ws4_result_POST

	if ws4_result_GET and ws4_result_POST:
		print "Test succeeded for Case file: " + f
	elif ws4_result_GET:
		print "GET - method Test succeeded for Case file: " + f
	elif ws4_result_POST:
		print "POST - method Test succeeded for Case file: " + f
	print "-----------------------------------------------------" 
	ws4_results.append(ws4_result)

for result in ws4_results:
	result_ws_4 = (result_ws_4 and result)
 	if not(result_ws_4):
		break 

print "---------------------------------------------------------"
if len(ws4_results) == 0:
	print "No Test Cases found"
	result_ws_4 = True 
elif (result_ws_4):
    print("Success ! Web Service 4 : Resolve Scientific Names with GNR TNRS IS WORKING WELL")
else:
    print("Failed ! Web Service 4 : Resolve Scientific Names with GNR TNRS IS NOT WORKING")


########################################################
#Test Web Service 5 : Get Phylogenetic Trees from Open Tree of Life - GET method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 5 : Get Phylogenetic Trees from Open Tree of Life - GET method"
print "========================================================="
result_ws_5 = True
ws5_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/Get_Tree_OT_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
	separator = "|"
	ws5_input_GET = separator.join(input_list)
	#print "Case file input: " + ws5_input
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_5 = False
 		print "Could not find output file for " + f
		break;
	else:		
		ws5_output = helper.create_content_file(output_file)
		#print "Case file output: " + ws5_output
 		ws5_result = web_services.testService_GetPhylogeneticTreeFrom_OpenTree_5_GET(ws5_input_GET, ws5_output)
		if ws5_result:
			print "Test succeeded for Case file: " + f
			print "---------------------------------------------------------" 
		ws5_results.append(ws5_result)

for result in ws5_results:
	result_ws_5 = (result_ws_5 and result)
 	if not(result_ws_5):
		break; 

print "---------------------------------------------------------"
if len(ws5_results) == 0:
	print "No Test Cases found"
	result_ws_5 = True 
elif (result_ws_5):
    print("Success ! Web Service 5 : Get Phylogenetic Trees from Open Tree of Life IS WORKING WELL")
else:
    print("Failed ! Web Service 5 : Get Phylogenetic Trees from Open Tree of Life IS NOT WORKING")

########################################################
#Test Web Service 5 : Get Phylogenetic Trees from Open Tree of Life - POST method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
'''
print "========================================================="
result_ws_5 = False
json_input='{"resolvedNames": [{"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga striata", "search_string": "setophaga strieta", "synonyms": ["Dendroica striata", "Setophaga striata"], "taxon_id": 60236}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Setophaga magnolia", "search_string": "setophaga magnolia", "synonyms": ["Dendroica magnolia", "Setophaga magnolia"], "taxon_id": 3597209}, {"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga angelae", "search_string": "setophaga angilae", "synonyms": ["Dendroica angelae", "Setophaga angelae"], "taxon_id": 3597191}, {"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga plumbea", "search_string": "setophaga plambea", "synonyms": ["Dendroica plumbea", "Setophaga plumbea"], "taxon_id": 3597205}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Setophaga virens", "search_string": "setophaga virens", "synonyms": ["Dendroica virens", "Setophaga virens"], "taxon_id": 3597195}]}'
print "Start Test WS 5 : Get Phylogenetic Trees from Open Tree of Life - POST method"
print "Case 1 : Paramter  = %s \n" %(str(json_input))
result_case_1 = False
result_case_1 = web_services.testService_GetPhylogeneticTreeFrom_OpenTree_5_POST(json_input,"(((Setophaga_striata_ott60236,Setophaga_magnolia_ott3597209),Setophaga_virens_ott3597195),(Setophaga_plumbea_ott3597205,Setophaga_angelae_ott3597191))Setophaga_ott666104;")
print "---------------------------------------------------------"
if (result_case_1 == True):
    result_ws_5 = True
    print("Sucessful ! Web Service 5 : Get Phylogenetic Trees from Open Tree of Life - POST method IS WORKING WELL")
else:
    result_ws_5 = False
print "========================================================="

'''
########################################################
#Test Web Service 6 : Get all Species from a Taxon
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 6 : Get all Species from a Taxon"
print "========================================================="
result_ws_6 = True
ws6_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/Taxon_All_Species_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
	ws6_input = input_list[0]
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_6 = False
 		print "Could not find output file for " + f
		break		
	else:
		ws6_output = helper.create_list_file(output_file)
		ws6_result = web_services.testService_GetAllSpeciesFromATaxon_WS_6(ws6_input, ws6_output)
		if ws6_result:
			print "Test succeeded for Case file: " + f
	ws6_results.append(ws6_result)

for result in ws6_results:
	result_ws_6 = (result_ws_6 and result)
 	if not(result_ws_6):
		break 

print "---------------------------------------------------------"
if len(ws6_results) == 0:
	print "No Test Cases found"
	result_ws_6 = True 
elif (result_ws_6):
    print("Success ! Web Service 6 : Get all Species from a Taxon IS WORKING WELL")
else:
    print("Failed ! Web Service 6 : Get all Species from a Taxon IS NOT WORKING")

########################################################
#Test Web Service 7 : Get all Species from a Taxon filtered by country
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 7 : Get all Species from a Taxon filtered by country"
print "========================================================="
result_ws_7 = True
ws7_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/Taxon_Country_Species_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
	ws7_input1 = input_list[0]
	ws7_input2 = input_list[1]
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_7 = False
 		print "Could not find output file for " + f
		break		
	else:
		ws7_output = helper.create_list_file(output_file)
		ws7_result = web_services.testService_GetAllSpeciesFromATaxonFilteredByCountry_WS_7(ws7_input1, ws7_input2, ws7_output)
		if ws7_result:
			print "Test succeeded for Case file: " + f
	ws7_results.append(ws7_result)

for result in ws7_results:
	result_ws_7 = (result_ws_7 and result)
 	if not(result_ws_7):
		break 

print "---------------------------------------------------------"
if len(ws7_results) == 0:
	print "No Test Cases found"
	result_ws_7 = True 
elif (result_ws_7):
    print("Success ! Web Service 7 : Get all Species from a Taxon filtered by country IS WORKING WELL")
else:
    print("Failed ! Web Service 7 : Get all Species from a Taxon filtered by country IS NOT WORKING")

########################################################
#Test Web Service 8 : Get Image URLs of a list of species
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 8 : Get Image URLs of a list of species"
print "========================================================="
result_ws_8 = True
ws8_results = []
files_list = helper.get_filepaths("Species_EOL_Images_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
 	#prepare ws8 input
	separator = "|"
	ws8_input_GET = separator.join(input_list)
	print "Case file input: " + ws8_input_GET
	ws8_input_POST = helper.prepare_json_input('{"species":[',input_list) 
	print "Case file input: " + ws8_input_POST
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_8 = False
 		print "Could not find output file for " + f
		break		
	ws8_output = helper.create_list_file(output_file)
	#print "Case file output: " + ws8_output
 	ws8_result_GET = web_services.testService_GetImagesURLListOfSpecies_WS_8_GET(ws8_input_GET, ws8_output)
	ws8_result_POST = True#web_services.testService_GetImagesURLListOfSpecies_WS_8_POST(ws8_input_POST, ws8_output) 	
	ws8_result = ws8_result_GET and ws8_result_POST

	if ws8_result_GET and ws8_result_POST:
		print "Test succeeded for Case file: " + f
	elif ws8_result_GET:
		print "GET - method Test succeeded for Case file: " + f
	elif ws8_result_POST:
		print "POST - method Test succeeded for Case file: " + f
	print "-----------------------------------------------------" 
	ws8_results.append(ws8_result)

for result in ws8_results:
	result_ws_8 = (result_ws_8 and result)
 	if not(result_ws_8):
		break 
print "---------------------------------------------------------"
if len(ws8_results) == 0:
	print "No Test Cases found"
	result_ws_8 = True 
elif (result_ws_8):
    print("Success ! Web Service 8 : Get Image URLs of a list of species IS WORKING WELL")
else:
    print("Failed ! Web Service 8 : Get Image URLs of a list of speciesIS NOT WORKING")


########################################################
#Test Web Service 9 : Get Species (of a Taxon) that have genome sequence in NCBI
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 9 : Get Species (of a Taxon) that have genome sequence in NCBI"
print "========================================================="
result_ws_9 = True
ws9_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/Taxon_Genome_Species_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
	ws9_input = input_list[0]
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_9 = False
 		print "Could not find output file for " + f
		break		
	else:
		ws9_output = helper.create_list_file(output_file)
		ws9_result = web_services.testService_GetSpeciesNCBI_WS_9_GET(ws9_input, ws9_output)
		if ws9_result:
			print "Test succeeded for Case file: " + f
	ws9_results.append(ws9_result)

for result in ws9_results:
	result_ws_9 = (result_ws_9 and result)
 	if not(result_ws_9):
		break 

print "---------------------------------------------------------"
if len(ws9_results) == 0:
	print "No Test Cases found"
	result_ws_9 = True 
elif (result_ws_9):
    print("Success ! Web Service 9 : Get Species (of a Taxon) having genome sequence in NCBI IS WORKING WELL")
else:
    print("Failed ! Web Service 9 : Get Species (of a Taxon) having genome sequence in NCBI IS NOT WORKING")

########################################################
#Test Tree Viewer Service : Test whether the tree viewer service is alive
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing Tree Viewer Service : Check whether treeviewer service is alive"
print "========================================================="

result_ws_tvs = web_services.testService_TreeViewer_Alive()	

print "---------------------------------------------------------"
if (result_ws_tvs):
    print("Success ! Tree Viewer Service : Tree Viewer service IS WORKING WELL")
else:
    print("Failed ! Tree Viewer Service : Tree Viewer service IS NOT WORKING")


########################################################
#Finally Result
########################################################
if (result_ws_1 == True and result_ws_2 == True and result_ws_3 == True and result_ws_4 == True and result_ws_5 == True and result_ws_6 == True and result_ws_7 == True and result_ws_8 == True and result_ws_9 == True and result_ws_tvs == True):
    exit(0)
else:
    exit(1)
