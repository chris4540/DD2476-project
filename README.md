# DD2476-project
DD2476 - Search Engines and Information Retrieval - User Profiling
project. 

## How to index the data?
1. Install elasticsearch V6.3
2. Modify ./load_wiki_dataset/load_svwiki.sh to fit your elasticsearch (es) url
3. Run ./load_wiki_dataset/load_svwiki.sh

## How to use it for the experiment
1. create the user profile database  
    1. Go to ```<repo>/usr_profile_db/```
    2. run the script ```create_db.sh```
    3. you can fine tune the static profile by editing ```data.sql```
2. plot the word cloud see if it works
3. run the experiement

## How to run frontend?
1. Install virtual environment with Python 3.7 and all dependencies stated in requirements.txt
2. cd frontend
3. Check the configuration parameters in config.py, specifically elastic_host, to point to your elasticsearch installation
4. python ./frontend.py
5. Open browser in link stated in the console, probably it is http://localhost:5000
