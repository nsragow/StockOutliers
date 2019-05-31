from cache import Cacher,CachedJsonGet


func = lambda x : x
dir = "/Users/noah/Flatiron/Projects/StockOutliers/CacheSystem/prac_files"


json = """
{"hi":3}
"""
keys = [
"hi",
"you",
"jo"
]

c = Cacher(func,dir)

for key in keys:
    c.cache(key,json)
    assert c.read(key) == {"hi":3}
c.close()

c = Cacher(func,dir)
for key in keys:
    assert c.read(key) == {"hi":3}
for key in keys:
    c.cache(key,{"second":2})
    assert c.read(key) == {"second":2}
try:

    print(c.read("whhhat"))
    raise Exception("should have thrown keyerror")
except KeyError:
    pass
c.close()



#example

pairs = {
"key1":{"a":3},
"key2":{},
"key3":{"b":["a","b"]},
"key4":{},
"key5":{" c":30},
"key6":{}
}
c = Cacher(func,dir)

getter = CachedJsonGet(pairs.get,c)


for key in pairs.keys():
    assert getter.get(key) == pairs.get(key)
    assert getter.get(key) == pairs.get(key)
getter.close()
