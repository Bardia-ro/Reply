# Reply
Reply application API

In order to run this application you will need to run the following command in the
command line in order to install requirements file.

pip3 install requirements.txt

Then you will need to run the migrations by:

python3 manage.py makemigrations ReplyAPI
python3 manage.py migrate

Then you would be able to run the server locally by:

python3 manage.py runserver
