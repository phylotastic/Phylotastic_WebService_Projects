# -*- coding: utf-8 -*-
#Open Tree of Life tree service: version 1.2
import json
import time
import requests
import re
import ast
import datetime

from . import r_helper
from . import google_dns
from . import tree_studies_service
#------------------------
from ete3 import Tree
from ete3.parser.newick import NewickError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api_url = "https://api.opentreeoflife.org/v3/tree_of_life/"
headers = {'content-type': 'application/json'}
    
#-----------------Induced Subtree of a set of nodes [OpenTree]---------------------
#input: list (comma separated) of ottids (long)   
#output: json object with inducedsubtree in newick key and status message in message key
def get_inducedSubtree(ottIdList):
 	resource_url = api_url + "induced_subtree"    
    
 	payload_data = {
     	'ott_ids': ottIdList
 	}
 	jsonPayload = json.dumps(payload_data)
    
 	try: 
 		response = requests.post(resource_url, data=jsonPayload, headers=headers)
 	except requests.exceptions.ConnectionError:
 		alt_url = google_dns.alt_service_url(resource_url)
 		response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    #----------------------------------------------

 	newick_tree_str = ""
 	studies = ""
 	inducedtree_info = {}

 	if response.status_code == requests.codes.ok:
 		data_json = json.loads(response.text)
 		newick_tree_str = data_json['newick']
 		studies = data_json['supporting_studies']		
 		inducedtree_info['message'] = "Success"
 		inducedtree_info['status_code'] = 200
 	else:
 		try: 
 			error_msg = str(response.text)
 			if 'node_id' in error_msg:
 				st_indx = error_msg.find("node_id")  #"[/v3/tree_of_life/induced_subtree] Error: node_id 'ott4284156' was not found!"
 				en_indx = error_msg.find("was")
 				missing_node_id_str = error_msg[st_indx+9: en_indx-2]
 				missing_ott_id = int(missing_node_id_str.replace("ott", ""))
 				ottIdList.remove(missing_ott_id)
 				return ottIdList
 			else:
 				error_json = json.loads(error_msg)
 				error_msg = error_json['message']
 				inducedtree_info['message'] = "OpenTreeofLife API Error: " + error_msg
         	
 		except Exception as e:
 			inducedtree_info['message'] =  "OpenTreeofLife API Error: " + str(e)
     		 	
 	inducedtree_info['status_code'] = response.status_code

 	inducedtree_info['newick'] = newick_tree_str
 	inducedtree_info['studies'] = studies
 	
 	return inducedtree_info

#-------------------------------------------------------
def subtree(ottidList):   
 	induced_response = get_inducedSubtree(ottidList)
 	while type(induced_response) is list: 
 		induced_response = get_inducedSubtree(induced_response)    
 
 	return induced_response 
