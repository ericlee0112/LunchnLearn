# Before you start
1. Make sure you have python version 3.0 or higher
2. Make sure you have pip version 19 or higher
3. Install Docker
# How to set up environment
clone the repository
```
git clone https://github.com/asabedia/LunchnLearn.git
```
open up your terminal, cd into the project, and run the launch_db shell script, this will spin up the postgresql database on a docker container. Also, if you do not have Docker installed, please install it first before running the command below. I have provided a link to follow to install Docker below.
https://docs.docker.com/install/
```
sh launch_db.sh
```
After you run the command above, you should see in your terminal that the database system is ready to accept connections. 

Assuming that no errors were encountered from running launch_db.sh, you can then create a virtual environment, this is where you will install your dependencies in.
To do this, you run:
```
virtualenv name_of_your_virtual_environment
```
Virtualenv should already be pre-installed if you are using Python version 3.0 or higher, but if you dont, you should update your python version and run this command:
```
python3 -m pip install --user virtualenv
```
Now that you have a virtual environment set up, now it's time to boot up your virtual environment.
```
source name_of_your_virtual_environment/bin/activate
```
Assuming that nothing went wrong, you can now install the dependencies for this project. You can do this by running:
```
pip install -r requirements.txt
``` 
Now that you have your dependencies installed, you must then run all migrations to set up tables by going into lunch_and_learn:
```
cd lunch_and_learn
```
And then:
```
python manage.py makemigrations
python manage.py migrate
```
Assuming that nothing went wrong, you can then insert fake data for the Postgres database. 
Then, you run:
```
python manage.py loaddata fixtures/demo_test_data.json
```
This will load fake data into the Postgres database

Finally, you can boot up the application by running:
```
python manage.py runserver
```
It is suggested that you use Google Chrome to view this application
Go on to localhost:8000 to view the lunch and learn application
