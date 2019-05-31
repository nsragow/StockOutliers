import json




next_id = 0


def increment_id():
    next_id+=1

def format_directory(dir_str):
    if dir_str[-1] != "/":
        dir_str += "/"
    return dir_str


def get_json_dict(file_path):
    file = open(file_path,"r").read()
    json_dict = json.loads(file)
    return json_dict


class Cacher():
    '''
    Cache any json (as string or dict) to a file.
    '''
    def __init__(self,to_str_func,path_to_dir,file_start="jch"):
        '''
        to_str_func:
            Function that takes a key and returns a unique string.
            The return string is considered unique if it only corresponds to key's which are semantically equivalent.
        '''
        self.base_path = format_directory(path_to_dir)
        self.key_func = to_str_func

        self.meta = self.get_meta(self.base_path+".META")
        if "file_start" in self.meta:
            self.file_start = self.meta["file_start"]
        else:
            self.file_start = file_start
            self.meta["file_start"] = file_start

    def cache(self,key,response):
        if type(response) == dict:
            response = json.dumps(response)
        key = self.key_func(key)
        self.meta["pairs"][key] = self.write_to_json(key,response)
    def write_to_json(self,key,json):
        if key not in self.meta["pairs"].keys():

            file_path = format_directory(self.base_path) + self.id_to_name(self.meta["next_id"])
            self.meta["next_id"]+=1
        else:
            file_path = self.meta["pairs"][key]
        file = open(file_path,"w")

        file.write(json)
        file.close()
        return file_path

    def id_to_name(self,id):
        id_str = str(id)
        return f"{self.file_start}_{id_str}.json"
    def read(self,key):
        '''
        raises KeyError if not in cache
        '''
        key = self.key_func(key)
        return get_json_dict(self.meta["pairs"][key])

    def close(self):
        self.write_back_meta()
        self.base_path = None
        self.key_func = None
        self.meta = None

    def write_back_meta(self):
        file = open(self.base_path+".META","w")
        file.write(json.dumps(self.meta))
        file.close()

    def get_meta(self,path):


        try:
            open(path,"r").close()
        except:
            import os
            if not os.path.exists(self.base_path):
                os.makedirs(self.base_path)
            file = open(path,"w+")
            file.write("{}")
            file.close()
        file = open(path,"r")


        string = file.read()
        meta = json.loads(string)
        if "next_id" not in meta.keys():
            meta["next_id"] = 0
        if "pairs" not in meta.keys():
            meta["pairs"] = dict()
        return meta
class CachedJsonGet():
    '''
    Object which runs a function intended to get json dict.
    If the dict has already been found, will return the cached dict.

    Usage:
        getter = CachedJsonGet(some_getter,some_cacher)
        response = getter.get("https://www.google.com/json/some_json.json")
        response2 = getter.get("https://www.google.com/json/some_json.json")
        getter.close()
    '''
    def __init__(self,json_getter,cacher):
        '''
        json_getter:
            Function which returns a python representation of json
        cacher:
            a CachedJsonGet with corresponding to the json_getter function.
            This means that CachedJsonGet_inst.read(key) == json_getter(key) assuming CachedJsonGet_inst has already cached the response
        '''
        self.json_getter = json_getter
        self.cacher = cacher
    def get(self,key):
        try:
            return self.cacher.read(key)
        except KeyError:
            to_cache = self.json_getter(key)
            self.cacher.cache(key,to_cache)
            return to_cache
    def close(self):
        self.cacher.close()
        self.json_getter = None
        self.cacher = None
