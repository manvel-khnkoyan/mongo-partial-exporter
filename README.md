
This script could be helpful when you have big database, and you want to dump 
structure with few data without broking relations.

To making partial mongodump, use special configuration file to describe relations between collections.
So having information between collections - scrip will collect data according relations only.
By default script will collect last documents, but you can also change sort or 
add specific query for each collection. 

  

##### How to dump mongo instance

```bash
pip3 export.py --host localhost:27017 --db main_db --input scheme.yaml --level 5 --path /home/ubuntu/ 
```

##### Installation

```git clone https://github.com/manvel-khnkoyan/mongo-partial-exporter.git```  
```cd mongo-instance-exporter```  
```sudo pip3 install -r requirements.txt```  

##### Configuration file

Configuration file is yaml.

```yaml
users: # -> First keys are collections
    start: yes      # -> options
    limit: 100      # -> options
    projection:     # -> options
        userId: 1   # -> options
        devices: 1  # -> options
    query:          # -> options
        deletedAt:  # -> options
    relations:  # -> under this key can be described relations between users and other collections
        tokens:   # -> related collection
            - parentKey: userId:string  # -> users collection relation key with type after :
              currentKey: userId:string # -> related collection relation key with type after :
tokens:
    relations:
        groups:
            - parentKey: groupId:string
              currentKey: groupId:string 
```

  
**parentKey** and **currentKey** are support also for objects deep hierarchy:  
ex.: user.userId:number

##### Types

There 3 types allowed to use:  
***number*** for any number, **string** and **ObjectId** for mongodb bson  


##### Arrays


Arrays also widely supported. For these kind of objects:  
```{a: [{b: c}]}``` or ```{a: {b: [c]}]}```

can be used ```a.b.c``` key ( or for example with type ```a.b.c:number```)


##### Options

All options are not required.  

**start**: Inital collection    
**limit**: collection limit  
**sort**: sort collection  
**projection**: mongodb projections (useful for huge documents)  
**query**: Specific db query


 