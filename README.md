# WIKILNKS

DTU - 02807 Computational Tools for Data Science - Project

Wikilinks is a system that lets anyone find the shortest path between two wikipedia articles, only using links

![Wikilinks Interface](https://github.com/EmilieTrouillard/ComputationalTools/blob/master/wikilinks.png)

## Prerequisites

* Python 3, Packages:

    * [MrJob](https://pythonhosted.org/mrjob/)

    * [numpy](http://www.numpy.org/)

    * If you want to be able to run the interface and the graph database, you will also need: 

        * [Flask](http://flask.pocoo.org/docs/1.0/quickstart/)

        * [neo4j-driver](https://neo4j.com/developer/python/)


## Create your own wikilinks

Learn here how to replicate the wikilinks path finder between two wikipedia articles on a sample (smaller) data set.
All necessary data is present in the ```sample``` folder, and all output data will be stored there as well.

#### Preprocessing

The first step of the preprocessing is to create ids for the titles:
```
ComputationalTools$ python preprocessing/indexcreation_mapReduce.py
```

Then, before creating the graph that links all pages, it is needed to store what are the redirect pages so they are later not considered in the graph.
```
ComputationalTools$ python preprocessing/redirectcreation_mapReduce.py
```

Once done, it is now time to create the actual graph (as a txt file)
```
ComputationalTools$ python preprocessing/graphcreation_mapReduce.py
```

#### BFS:

*STANDARD BFS*

Getting the shortest path between two articles using standard bfs relies on the ```bfs/BFS.py``` script. It can be called with the command:
```
ComputationalTools$ python bfs/BFS.py $inputFile$ $options...
```

With the sample graph file being present in ```sample/graphfile``` as ```$inputFile$```. To learn more about the options, you can run:

```
ComputationalTools$ python bfs/BFS.py -h
```

Example of an actual command:
```
ComputationalTools$ python bfs/BFS.py sample/graphfile -sn Apollo -en Alpha -ti sample/title_to_id -it sample/id_to_title
```

*MAP REDUCE SHORTEST PATH*

For the implementation of the shortest path using map reduce bfs:
```
ComputationalTools$ python bfs/MRBFS_main.py $inputFile$ $options...
```

Here again, if more details about the arguments and possible options, run:
```
ComputationalTools$ python bfs/MRBFS_main.py -h
```

Exemple of an actual running command:
```
python bfs/MRBFS_main.py sample/graphfile -s 0
```


#### Graph DB + Interface

To run the wikilinks interface, it is necessary to populate the graph database that serves the data first. For that matter, it is needed to create csv files containing the nodes and edges of the graph that will later be imported in the db.
```
ComputationalTools$ python preprocessing/createCSV.py
```

To proceed with the next steps, it is needed to have ```neo4j``` installed. To learn more about ```neo4j```, head over to the [neo4j section](#NEO4J). 
You can then copy the given csv files to a place where the database can import from them. Then run the following command with ```$NEO4J_FOLDERS$```being the home folder of ```neo4j```. (See [Neo4j File Locations](https://neo4j.com/docs/operations-manual/current/configuration/file-locations/) to learn where it is).
```
cp sample/nodes_wikilinks.csv $NEO4J_FOLDER$/import/ && cp sample/relationships_wikilinks.csv $NEO4J_FOLDER$/import/
```

If you have neo4j already running, stop it.
```
NEO4J-FOLDER$ ./bin/neo4j stop
```

The following commands imports the csv files in database. Make sure that you don't have any databse called ```wikilinks``` If you need help regarding neo4j, see the [neo4j section](#NEO4J).
```
NEO4J-FOLDER$ ./bin/neo4j-admin import --database wikilinks.db --id-type INTEGER --nodes:Page "import/nodes_wikilinks.csv" --relationships:LINKS_TO "import/relationships_wikilinks.csv" --delimiter ";" --array-delimiter "|"
```

It is now necessary to update the default database for ```neo4j```. Modify the config file
```
NEO4J-FOLDER$ nano conf/neo4j.conf
```

and then update the active database field with the database. 
```
dbms.active_database=wikilinks.db
```

Now verify that the database runs smoothly:
```
NEO4J-FOLDER$ ./bin/neo4j console
```
And verify that you can access it at ```localhost:7474```. 

If the database starts, you can now stop it 
```
NEO4J-FOLDER$ ./bin/neo4j stop
```

and boot it again as a daemon.
```
NEO4J-FOLDER$ ./bin/neo4j start
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

Go to ```http://localhost:5000/``` or ```http://localhost:8080/``` and you can now experiment around! Be advised not articles exist on this sample set. Ex of a query: Anthropology & Anarchism.


**/!\ NOTE**:
There is no reason why would anyone's database config would be the same as ours. We created a db config file for one to change the credentials of the database in 
```
ComputationalTools/graphdb/dbconfig.py
```


#### All Pairs Shortest Paths:

The script that generates all the shortest paths behind any pair of articles can be found in the ```apsp/``` folder. It can be called running the command:
```
ComputationalTools$ python apsp/MRAPSP_main.py $inputFile$ $options...
```

Once more, to learn more about the possible options, run:
```
ComputationalTools$ python apsp/MRAPSP_main.py -h
```

As an example, you can run the following command: 
```
ComputationalTools$ python apsp/MRAPSP_main.py sample/graphfile
```

You're done! ;)

====================================================================

===================== FOR PROJECT CONTRIBUTORS =====================

====================================================================

## Project architecture and development information

The project is split in several subfolders to improve understandability.

* apsp: Stores script generating shortest paths for all pairs (all pairs shortest path).

* bfs: Stores everything related to bfs (standard & map reduce versions).

* data: Stores all data used in the project.

* graphdb: Stores all files related to the graph database.

* interface: Stores everything related to the interface of the wikilinks system.

* preprocessing: Stores all scripts used to pre-process wikipedia's data.

* sample: directory used for demo purposes.


## Git Instructions

We will keep the gitflow simple with a single unprotected master branch. This requires to be disciplined about pushes&pulls. (Loads of merge requests will appear otherwise.)

Always remember to pull before pushing ```git pull origin master```

When you want to push new work: ```git add -p```. This will enter an interactive mode where you can verify the modifications you want to push. Please avoid ```git add .``` if possible. 

Then ```git commit -m "{COMMIT MESSAGE.}"``` to commit and finally ```git push origin master``` to push your changes. 

Note: If you fucked up something and want to drop a commit, you can do see by using the interactive mode of rebase ```git rebase -i```. Once done you will have to force push on master to save your rebase. PLEASE TELL THE OTHERS BEFORE FORCE PUSH.

Good Luck!

## Interface

To start the interface, simply run: 

```export FLASK_APP=backInterface.py``` 

(```export FLASK_ENV=development``` for dev) 

and then ```python -m flask run```. 

/!\ To do this it is necessary to have flask installed. (If you are not using a virtualenv, it highly recommended to learn more about them, see [here](https://docs.python-guide.org/dev/virtualenvs/))

```
pip install flask
```

(See [here](http://flask.pocoo.org/docs/1.0/installation/) for details), 

as well as the neo4j-driver.

```
pip install neo4j-driver
```
(See [here](https://neo4j.com/developer/python/) for details).


#### NEO4J

See [installation](https://neo4j.com/docs/operations-manual/current/installation/).

*Changing Database*

Edit the neo4j conf file. (See [File Locations](https://neo4j.com/docs/operations-manual/current/configuration/file-locations/)) to know where it is located. (Ex given on Debian)
```
nano /etc/neo4j/neo4j.conf
```

and then update the active database field with the database of your choice.

```
dbms.active_database=wikilinks.db
```

(We are using 'wikilinks')

and restart the database.

*Changing Password*

At the start, the password of any database will be _neo4j_. See [here](https://neo4j.com/docs/operations-manual/current/configuration/set-initial-password/) to set a password.

*Start from shell*

Make sure the database runs. To boot it from shell, type in ```sh ./bin/neo4j start``` from the neo4j folder.

--------------------

## DEV OPS

[link for the server configuration](https://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/)

[link for https certification](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-debian-9)

#### DB Troubleshooting

(Steps for properNeo4j installation on debian)[https://neo4j.com/docs/operations-manual/current/installation/linux/debian/]

*Note*:

It's needed to connect to the browser interface once to set up the password. 

First modify the configuration of neo4j: ```nano /etc/neo4j/neo4j.conf``` by changing ```dbms.active_database=graph.db``` to ```dbms.active_database=wikilinks.db``` and by uncommenting the line ```dbms.connectors.default_listen_address=0.0.0.0```. 

Before starting neo4j, make sure the firewall has the right ports opened: ```sudo ufw allow 7474```, ```sudo ufw allow 7687``` (Don't forget to disable them once done!). 

Then start the database with ```sudo neo4j console``` and open the server on port ```7474```. 

Connect to it and it will ask you to change password. Once done, make sure the actual website works, disable the firewall, stop the instance of neo4j runner, enable the service and start it.

Import DB on server:

```sudo neo4j-admin import --database wikilinks.db --id-type INTEGER --nodes:Page "/var/lib/neo4j/import/nodesCleanTitles.csv" --relationships:LINKS_TO "/var/lib/neo4j/import/relationships_unique.csv" --delimiter ";" --array-delimiter "|"```
