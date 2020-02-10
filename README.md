# The Waters Relationship Selection Task (WRST)

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run the app locally you will need to have the following installed:

python 3.6+
redis-server
postgres (psql)

### Installing

Once you have cloned the repository you should create a virtual environment to work in:

```
virtualenv venv
source venv/bin/activate
```

Now you can install the appropriate packages via the requirements.txt file:

```
pip install -r requirements.txt
```

This should install all the packages that you need to run the app.

Installing the autoenv packages will make it very easy to configure your local development environment and not have to repeat the process again.  Do this as follows:

```
deactivate
pip install autoenv==1.0.0
touch .env
```

Then in your .env file add the following lines:

```
source env/bin/activate
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/wrst"
export REDIS_URL="redis://localhost:6379"
```

Now run the following commands in your terminal:

```
echo "source `which activate.sh`" >> ~/.bashrc
source ~/.bashrc
```

Now, whenever you cd back into the wrst directory it will automatically activate your virtual environment and configure the local environment variables.

## Configuring the database locally

Before running the app locally, you need to configure and specify the database that will be used for logging.  This can be done in two steps:

Step 1: Create a local database

Note we are using the name wrst here to match the environment variable set above.  You can name the database whatever you'd like but need to be consistent.

```
CREATE DATABASE wrst
```

You will not need to create any tables in the database.  These will be automatyically configured when the app is run

## Running the app locally

You will need to have a local redis-server instance running.  To do this, open a new terminal window and type:

```
redis-server
```

(Optional) If you want to see the database writes while the app is running you can do this by opening a terminal window and typing:

```
psql wrst
```

Now, you can run the app itself. Open another terminal window and go to the top level directory of the wrst app.  Now type:

```
python -m wrst.app
```

You can then open your browser and type the following URL:

```
http://127.0.0.1:5000/login_test/
```

which should show the wrst consent form for tesst users.

## Deployment

Deploying the app to Heroku is simple.  First we add the appropriate remote:

```
git remote add pro git@heroku.com:wrst-stage.git
git remote add pro git@heroku.com:wrst-pro.git
```

Then you can simple add/commit/push in the usual way, e.g.:

```
git add .
git commit -m 'whatever message'
git push stage master
git push stage master
```

## Authors

* **Drew Waters**
* **Debshila Basu Mallick** 