#-----------------------------------------------------------
#get newick string for tree from OpenTree
#input: list of resolved scientific names
def get_tree_OT(resolvedNames, include_studies=False, include_ottid=True):
 	start_time = time.time() 
 	ListSize = len(resolvedNames)
    
 	response = {}
 	if ListSize == 0:
 		response['newick'] = ""
 		response['message'] = "Error: List of resolved names empty"
 		response['status_code'] = 500
 		
 		return response
 		
 	rsnames = resolvedNames
 	#rsnames = resolvedNames['resolvedNames']
 	ottIdList = []
 	for rname in rsnames:
 		if 'matched_results' in rname:
 			for match_result in rname['matched_results']:
 				if 'Open Tree of Life' in match_result['data_source']:
 					ottIdList.append(match_result['taxon_id'])
 					break 			
 		else:
 			if rname['resolver_name'] == 'OT':
 				ottIdList.append(rname['taxon_id'])
 			else:
 				response['newick'] = ""
 				response['message'] = "Error: wrong TNRS. Need to resolve with OpenTreeofLife TNRS"
 				response['status_code'] = 500
 				return response
 			     
    #get induced_subtree
 	final_result = {} 
 	opentree_result = subtree(ottIdList)
 	if opentree_result['status_code'] != 200:	
 		return opentree_result 

 	newick_str = opentree_result['newick']
 	if newick_str.find(";") == -1:
 		newick_str = newick_str + ";"
 
 	if not(include_ottid):
 		# Delete ott_ids from tip_labels
 		nw_str = newick_str
 		nw_str = re.sub('_ott\d+', "", nw_str)
 		newick_str = nw_str
 		#newick_str = nw_str.replace('_', " ")

 	#remove singleton nodes from tree
 	final_nwk_bytes = r_helper.remove_singleton(newick_str)
 	final_nwk_str = str(final_nwk_bytes, 'utf-8') #convert a Python 3 byte-string variable into a regular string
 	#print (type(final_nwk_str))
 	if final_nwk_str is None: #R function did not work
 		final_nwk_str = newick_str
 	
 	final_result['newick'] = final_nwk_str #newick_str.encode('ascii', 'ignore').decode('ascii')
 	
 	if opentree_result['newick'] != "":
 		final_result['message'] = "Success"
 		final_result['status_code'] = 200
 		synth_tree_version = get_tree_version()		
 		tree_metadata = get_metadata()
 		tree_metadata['inference_method'] = tree_metadata['inference_method'] + " from synthetic tree with ID "+ synth_tree_version
 		final_result['tree_metadata'] = tree_metadata
 		final_result['tree_metadata']['synthetic_tree_id'] = synth_tree_version
 		#https://wiki.python.org/moin/UnicodeDecodeError
 		newick_str = newick_str.encode('utf-8', 'ignore')
 		num_tips = get_num_tips(newick_str)
 		if num_tips != -1:
 			final_result['tree_metadata']['num_tips'] = num_tips
 		study_ids = opentree_result['studies']
 		final_result['tree_metadata']['study_ids'] = study_ids

 		if include_studies:
 			#get studies 
 			study_list = tree_studies_service.get_studies(study_ids) 	
 			final_result['tree_metadata']['supporting_studies'] = study_list['studies']
 		 
 	end_time = time.time()
 	execution_time = end_time-start_time
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	meta_data = {}
 	meta_data['creation_time'] = creation_time
 	meta_data['execution_time'] = float("{:4.2f}".format(execution_time))
 	meta_data['source_urls'] = ["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tree_of_life"]

 	final_result['meta_data'] = meta_data  

 	return final_result
 	
#--------------------------------------------
#find the number of tips in the tree
def get_num_tips(newick_str):
 	parse_error = False
 	try:
 		tree = Tree(newick_str)
 	except NewickError:
 		try:
 			tree = Tree(newick_str, format=1)
 		except NewickError as e:
 			#print str(e) 
 			if 'quoted_node_names' in str(e):
 				try:
 					tree = Tree(newick_str, format=1, quoted_node_names=True)
 				except NewickError as e:
 					parse_error = True	
 			else:
 				parse_error = True

 	if not(parse_error):
 		tips_list = [leaf for leaf in tree.iter_leaves()]            
 		tips_num = len(tips_list)
 	else:
 		tips_num = -1

 	return tips_num

#-------------------------------------------
def get_tree_version():
 	resource_url = api_url + "about"    
    
 	#----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
 	try: 
 		response = requests.post(resource_url)
 	except requests.exceptions.ConnectionError:
 		alt_url = google_dns.alt_service_url(resource_url)
 		response = requests.post(alt_url, verify=False)                
    #----------------------------------------------
        
 	metadata = {}
 	if response.status_code == requests.codes.ok:
 		data_json = json.loads(response.text)
 		return data_json['synth_id']
 	else:
 		return "" #Error: getting synth tree version"  

#---------------------------------------------
def get_metadata():
 	tree_metadata = {}
 	tree_metadata['topology_id'] = "NA"
 	tree_metadata['gene_or_species'] = "species"
 	tree_metadata['rooted'] = True
 	tree_metadata['anastomosing'] = False
 	tree_metadata['consensus_type'] = "NA"
 	tree_metadata['branch_lengths_type'] = None
 	tree_metadata['branch_support_type'] = None
 	tree_metadata['character_matrix'] = "NA"
 	tree_metadata['alignment_method'] = "NA"
 	tree_metadata['inference_method'] = "induced_subtree"

 	return tree_metadata	
#---------------------------------------------
	    

