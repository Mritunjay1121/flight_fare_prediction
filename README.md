# flight_fare_prediction

Creating the environment


conda create -p flight_fare_prediction python==3.7 -y
...

Activating the environement


conda activate C:\Users\mritu\PycharmProjects\Projects\flight_fare_prediction\flight_fare_prediction\flight_fare_prediction\flight_fare_prediction #
...

Installing libraraies written in requirements.txt

pip install -r requirements.txt 
...git 

To ignore a file , write its name inside gitignore so that it should not be on the github

To check Git Status

git status
...

To push some files onto the github.

git add <filename> 
    or
git add . 

To add all files
...


Used to see the versions


git log
...

To create or save changes/versions 

git commit -m "<any message>"
...


To send the chaanges to git

git push origin main
...

To check remote url

git remote -v
...

To setup CI/CD Pipeline in heroku we need 3 informations

1. Heroku Email :   mritunjay.1121@gmail.com
2. Heroku API Key : f9fead10-4fb3-443f-ba99-d10ecb9fb4b9
3. Heroku App Name: p1-flight-fare-prediction


Create a Dockerfile inside main directory and write the code there for the configuration of virtual machine


BUILD DOCKER IMAGE
...

docker build -t <image_name>:<tagname> .
...

Note : Image name should for docker must be in lowercase


To list dockerimages
...

docker images


Run docker image
...

docker run -p 5000:5000 -e PORT =5000 <docker image id>
...

To check running container in docker
...

docker ps
...

To stop docker container
...

docker stop <container id>
...

Now , set the changes to github

