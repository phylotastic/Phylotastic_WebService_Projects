import json
#import subprocess
import cherrypy
import os
import datetime
import time

from cherrypy import tools
from distutils.util import strtobool
import data_handler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WS_NAME = "phylotastic_ws"
WS_GROUP = "ds" #data service
ROOT_FOLDER = os.getcwd()
HOST = "0.0.0.0"
PORT = "5000"

#============================================================================
ACCESS_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_access_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_error_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

#===========================================================
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

#---------------------------------------------
def return_response_error(error_code, error_message,response_format="JSON"):
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

#---------------------------------------------------------    
class TreeViewer_Data_Service_API(object):
    def index(self):
        return "TreeViewer_Data_Service API : Find info of species for TreeViewer";

    @cherrypy.tools.json_out()
    def check_db(self, **request_data):
          
        try:
            conn = data_handler.connect_mongodb()
            service_result = data_handler.check_collection(conn)   
            conn.close()

            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("====CheckDBError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #---------------------------------------------
    def get_image_info(self, species=None, image_id=0, next_image=False):
        if species is None:
            return return_response_error(400,"Error:Missing parameter 'species'")
        if type(next_image) is not bool:
            next_image = strtobool(next_image)
   
        service_result = data_handler.image_info_controller(species, int(image_id), next_image)   
        
        return json.dumps(service_result)

    #--------------------------------------------------
    def get_link_info(self, species=None):
        if species is None:
            return return_response_error(400,"Error:Missing parameter 'species'")
           
        service_result = data_handler.link_info_controller(species)   
        
        return json.dumps(service_result)

    #--------------------------------------------------------
    def image_info_exists(self, species=None):
        if species is None:
            return return_response_error(400,"Error:Missing parameter 'species'")
           
        service_result = data_handler.images_exists(species)           

        return json.dumps(service_result)

    #---------------------------------------------------------
    def images_download_time(self,newick=None):
        if newick is None:
            return return_response_error(400,"Error:Missing parameter 'newick'")
        
        service_result = data_handler.estimate_image_download(newick)
        #if (service_result['number_species'] != 0):
           #subprocess.Popen(args=['python', 'data_handler.py', '%s' % newick], shell=True)
        print ("images download time: %s" %service_result['download_time'])        
        return json.dumps(service_result) 

    #---------------------------------------------------------
    def download_all_images(self,newick=None):
        if newick is None:
            return return_response_error(400,"Error:Missing parameter 'newick'")
        
        service_result = data_handler.load_all_images(newick)
        if service_result['download_complete']:
           #print "Download completed"
           return "<b>Done. Click again to display images on tree</b>"
           #return "<b>Download of images completed. Please click the load images button again</b>" 
       
 	#------------------------------------------------
    #Public /index
    index.exposed = True
    check_db.exposed = True
    get_image_info.exposed = True
    get_link_info.exposed = True
    image_info_exists.exposed = True
    images_download_time.exposed = True
    download_all_images.exposed = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CORS():
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"


#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': HOST,
                            'server.socket_port': int(PORT),
                            'log.error_file':ERROR_LOG_CHERRYPY,
                            'log.access_file':ACCESS_LOG_CHERRYPY,
                            'tools.log_tracebacks.on': True
                          })

    
    conf_CORS = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'error_page.500': error_page_500,
                'request.show_tracebacks': True
             }
    }
    
    #Mounting services
    cherrypy.tree.mount(TreeViewer_Data_Service_API(), '/%s/%s' %(str(WS_NAME),str(WS_GROUP)), conf_CORS )
    
    #Starting Server
    cherrypy.engine.start()
    cherrypy.engine.block()
