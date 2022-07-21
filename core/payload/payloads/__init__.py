import os
import sys
class PayloadManagement:
    def __init__(self):
        self.payload_names = [os.path.basename(x) for x in PayloadManagement.list_payloads()]
        self.payload_handlers_paths = ["payload.payloads" + "." + os.path.basename(x) + "." +  "main" for x in PayloadManagement.list_payloads()]
        self.payloads_descriptions = {}
        for payload_names,importable_path in zip(self.payload_names,self.payload_handlers_paths):
            self.payloads_descriptions[payload_names]=getattr(__import__(importable_path),"__author__")
        
    @classmethod
    def list_payloads(self):
        target_path = [os.path.join(os.path.dirname(__file__),x) for x in os.listdir(os.path.dirname(__file__))]
        filtered_path = list(filter(lambda x:x if os.path.isdir(x) and not os.path.basename(x).startswith("__") else None,target_path))
        return filtered_path