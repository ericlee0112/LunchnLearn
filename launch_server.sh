#!/usr/bin/env bash

ENV="lnlvenv"
bash launch_db.sh
python3 -m venv "$ENV"
source "$ENV"/bin/activate
pip install -r requirements.txt
cd  lunch_and_learn 
python3 manage.py migrate 
python3 manage.py loaddata demo_test_data
python3 manage.py runserver