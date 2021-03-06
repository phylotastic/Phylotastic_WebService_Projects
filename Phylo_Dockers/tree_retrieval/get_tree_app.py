'''
Phylotastic Web Services
@author: Abu Saleh
'''

import cherrypy
import time
import datetime
import json
import os
import sys
import collections

from cherrypy import tools
from str2bool import str2bool

from service import resolve_names_service
from service import opentree_tree_service
from service import phylomatic_tree_service

#==============================================================
WebService_Group = "gt"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
HOST = "0.0.0.0"  #"127.0.0.1"
PORT = "5052"

#============================================================================
ACCESS_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_access_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_error_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

#------------------------------------------
#When user requests invalid resource URI
def error_page_404(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status
    return json.dumps({'message': "Error: Could not find the requested resource URI"})

#When user makes bad request
def error_page_400(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status
    return json.dumps({'message': message})

#When internal server error occurs
def error_page_500(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status
    return json.dumps({'message': message, 'traceback': traceback, 'status_code': 500})

#--------------------------------------------
def return_response_error(error_code, error_message, response_format="JSON"):
    #error_response = {'message': error_message, 'status_code':error_code}
    error_response = {'message': error_message}
    if (response_format == "JSON"):
        cherrypy.response.headers['Content-Type'] = "application/json"
        cherrypy.response.status = error_code
        cherrypy.response.body = error_response
        return error_response
    else:
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.body = error_message
        return json.dumps(error_response)
       
#-------------------------------------------
class CustomException(Exception):
    pass



#===============================Get_Tree_OpenTree_Service==========================
class Get_Tree_OpenTree_Service_API(object):
    def index(self):
        return "Get_Tree_OpenTree_Service API: Get Induced Subtree from Open Tree of Life";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")
           
            taxa = str(request_data['taxa']).strip()
            taxalist = taxa.split('|')

            include_metadata = False
            include_ottid = True
            if request_data is not None and 'studies' in request_data:
               include_metadata = str(request_data['studies']).strip()
               if type(include_metadata) is not bool:
                  include_metadata = str2bool(include_metadata)

            if request_data is not None and 'ottid' in request_data:
               include_ottid = str(request_data['ottid']).strip()
               if type(include_ottid) is not bool:
                  include_ottid = str2bool(include_ottid)

            if len(taxalist) == 1 and '' in taxalist: 
               raise CustomException("'taxa' parameter must have a valid value")

            if len(taxalist) > 2000: 
               return return_response_error(403,"Error: Currently more than 2000 taxa is not supported","JSON")

        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            nameslist_json = resolve_names_service.resolve_names_OT(taxalist, False, False)
            nameslist = nameslist_json["resolvedNames"]
            service_result = opentree_tree_service.get_tree_OT(nameslist,include_metadata,include_ottid) 
            result_json = service_result  
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====OToLTreeGetError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            include_metadata = False
            include_ottid = True
            input_json = cherrypy.request.json
            
            if 'taxa' not in input_json and 'resolvedNames' not in input_json:
                raise KeyError("taxa")
            elif 'taxa' in input_json and 'resolvedNames' not in input_json:
                taxalist = input_json["taxa"]
                if type(taxalist) is not list:
                   return return_response_error(400,"Error: 'taxa' parameter must be of list type","JSON")

                if len(taxalist) == 0 and 'resolvedNames' not in input_json: 
                   raise CustomException("'taxa' parameter must have a valid value")

                if len(taxalist) > 2000: 
                   return return_response_error(403,"Error: Currently more than 2000 names is not supported","JSON")
            if 'studies' in input_json:		
                 include_metadata = input_json['studies']
                 if type(include_metadata) is not bool:
                    include_metadata = str2bool(include_metadata)
            if 'ottid' in input_json:		
                 include_ottid = input_json['ottid']
                 if type(include_ottid) is not bool:
                    include_ottid = str2bool(include_ottid)	 

        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            if 'resolvedNames' not in input_json: 
                nameslist_json = resolve_names_service.resolve_names_OT(taxalist, False, False)
                nameslist = nameslist_json['resolvedNames']
                if len(nameslist) > 2000: 
                   return return_response_error(403,"Error: Currently more than 2000 names is not supported","JSON")
            else:
                nameslist = input_json['resolvedNames']
                taxalist = nameslist

            service_result = opentree_tree_service.get_tree_OT(nameslist, include_metadata, include_ottid)   
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====OToLTreePostError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

#--------------------------------------------------------------------
    #Public /index
    index.exposed = True
    get_tree.exposed = True
    tree.exposed = True

#=========================Get_Tree_Phylomatic_Service=============================
class Get_Tree_Phylomatic_Service_API(object):
    def index(self):
        return "Get_Tree_Phylomatic_Service_API : Get subtree from phylomatic";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            taxa = str(request_data['taxa']).strip();
            taxalist = taxa.split('|')

            if len(taxalist) == 1 and '' in taxalist: 
               raise CustomException("'taxa' parameter must have a valid value")

            if len(taxalist) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")

        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")

        try:                
            service_result = phylomatic_tree_service.tree_controller(taxalist) 
            result_json = service_result  
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====PhylomaticTreeGetError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            if 'taxa' not in input_json and 'resolvedNames' not in input_json:
                raise KeyError("taxa")
            elif 'taxa' in input_json and 'resolvedNames' not in input_json:
                taxalist = input_json["taxa"]
                if type(taxalist) is not list:
                   return return_response_error(400,"Error: 'taxa' parameter must be of list type","JSON")

                if len(taxalist) == 0 and 'resolvedNames' not in input_json: 
                   raise CustomException("'taxa' parameter must have a valid value")

                if len(taxalist) > 1000: 
                   return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON") 
  				 
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            if 'resolvedNames' not in input_json: 
                nameslist_json = resolve_names_service.resolve_names_OT(taxalist, False, False)
                nameslist = nameslist_json['resolvedNames']
                if len(nameslist) > 1000: 
                   return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")
            else:
                nameslist = input_json['resolvedNames']
                taxalist = phylomatic_tree_service.retrieve_taxa(nameslist)

            service_result = phylomatic_tree_service.tree_controller(taxalist)   
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====PhylomaticTreePostError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #--------------------------------------------------------------
    #Public /index
    index.exposed = True
    get_tree.exposed = True
    tree.exposed = True


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': HOST, #'0.0.0.0' "127.0.0.1",
                            'server.socket_port': int(PORT),
                            'log.error_file':ERROR_LOG_CHERRYPY,
                            'log.access_file':ACCESS_LOG_CHERRYPY,
                            'tools.log_tracebacks.on': True
                          })
    conf_app = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'error_page.500': error_page_500,
                'request.show_tracebacks': True
             }
    }
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Mounting Services
    cherrypy.tree.mount(Get_Tree_OpenTree_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group),"ot"), conf_app)
    cherrypy.tree.mount(Get_Tree_Phylomatic_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group),"pm"), conf_app)
    
    #Starting Server
    cherrypy.engine.start()
    cherrypy.engine.block()
