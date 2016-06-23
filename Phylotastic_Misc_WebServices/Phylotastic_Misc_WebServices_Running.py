'''
Created on June 23, 2016
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

from support import compare_trees_service


#WebService_Group1 = "ts"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5006"
PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5006 = ROOT_FOLDER + "/log/%s_5006_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5006 = ROOT_FOLDER + "/log/%s_5006_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


def return_response_error(error_code, error_message,response_format="JSON"):
    error_response = {'message': error_message, 'status_code':error_code}
    if (response_format == "JSON"):
        return json.dumps(error_response)
    else:
        return error_response

#--------------------------------------------------------------    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Compare_Trees_Service_API(object):

 	def index(self):
 		return "Compare_Trees_Service API: Compare two phylogenetic trees"

 	@cherrypy.tools.json_out()
 	@cherrypy.tools.json_in()
 	def compare_trees(self,**request_data):
 		try:
 			input_json = cherrypy.request.json
 			tree1_str = input_json["tree1_nwk"]
 			tree2_str = input_json["tree2_nwk"]
 		except KeyError, e:
 			return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"NotJSON")
 		except Exception, e:
 			return return_response_error(400,"Error:" + str(e), "NotJSON")
 
 		service_result = compare_trees_service.compare_trees(tree1_str, tree2_str)
 		return service_result;
 	
 	#------------------------------------------------
 	index.exposed = True	
 	compare_trees.exposed = True
#-----------------------------------------------------------
def CORS():
    print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5006,
                            'log.error_file':ERROR_LOG_CHERRYPY_5006,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5006
                          })
    
    #conf_user_case_1 = {
    #          '/static' : {
    #                       'tools.staticdir.on' : True,
    #                       'tools.staticdir.dir' : os.path.join(ROOT_FOLDER, 'files'),
    #                       'tools.staticdir.content_types' : {'xml': 'application/xml'}
    #           }
               
    #}
    conf_thanhnh = {
             '/':{
                'tools.CORS.on': True
             }
    }
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Starting Server
    #cherrypy.tree.mount(Find_ScientificNames_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group2)), conf_thanhnh )
    cherrypy.tree.mount(Compare_Trees_Service_API(), '/%s' %(str(WS_NAME)), conf_thanhnh )
    
    cherrypy.engine.start()
    cherrypy.engine.block()
