# flight_fare_prediction

Creating the environment

```
conda create -p flight_fare_prediction python==3.7 -y
```

Activating the environement

```
conda activate flight_fare_prediction/
```

Installing libraraies written in requirements.txt

```
pip install -r requirements.txt 
```

To ignore a file , write its name inside gitignore so that it should not be on the github

To check Git Status

```
git status
```

To push some files onto the github.

```
git add <filename> 
```    

Or to add all files into github    

```
git add . 
```


Used to see the versions

```
git log
```

To create or save changes/versions 

```
git commit -m "<any message>"
```


To send the changes to gitub 

```
git push origin <branch_name>
```

To check remote url

```
git remote -v
```

To setup CI/CD Pipeline in heroku we need 3 informations

1. Heroku Email :   
2. Heroku API Key :
3. Heroku App Name: 


Create a Dockerfile inside main directory and write the code there for the configuration of virtual machine


BUILD DOCKER IMAGE

```
docker build -t <image_name>:<tagname> .
```

Note : Image name should for docker must be in lowercase


To list dockerimages

```
docker images
```

Run docker image

```
docker run -p 5000:5000 -e PORT =5000 <docker image id>
```

To check running container in docker

```
docker ps
```

To stop docker container

```
docker stop <container id>
```

Now , set the changes to github

Create housing.
Create setup.py and configure it for requirements.txt file 

Run this setup.py
Using 

```
python setup.py install
```


"e ." is used to install housing folder


Make all folders inside housing

And fill logging and exception folders first


Install ipykernel to run a jupyter notebook

We are using jupyter notebook to check the code that is to be written finally into our project to use it we must install ipykernel

```
pip install ipykernel
```

Filling the entity folder to define entities


Now making an ".yaml" inside config folder . Config folder inside main directory.".yaml" file to store our database coming from url...


Basically this ".yaml" file stores the artifacts coming from different artifacts



To use config.yaml file we install PyYAML module

To do some small functionalities like reading the yaml file we write code in util.util.py

To use write all the constants(hard coded values) used we use housing.constant.__init__.py

Data Drift: If data statistics gets changed we call as data drift



We will use evidently.ai to monitor it. We will generate graphs of train and test sets. And distribution of each column will be seen from both the datasets. If they are not alligned then there is data drift.If stats of both datasets are same then we say 0% datadrift


In the json file generated by evidently there is a matrice key that will have data to generate matrix of the data 

If training pipeline is already running the new training cant start.

close local host port connection

```
netstat -ano | findstr : 5000
```

Then get Process id of the proces

```
taskkill /PID <PID> /F
```

Deployed [Here](http://ec2-18-207-195-244.compute-1.amazonaws.com:8080/)
