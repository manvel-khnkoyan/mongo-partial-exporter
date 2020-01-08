
This script can be useful when you have a large database and you want to restore database skeleton only, with a few data
Only thing you need is create configuration files describing your database structure and relationships between collections.


### MongoDump

```bash
python3 export.py --host localhost:27017 --db main_db --input scheme.yaml --level 5 --path /home/ubuntu/ 
```

### MongoRestore

```bash
mongorestore -h localhost -d my_database /home/ubuntu/my_database 
```


### Installation

```git clone https://github.com/manvel-khnkoyan/mongo-partial-exporter.git```  
```cd mongo-instance-exporter```  
```sudo pip3 install -r requirements.txt```  

### Configuration

YAML configuration file example

```yaml
users: # -> The collection
    start: yes      # -> optional: (start from this collection)
    limit: 100      # -> optional: (maximum records for this collection)
    projection:     # -> optional: (collect only given fields, otherwise script will collect full data)
        userId: 1   # -> optional
        devices: 1  # -> optional
    query:          # -> optional: (Specific query)
        deletedAt:  # -> optional
    relations:  # -> under this key can be described relations between users and other collections
        tokens:   # -> related collection
            - parentKey: userId:string  # -> users collection relation key with type after :
              currentKey: userId:string # -> related collection relation key with type after :
tokens: # -> Another collection, this one without start, it means, data can be collected only from users
    relations:
        groups:
            - parentKey: groupId:string
              currentKey: groupId:string 
```
  
  
**parentKey** and **currentKey** are supporting deep objects hierarchy:  
ex.: user.userId:number

### Types

There 3 types allowed to use:  
***number*** for any number, **string** and **ObjectId** for mongodb bson  
  

### Arrays
  

Arrays also widely supported. For these kind of objects:  
```{a: [{b: c}]}``` or ```{a: {b: [c]}]}```

can be used ```a.b.c``` key ( or for example with type ```a.b.c:number```)


### Options

All options are not optional.  

**start**: Initial collection    
**limit**: collection limit  
**sort**: sort collection  
**projection**: mongodb projections (useful for huge documents)  
**query**: Specific db query


 
