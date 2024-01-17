import json

"""
Pretty print JSON and other simple data types
"""
def show_json(obj):

    if isinstance(obj,  (float, int, str, list, dict, tuple)): 
       print(obj)
       return
    
    print(obj.model_dump_json(indent=2))
# eo show_json