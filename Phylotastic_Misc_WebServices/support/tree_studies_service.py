#tree-studies service: version 1.0
import json
import time
import requests
import datetime
#import urllib
import google_dns

#===================================
headers = {'content-type': 'application/json'}
opentree_base_url = "https://api.opentreeoflife.org/v3/"

#~~~~~~~~~~~~~~~~~~~~ (OpenTree-tree_of_life)~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_study_ids(ottid_list):
    opentree_method_url = opentree_base_url + "tree_of_life/induced_subtree"
    
    payload = {
        'ott_ids': ottid_list	
    }
    
    jsonPayload = json.dumps(payload)
    
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    try: 
       response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       alt_url = google_dns.alt_service_url(opentree_method_url)
       response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    #---------------------------------------------- 
    #response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    
    studyid_result = {}

    try:
       result_data_json = json.loads(response.text)

       if response.status_code == requests.codes.ok:    
          studyid_result['study_ids'] = result_data_json['supporting_studies']
          msg =  "Success"
          statuscode = 200
       else:
          if 'message' in result_data_json:
             msg = "OpenTree Error: "+result_data_json['message']
          else:
             msg = "OpenTreeofLife API Error: Response error while getting study ids"
        
    except ValueError:
         msg = "OpenTreeofLife API Error: Could not decode json response"

    statuscode = response.status_code
        
    studyid_result['message'] =  msg
    studyid_result['status_code'] = statuscode

    return studyid_result

#------------------------(OpenTree-studies)------------------------------
def get_study_info(studyid):
    opentree_method_url = opentree_base_url + "studies/find_studies"
    
    payload = {
        'property': 'ot:studyId',
        'value': studyid,
        'verbose': True	
    }
    
    jsonPayload = json.dumps(payload)
    
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    try: 
       response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       alt_url = google_dns.alt_service_url(opentree_method_url)
       response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    
    #response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    
    studyinfo_result = {}
    result_data_json = json.loads(response.text)

    if response.status_code == requests.codes.ok:    
        
        if (len(result_data_json['matched_studies']) == 0):
           studyinfo_result['message'] =  "No matching study found"
     	   studyinfo_result['status_code'] = 200
        else: 
           if ('ot:studyPublicationReference' in result_data_json['matched_studies'][0]):
              studyinfo_result['Publication'] = result_data_json['matched_studies'][0]['ot:studyPublicationReference']
           else:
              studyinfo_result['Publication'] = ""
           if ('ot:studyId' in result_data_json['matched_studies'][0]):
              studyinfo_result['PublicationIdentifier'] = result_data_json['matched_studies'][0]['ot:studyId']
           else:
              studyinfo_result['PublicationIdentifier'] = studyid
           if ('ot:curatorName' in result_data_json['matched_studies'][0]):
              studyinfo_result['Curator'] = result_data_json['matched_studies'][0]['ot:curatorName']
           else:
              studyinfo_result['Curator'] = ""
           if ('ot:studyYear' in result_data_json['matched_studies'][0]):
              studyinfo_result['PublicationYear'] = result_data_json['matched_studies'][0]['ot:studyYear']
           else:
              studyinfo_result['PublicationYear'] = ""
           if ('ot:focalCladeOTTTaxonName' in result_data_json['matched_studies'][0]):
              studyinfo_result['FocalCladeTaxonName'] = result_data_json['matched_studies'][0]['ot:focalCladeOTTTaxonName']
           else:
              studyinfo_result['FocalCladeTaxonName'] = ""
           if ('ot:studyPublication' in result_data_json['matched_studies'][0]):
              studyinfo_result['PublicationDOI'] = result_data_json['matched_studies'][0]['ot:studyPublication']
           else:
              studyinfo_result['PublicationDOI'] = ""
           if ('ot:dataDeposit' in result_data_json['matched_studies'][0]):
              studyinfo_result['DataRepository'] = result_data_json['matched_studies'][0]['ot:dataDeposit']
           else:
              studyinfo_result['DataRepository'] = ""
           if ('ot:candidateTreeForSynthesis' in result_data_json['matched_studies'][0]):
              studyinfo_result['CandidateTreeForSynthesis'] = result_data_json['matched_studies'][0]['ot:candidateTreeForSynthesis']
           else:
              studyinfo_result['CandidateTreeForSynthesis'] = ""
        
        studyinfo_result['message'] =  "Success"
     	studyinfo_result['status_code'] = 200
    else:    
        if 'message' in result_data_json:
           studyinfo_result['message'] = "OpenTree Error: "+result_data_json['message']
        else:
           studyinfo_result['message'] = "Error: Response error while getting study info from OpenTreeofLife"
        
        studyinfo_result['status_code'] = response.status_code
        

    return studyinfo_result

