# ComputationalTools

Computational Tools for Data Science - Project

## Create your own wikilinks

Learn here how to replicate the wikilinks path finder between two wikipedia articles on a sample (smaller) data set.
All necessary data is present in the ```sample``` folder, and all output data will be stored there as well.

#### Preprocessing

The first step of the preprocessing is to create ids for the titles:
```
ComputationalTools$ python preprocessing/indexcreation_mapReduce
```

Then, before creating the graph that links all pages, it is needed to store what are the redirect pages so they are later not considered in the graph.
```
ComputationalTools$ python preprocessing/redirectcreation_mapReduce
```

Once done, it is now time to create the actual graph (as a txt file)
```
ComputationalTools$ python preprocessing/graphcreation_mapReduce
```

#### Graph DB + Interface

To run the wikilinks interface, it is necessary to populate the graph database that serves the data first. For that matter, it is needed to create csv files containing the nodes and edges of the graph that will later be imported in the db.
```
ComputationalTools$ python preprocessing/createCSV
```

You can then copy the given csv files to a place where the database can import from them.
```
cp sample/nodes_wikilinks.csv $NEO4J_FOLDER$/import/ && cp sample/relationships_wikilinks.csv $NEO4J_FOLDER$/import/
```

The following commands imports the csv files in database. Be careful to replace the ```$DATABASE_NAME$``` by the name of your own neo4j database. If you need help regarding neo4j, see the [neo4j section](#neo4j).
```
NEO4J-FOLDER$ sudo ./bin/neo4j-admin import --database $DATABASE_NAME$.db --id-type INTEGER --nodes:Page "import/nodes_wikilinks.csv" --relationships:LINKS_TO "import/relationships_wikilinks.csv" --delimiter ";" --array-delimiter "|"
```


Now that the database is functional, let's install all dependencies needed for the interface. It runs on [Flask](http://flask.pocoo.org/docs/1.0/quickstart/), a really lightweight python framework for web-development. 

It is always recommended to use virtual environments when dealing with python projects. See [here](https://virtualenv.pypa.io/en/latest/installation/) to learn how to install virtual-env. If you don't care about using a virtual env, you can still use the following commands, starting from ```cd interface```

```
ComputationalTools$ virtualenv -p python3 venv
ComputationalTools$ . venv/bin/activate
ComputationalTools$ pip install flask neo4j-driver
ComputationalTools$ cd interface
ComputationalTools$ export FLASK_APP=backInterface.py
ComputationalTools$ python -m flask run
```


**/!\ NOTE**:
There is no reason why would anyone's database config would be the same as ours. We created a db config file for one to change the credentials of the database in 
```
ComputationalTools/graphdb/dbconfig.py
```

#### BFS:

TODO

## Project Architecture

The project is split in several subfolders to improve understandability.

* bfs: Stores everything related to bfs.

* data: Stores all data used in the project.

* graphdb: Stores all files related to the graph database.

* interface: Stores everything related to the interface of the wikilinks system.

* preprocessing: Stores all scripts used to pre-process wikipedia's data.


## Git Instructions

We will keep the gitflow simple with a single unprotected master branch. This requires to be disciplined about pushes&pulls. (Loads of merge requests will appear otherwise.)

Always remember to pull before pushing ```git pull origin master```

When you want to push new work: ```git add -p```. This will enter an interactive mode where you can verify the modifications you want to push. Please avoid ```git add .``` if possible. 

Then ```git commit -m "{COMMIT MESSAGE.}"``` to commit and finally ```git push origin master``` to push your changes. 

Note: If you fucked up something and want to drop a commit, you can do see by using the interactive mode of rebase ```git rebase -i```. Once done you will have to force push on master to save your rebase. PLEASE TELL THE OTHERS BEFORE FORCE PUSH.

Good Luck!

## Interface & DB MISC

To start the interface, simply run: ```export FLASK_APP=backInterface.py``` (```export FLASK_ENV=development``` for dev) and then ```python -m flask run```. /!\ To do this it is necessary to have flask installed. (See: http://flask.pocoo.org/docs/1.0/installation/).

#### neo4j

See [installation](https://neo4j.com/docs/operations-manual/current/installation/).

**Changing Database**

edit the neo4j conf file. (See [File Locations](https://neo4j.com/docs/operations-manual/current/configuration/file-locations/)) to know where it is located. (Ex given on Debian)
```
nano /etc/neo4j/neo4j.conf
```

and then update the active database field with the database of your choice. 
```
dbms.active_database=wikilinks.db
```

(We using 'wikilinks')

and restart the database.

**Changing Password**

At the start, the password of any database will be _neo4j_. See [here](https://neo4j.com/docs/operations-manual/current/configuration/set-initial-password/) to set a password.

**Start from shell**
Make sure the database runs. To boot it from shell, type in ```sh ./bin/neo4j start``` from the neo4j folder.
