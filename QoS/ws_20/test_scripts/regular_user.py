import requests
import time
import json


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        self.post_body = {"newick": "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);"}

    def run(self):
        start_timer = time.time()
        jsonPayload = json.dumps(self.post_body)
        response = requests.post("http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/scale", data=jsonPayload, headers={'content-type': 'application/json'})

        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
