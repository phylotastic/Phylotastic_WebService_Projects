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
import types
import subprocess

from cherrypy import tools
from str2bool import str2bool
from functools import partial

from service import extract_names_service
from service import services_helper

#==============================================================
WebService_Group = "fn"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
HOST = "0.0.0.0"  #"127.0.0.1"
PORT = "5050"

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
        
#------------------------------------------


#-------------------------------------------
class CustomException(Exception):
    pass


#===========================Find_ScientificNames_Service_GNRD=============================
class Find_ScientificNames_Service_API(object):
    def index(self):
        return "Find_ScientificNames_GNRD_Service API: Find Scientific names from Url, Text, Files using GNRD";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def names_url(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            url = str(request_data['url']).strip()
            if len(url) == 0:
               raise CustomException("'url' parameter must have a valid value")
            if request_data is not None and 'engine' in request_data:
               engine = str(request_data['engine']).strip()
               if engine not in ['0', '1', '2']:
                  return return_response_error(400,"Error: 'engine' parameter must have a valid value","JSON") 
            else:
               engine = '0'
            if not services_helper.is_http_url(url):
               raise CustomException("'url' parameter must have a valid value")
            if not services_helper.does_url_exist(url):
               raise CustomException("'url' parameter must have a valid value")

        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_URL(url, int(engine))   
            result_json = service_result
            #------------------------------------------   
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====NamesURLError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    @cherrypy.tools.json_out()
    def names_text(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            text = str(request_data['text']).strip()
            
            if len(text) == 0:
               raise CustomException("'text' parameter must have a valid value")
            if request_data is not None and 'engine' in request_data:
               engine = str(request_data['engine']).strip()
               if engine not in ['0', '1', '2']:
                  return return_response_error(400,"Error: 'engine' parameter must have a valid value","JSON") 
            else:
               engine = '0'

        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_TEXT(text, int(engine))
            result_json = service_result
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====NamesTextError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")   
    
    #------------------------------------------------
    @cherrypy.tools.json_out()
    def names_file(self, inputFile=None, engine='0'):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")
            
            file_size = 0
            saved_dir_loc = os.getcwd()+"/data/"
            file_loc = saved_dir_loc+inputFile.filename            

            with open(file_loc, 'wb') as f_out:
    	        for block in iter(partial(inputFile.file.read, 64), b''):
        	        f_out.write(block)

            file_size = os.path.getsize(file_loc)
            #print(file_size)
            #changing the file permission
            subprocess.call(["chmod", "a-w", file_loc])
            if file_size == 0:
               raise CustomException("Input file cannot be empty")
            
            content_type = inputFile.content_type
            #print content_type
            new_filename = inputFile.filename
            contype = cherrypy.request.headers.get("Content-Encoding")

        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        try: 
            
            service_result = extract_names_service.extract_names_FILE(saved_dir_loc, new_filename, int(engine))   
            result_json = service_result
            #------------------------------------------   
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====NamesFileError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
    #------------------------------------------------
    #Public /index
    index.exposed = True
    names_url.exposed = True
    names_text.exposed = True
    names_file.exposed = True


#===========================Find_ScientificNames_Service_TaxonFinder=============================
class Find_ScientificNames_TaxonFinder_Service_API(object):
    def index(self):
        return "Find_ScientificNames_TaxonFinder_Service API: Find Scientific names from Url, Text using TaxonFinder";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def names_url(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            url = str(request_data['url']).strip()
            if len(url) == 0:
               raise CustomException("'url' parameter must have a valid value")

            if not services_helper.is_http_url(url):
               raise CustomException("'url' parameter must have a valid value")
            if not services_helper.does_url_exist(url):
               raise CustomException("'url' parameter must have a valid value")

            
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_taxonfinder(url, 'url')   
            result_json = service_result
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====TaxonFinderNamesURLError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    @cherrypy.tools.json_out()
    def names_text(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            text = str(request_data['text']).strip()
            
            if len(text) == 0:
               raise CustomException("'text' parameter must have a valid value")
            
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_taxonfinder(text, 'text')
            result_json = service_result
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====TaxonFinderNamesTextError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")   
       
    #------------------------------------------------------
    #Public /index
    index.exposed = True
    names_url.exposed = True
    names_text.exposed = True

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
    cherrypy.tree.mount(Find_ScientificNames_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group)), conf_app)
    cherrypy.tree.mount(Find_ScientificNames_TaxonFinder_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group), "tf"), conf_app)

    #Starting Server
    cherrypy.engine.start()
    cherrypy.engine.block()
