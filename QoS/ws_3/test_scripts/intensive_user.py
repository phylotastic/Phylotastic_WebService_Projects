import requests
import time
import json

class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        names_list = self.read_data("/home/tayeen/TayeenFolders/PythonFiles/qos/test_data/seaweed_plants.txt")
        self.post_body = {"scientificNames": names_list}
        

    def read_data(self,file_path):
        text_file = open(file_path, "r")
        data_list = text_file.read().split('\n')
        #print len(data_list)
        text_file.close()
       
        return data_list


    def run(self):
        start_timer = time.time()
        jsonPayload = json.dumps(self.post_body)
        response = requests.post("http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/names", data=jsonPayload, headers={'content-type': 'application/json'})

        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.read_data("/home/tayeen/TayeenFolders/PythonFiles/qos/test_data/seaweed_plants.txt")
    #print trans.custom_timers
