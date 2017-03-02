---
title: MongoDB Cheatsheet
category: databases
tags: NoSQL
---

## Import from CSV

```bash
mongoimport --db users --collection contacts --type csv --headerline --file contacts.csv
```

Specifying `--headerline` instructs mongoimport to determine the name of the fields using the first line in the CSV file.
Use the `--ignoreBlanks` option to ignore blank fields. For CSV and TSV imports, this option provides the desired functionality in most cases, because it avoids inserting fields with null values into your collection.

[MongoImport documentation](https://docs.mongodb.org/manual/reference/program/mongoimport/ )


## Make a Copy

Don't use copyTo - it is fully blocking... and deprecated in 3.x

```js
db = db.getSiblingDB("myDB"); // set current db for $out
var myCollection = db.getCollection("myCollection");

// via the Aggregation framework - project, get uniques if needed, create a new collection
myCollection.aggregate([{ $project:{"fulladdress":1}},{ $group:{ _id:"$fulladdress"}},{ $out:"myCollection2"}], { allowDiskUse:true }); 
  
// or use bulk update
var outputColl = db.getCollection( "myCollection2" );
var outputBulk = outputColl.initializeUnorderedBulkOp();
myCollection.find ( {}, { "fulladdress": 1, "count": 1 } ).forEach( function(doc) {
     outputBulk.find({ "fulladdress": doc.fulladdress }).update ( { $set : { "count": doc.count  } });
});
outputBulk.execute();
```

## Aggregation Tips

```js
// lowercase a string 
{ $project: { "address": { $toLower: "$address" } } },

// extract field within embedded document
{ $project: { "experience.location": 1 } },

// flatten 
{ $unwind: "$experience"},
{ $group: { _id: "$_id", locs: { $push: { $ifNull: [ "$experience.location", "undefined" ] } } } }
 
// output a collection
{ $out: "myCollection2" }

// get unique values 
{ $group: { _id: "$fulladdress" } }
```

## Print from a Cursor

```js
myCursor.forEach(printjson);

// or
while (myCollection.hasNext()) {
   printjson(myCollection.next());
} 
```