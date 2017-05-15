import time
import datetime
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
#import pandas.rpy.common as com
from rpy2.robjects import pandas2ri

def scale_tree(tree_newick):
	ro.r('library(datelife)')
	ro.r('estdates <- EstimateDates(input =' + tree_newick + ', output.format = "newick.median", partial = TRUE, usetnrs = FALSE, approximatematch = TRUE, method = "PATHd8")')
	scaled_tree = ro.r['estdates']
	
	pandas2ri.activate()	
	# converting <class 'rpy2.robjects.vectors.StrVector'> to <type 'numpy.ndarray'>	
	objstr = pandas2ri.ri2py(scaled_tree)
	# get the 'numpy.string_' object
	scaled_tree_str = objstr[0]
	
	return scaled_tree_str

#----------------------------------------------
def scale_tree_api(tree_newick):
	start_time = time.time()
	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-20"
	response = {}
	response['message'] = "Success"
 	response['status_code'] = 200	
	formatted_newick = '\"' + tree_newick + '\"'
	
	try:	
		sc_tree = scale_tree(formatted_newick)
		sc_tree = sc_tree.replace("_"," ")
		response['scaled_tree'] = sc_tree	
	except:
		response['message'] = "Error: Failed to scale from datelife R package"
 		response['status_code'] = 500		
	
	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
	response['creation_time'] = creation_time
 	response['execution_time'] = "{:4.2f}".format(execution_time)
	response['input_tree'] = tree_newick
 	response['service_documentation'] = service_documentation
 	
	return response
 
#-----------------------------------------------
'''
if __name__ == "__main__":

	tree_newick = "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);" 
	
	sc_tree = scale_tree_api(tree_newick)
	print "Result: %s" %sc_tree
'''


