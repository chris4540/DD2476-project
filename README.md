# DD2476-project
DD2476 - Search Engines and Information Retrieval - User Profiling
project. Test.


## Tasks
- [x] Log the basic behaviour of the user on the search engine
- [x] The user profile with vector space model
- [x] Time/session evoluting user profile
- [x] Reordering 

## Getting tf-idf score from elastic with the current docuement
https://stackoverflow.com/questions/42220764/elasticsearch-getting-the-tf-idf-of-every-term-in-a-given-document

## Reference to the old project
https://github.com/gondor2222/DD2476_project

## Possible to do comparsion
https://github.com/tejasadhav/pws-search

## Experiement
1. base line exp: with/without user profiling
2. compare different weigting of the static vs dynamic profile


## How to use it for the experiment
1. create the user profile database  
    1. Go to ```<repo>/usr_profile_db/```
    2. run the script ```create_db.sh```
    3. you can fine tune the static profile by editing ```data.sql```
2. plot the word cloud see if it works
3. run the experiement 