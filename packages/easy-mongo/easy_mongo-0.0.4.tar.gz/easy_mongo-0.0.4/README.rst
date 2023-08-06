easy_mongo
^^^^^^^^^^
Easy to use python mongo(for kb first)

pymongo Reference: https://pymongo.readthedocs.io/en/3.10.0/tutorial.html

Quick Start
-----------
**Installation**: pip install easy_mongo

1.config
>>>>>>>>
Edit conf/conf.yml
::

    mongo: # mongo config
      host: 127.0.0.1
      port: 27017
      name: db_name
      password: password # blank if not require

2.demo
>>>>>>
::

    from easy_mongo.mongo import EasyMongo

    def demo_mongo():
        easy_mongo = EasyMongo('../conf/conf.yml')
        col = easy_mongo.get_collection('country')
        # get first 10 items
        # reference pymongo
        for item in col.find().limit(10):
            print(item)


    if __name__ == '__main__':
        demo_mongo()

