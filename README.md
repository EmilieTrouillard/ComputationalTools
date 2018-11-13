# ComputationalTools

Computational Tools for Data Science - project

### Project Architecture

The project is split in several subfolders to improve understandability.

* data: Stores all data used in the project.

* preprocessing: Stores all scripts used to pre-process wikipedia's data.

* bfs: Stores everything related to bfs.

* graphdb: Stores everything related to the graph database.

* interface: Stores everything related to the interface of the system.


### Git Instructions

We will keep the gitflow simple with a single unprotected master branch. This requires to be disciplined about pushes&pulls. (Loads of merge requests will appear otherwise.)

Always remember to pull before pushing ```git pull origin master```

When you want to push new work: ```git add -p```. This will enter an interactive mode where you can verify the modifications you want to push. Please avoid ```git add .``` if possible. 

Then ```git commit -m "{COMMIT MESSAGE.}"``` to commit and finally ```git push origin master``` to push your changes. 

Note: If you fucked up something and want to drop a commit, you can do see by using the interactive mode of rebase ```git rebase -i```. Once done you will have to force push on master to save your rebase. PLEASE TELL THE OTHERS BEFORE FORCE PUSH.

Good Luck!

### Interface

To start the interface, simply run: ```export FLASK_APP=backInterface.py``` and then ```python -m flask run```. /!\ To do this it is necessary to have flask installed. (See: http://flask.pocoo.org/docs/1.0/installation/)