#----------------------------------------------------
def get_studies(studyid_list):
    start_time = time.time()
    studies_list = []
    study_ids = [study[:study.find("@")] for study in studyid_list]
    for studyid in study_ids:
        study_info = get_study_info(studyid)
        if study_info['status_code'] == 200:
           msg = study_info['message']
           status = study_info['status_code']
           #delete status keys from dictionary 
           del study_info['status_code']
           del study_info['message']
           studies_list.append(study_info)
        else:
           msg = study_info['message']
           status = study_info['status_code']
           break    

    end_time = time.time()
    execution_time = end_time-start_time
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#studies"] }

    response = {'studies':studies_list, 'message': msg, 'status_code': status , 'meta_data': meta_data}

    return response

#----------------------------------------------------
def get_studies_from_ids(id_list, is_ottid=True):
    start_time = time.time()
    studies_info = {}
    if is_ottid: #check whether the id_list is a list of ott ids or not
       study_id_list_json = get_study_ids(id_list)
       if study_id_list_json['status_code'] == 200:
          study_id_list = study_id_list_json['study_ids']
          studies_info_resp = get_studies(study_id_list)
          studies_info['studies'] = studies_info_resp['studies'] 
          if studies_info_resp['status_code'] != 200:
              studies_info['message'] = studies_info_resp['message']
              studies_info['status_code'] = studies_info_resp['status_code']
          else:
              studies_info['message'] = "Success"
              studies_info['status_code'] = 200
       else:
          studies_info['studies'] = []
          studies_info['message'] = study_id_list_json['message']
          studies_info['status_code'] = study_id_list_json['status_code']
    else: #when study ids are given directly
       studies_info_resp = get_studies(id_list)
       studies_info['studies'] = studies_info_resp['studies'] 
       if studies_info_resp['status_code'] != 200:
          studies_info['message'] = studies_info_resp['message']
          studies_info['status_code'] = studies_info_resp['status_code']
       else:
          studies_info['message'] = "Success"
          studies_info['status_code'] = 200
       
    end_time = time.time()
    execution_time = end_time-start_time
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#studies"] }

    studies_info['meta_data'] = meta_data

    return studies_info
    

#-------------------(OpenTree-TNRS)-----------------------------
def get_ott_ids(taxa, context=None):
    opentree_method_url = opentree_base_url + "tnrs/match_names"
    
    payload = {
        'names': taxa
    }
    if context is not None:
       payload['context_name'] = context

    jsonPayload = json.dumps(payload)
    
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    try: 
       response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       alt_url = google_dns.alt_service_url(opentree_method_url)
       response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    #response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    
    ott_id_list = []
    ott_id_result = {}

    result_data_json = json.loads(response.text)
    if response.status_code == requests.codes.ok:    
        result_list = result_data_json['results'] 
        for result in result_list:
            match_list = result['matches']
            for match in match_list:
                if float(match['score']) >= 0.75:
                   ott_id_list.append(match['taxon']['ott_id'])
                   break

        ott_id_result['ott_ids'] = ott_id_list	
        ott_id_result['status_code'] = 200
        ott_id_result['message'] = "Success"
    else:
        ott_id_result['ott_ids'] = ott_id_list	
        ott_id_result['status_code'] = response.status_code
        if 'message' in result_data_json:
           ott_id_result['message'] = "OpenTree Error: "+result_data_json['message']
        else:
           ott_id_result['message'] = "Error: getting ott ids from OpenTreeofLife"
    
    return ott_id_result

#----------------------------------------------------------
def get_studies_from_names(taxa_list, context=None):
    start_time = time.time()
    ottidlist_json = get_ott_ids(taxa_list, context)
    studies_info = {}
    if ottidlist_json['status_code'] != 200:    
        final_result = ottidlist_json   
    else:
        study_id_list_json = get_study_ids(ottidlist_json['ott_ids'])
        if study_id_list_json['status_code'] == 200:
           studies_info_resp = get_studies(study_id_list_json['study_ids'])
           studies_info['studies'] = studies_info_resp['studies'] 
           if studies_info_resp['status_code'] != 200:
              studies_info['message'] = studies_info_resp['message']
              studies_info['status_code'] = studies_info_resp['status_code']
           else:
              studies_info['message'] = "Success"
              studies_info['status_code'] = 200 
        else:
           studies_info['studies'] = []
           studies_info['message'] = study_id_list_json['message']
           studies_info['status_code'] = study_id_list_json['status_code']

        final_result = studies_info
    
    end_time = time.time()
    execution_time = end_time-start_time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#studies"] }

    final_result['meta_data'] = meta_data

    return final_result
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
 	#idlist = [433666, 18021, 3802384, 912655, 3746533, 918710]
	#idlist = ["ot_519", "ot_930", "ot_490", "pg_793", "pg_1631"]
 	#idlist = ["ot_519@tree2","ot_930@tree3", "ot_490@Tr70734","pg_793@tree5659","pg_1631@tree3297"]
	#print get_studies_from_ids(idlist)
 	
 	idlist = ["pg_1428@tree2855","ot_328@tree1","pg_2685@tree6235","pg_1981@tree4052","ot_278@tree1"]	
 	print get_studies(idlist)
