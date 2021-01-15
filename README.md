# TDS_APP

#### This is a Traffic Director System. Main purpose of this app is to allow users to create short links and to track statistics of requests...
#### The application is written in Python3.8/Django3.1.5 and HTML. The TDS APP contains User Management System and it is powered with PostgreSQL database.

#### The TDS_APP is deployed on Heroku and it can be found in following link: [here](http://tdsproject.herokuapp.com/)

##### Run TDS_APP locally you need to:
##### Clone the project from git repository:
```
git clone https://github.com/dragosavac/TDS_APP
```

##### Create and activate Python virtual environment

```
python3 -m venv venv
. venv/bin/activate
```
##### Install dependencies

```
pip3 install -r requirements.txt
```
##### Enter database credentials in .env file

```
SECRET_KEY=SECRET_KEY
NAME=DB_NAME
USER=DB_USER
PASSWORD=DB_PASSWORD
HOST=DB_HOST
PORT=DB_PORT

```

##### If you're into testing email functionalities, email credentials in .env file but don't have tpo bother with it


```
MAIL_HOST_PASSWORD=MAILAPPPASSWORD
EMAIL_HOST_USER=MAIL
EMAIL_HOST=smtp.gmail.com
```

##### Make migrations

```
python manage.py makemigrations

```
##### Migrate

```
pyhon manage.py migrate
```

##### Create superuser

```
python manage.py createsuperuser
```
##### Runserver locally
```
python manage.py runserver
```

Almost every feature can be tested locally, except redirection functionalities

You can test LinkStatistics locally page by entering data in Admin Panel

##### Tips for testing redirect links on Heroku server

1. Tap on Create Short Url button on Home page 
2. Parameter stands for randomly generated short url parameter
3. Link stands for default link where user should be redirected, if no rule for weights and countries match
4. Click on randomly generated link, to see if you will be redirected on right page
5. Check LinkStats and ClickStats to see the details of requests

