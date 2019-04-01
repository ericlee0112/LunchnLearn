# Before you start
1. Make sure you have python version 3.0 or higher
2. Make sure you have pip version 19 or higher
3. Install Docker
# How to set up environment
clone the repository
```
git clone https://github.com/asabedia/LunchnLearn.git
```
open up your terminal, cd into the project, and run the launch_server shell script, this will spin up the postgresql database on a docker container and will migrate the database schemas and the fixture data to the postgres database. The script will then create a python virtual environment called 'lnlvenv' and install the required dependencies. Finally this command will also run the Django server on localhost:8000. If you do not have Docker installed, please install it first before running the command below. I have provided a link to follow to install Docker below.
https://docs.docker.com/install/
```
bash launch_server.sh
```
After you run the command above, you should see in your terminal that the server is ready to accept requests. 

# Notes
- the server should be running on 'localhost:8000/' and not 'http://127.0.0.1:8000/'
