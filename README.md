![example](https://st4.depositphotos.com/12141488/20550/v/450/depositphotos_205505540-stock-illustration-scratched-textured-example-stamp-seal.jpg)

# demo project (Python,docker,redis,mongodb)

## The project based on requirements:

* Design and implement a school system for managing students, course & grades.
    - API systems to create and modify Students, Courses and Grades.
        - RESTful over HTTP (CRUD)
    - Provide statistical calculations over this data.
        - the student with the highest average in courses (limited to  return one of them).
        - the easiest course (the one with the highest average grades)
        - Implemented cache mechanism (based on redis)

    
##### Data Models in project:
Student

    Id              -> String Object (Autoinc ID)
    First name      -> String
    Last name       -> String
    Email           -> String
    
Course
    
    Id              -> String Object (Autoinc ID)
    Name            -> String
    Students        -> String

Grade

    Grade           -> Intager
    Student         -> String (ID from sudents collection)     
    Course          -> String (ID from courses collection)


## Project installation:
basically installation requires docker & docker compose installed on machine:
the installation will setup/install 4-dockers
* redis
* mongoDB
* python/script machine
* nginx web server

for installation run:
```shell script
$ docker-compose up --build
``` 
## Project endpoints:
Management url / GUI editor:

    http://localhost/manager
    
### RESTful API:
#### List collection records
Each collection (students | courses | grades) can be retrieved by request

     GET   http://localhost/api/[students|courses|grades]
     *** REPLACE localhost to your deployment address or domain
     *** in url request use only one collection from (students | courses | grades)
  
Example:
```sh
$ curl -i -H 'Accept: application/json' http://localhost/api/students
```  
```js
var URL="http://localhost/api/students";

var xhr = new XMLHttpRequest();
xhr.open('GET', URL, true);
xhr.responseType = 'json';
xhr.onload = function() {
	console.log(xhr.status);
	console.log(xhr.response);
};
xhr.send();
```
#### Create a new record
POST - create a new record in collection
(student / course / grade)
Each collection record can be created by request

     POST   http://localhost/api/[students|courses|grades]
     *** the fields/data transfered in a POST body
     *** the filds you can find at top of this readme "Data Models in project"
     *** REPLACE localhost to your deployment address or domain
     *** in url request use only one collection from (students | courses | grades)
  
Example:
```sh
$ curl -i -H 'Accept: application/json' -d 'firstName=John&lastName=Doe&email=abuse@gmail.com' http://localhost/api/students
```  
```js
var URL="http://localhost/api/students";

var xhr = new XMLHttpRequest();
xhr.open('POST', URL, true);
xhr.responseType = 'json';
xhr.onload = function() {
	console.log(xhr.status);
	console.log(xhr.response);
};
xhr.send(JSON.stringify({ "email": "abuse@gmail.com", "firstName": "John","lastName": "Doe" }));

```

####Update a record
PUT - update record in collection
(student / course / grade)

     PUT   http://localhost/api/[student|course|grade]/[RECORD_ID]
     *** the fields/data transfered in a PUT body (like in a POST method)
     *** the filds you can find at top of this readme "Data Models in project"
     *** REPLACE localhost to your deployment address or domain
     *** in url request use only one collection from (student | course | grade)
     *** specify the record ID in request
  
Example:
```sh
$ curl -i -H 'Accept: application/json' -d 'firstName=John&lastName=Doe&email=abuse@gmail.com' http://localhost/api/student/5e38a31ad272c0000cdcfad7
```  
```js
var recorID="5e38a31ad272c0000cdcfad7";
var URL="http://localhost/api/student/"+recorID;

var xhr = new XMLHttpRequest();
xhr.open('PUT', URL, true);
xhr.responseType = 'json';
xhr.onload = function() {
	console.log(xhr.status);
	console.log(xhr.response);
};
xhr.send(JSON.stringify({ "email": "abuse@gmail.com", "firstName": "John","lastName": "Doe" }));

```


#### Delete a record
DELETE - method used to delete record from collection
(student / course / grade)

     PUT   http://localhost/api/[student|course|grade]
     *** REPLACE localhost to your deployment address or domain
     *** in url request use only one collection from (student | course | grade)
     *** specify the record ID in request
  
Example:
```sh
$ curl -i -H 'Accept: application/json' -X DELETE http://localhost/api/student/5e38a31ad272c0000cdcfad7
```  
```js
var recorID="5e38a31ad272c0000cdcfad7";
var URL="http://localhost/api/student/"+recorID;

var xhr = new XMLHttpRequest();
xhr.open('DELETE', URL, true);
xhr.responseType = 'json';
xhr.onload = function() {
	console.log(xhr.status);
	console.log(xhr.response);
};
xhr.send();

```
