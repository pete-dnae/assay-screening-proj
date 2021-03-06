# Assay Screening Technical Briefing

# Table of Contents

* Intro and Overview
* Computing Architecture Overview
* Developer getting started instructions
* Deployment

# Intro and Overview

This project provides a Web App to help scientists design and run experiments
which comprise a matrix of Assays deployed to chambers on a plate(s). The crux
of the challenge is how to mix and dilute Reagents, in some cases recursively,
and then to allocate variations of these mixtures to each chamber.

The allocations which the scientists wish to make reflect strategies. The
strategies will be introducing controlled changes to levels in each mixture of
such things as human dna presence and target strain concentrations. Typically
these things are allocated so as to change gradually as you move down or across
a plate, or in blocks on the plate.

The incumbent tooling (which this app seeks to replace) are hand-edited
spreadsheets. These are very time consuming to work with and problematically
error-prone. They also defeat the notion of there being a single-source of
truth within the company on these matters because the spreadsheets can be
copied, modified and distributed at will.

The Web App will use a centralised database behind the scenes to provide
a unitifed single source of truth for all users. The user experience for
scientists to use it is a Web App accessible from their browser.

The app presents a model whereby some entities in the database are shared and
represent universally used things. These will include things like the Reagent
names we are working with. Standardised groups of primers for example. The Web
App will aid the scientists in managing and curating these shared resources.

The other side to the database is that it contains Experiments. Scientists can
create and then design experiments in the Web App, which get saved in the
database.

An experiment design is centered around what we call a *Rules
Script*. This is a mini-program in a very simple domain specific language.
Like this: (Taken from app/model_builders/reference_data.py)

    V ver-1
    P Plate1
    A Titanium-Taq              1-12  A-H 0.02 M/uL
    A (Eco)-ATCC-BAA-2355       1,5,9 B   1.16 x
    A (Eco)-ATCC-BAA-9999       2     C,D 1.16 x
    # This is a comment
    P Plate42
    T Plate1 1 B                1-12  A-H   20 dilution
    A Pool_1                    1-3   A-H    1 x
    A Ec_uidA_6.x_Eco63_Eco60   4-9   A-H  0.4 uM

It's little more than a series of *plate* declarations, interspersed with lines
of text that say "I want to put this *reagent* and this *concentration* into
these cells". You can specify the cells singly, in blocks or in sets. You can
also put in similar lines that describe the *transfer* of some liquid from a
well on plate into some well(s) on another.

The Web App provides an editor for this script, that provides live graphical
feedback on the allocation being created.

We anticipate the app being extended fairly continuously to cover things like
automating the programming of lab robots. And helping to keep track of such
things as reagent batch numbers.

# Computing Architecture Overview

What you see is a Web App that shows you visually, the experiments avaiable,
and the details of each of them.  It offers various forms and screens and so on
to let you create new experiments, and edit them etc. This Web App is a modern
Javascript application that runs in your browser. It follows the _Single Page
Application_ architecture. And uses the _Vue.js_ web framework, with the Vuex
extension to manage application state. Plus the _Bootstrap_ CSS library.

Much of the logic and intelligence for the application resides in a back-end
web service running in the Cloud. The Web App has a *conversation* with the
back-end web service in order to decide what to show, at any one time, and it
also sends messages to it when the user edits things, so that the web service
can reply with changes in what to show in the new state. This conversation uses
the _REST_ communication methodology. The backend web service is implemented in
Python using the _Django_ framework, plus the _Django Rest Framework_
extension. There is only one backend web service, but there can be multiple
simultaneous Web App's being used by scientists all talking to the back end at
once.

The web service in the cloud is hosted on the _Heroku_ Platform-As-A-Service
(PAAS). Behind the web service is a database as the permanent data-store, and
this is a _Relational_ type database. In this case a cloud deployment of
_PostgreSQL_ provided as part of Heroku's PAAS.

# Developer Getting Started Instructions (Back End)

## Prerequisites

* Python 3 installed
* A virtual env installed
* git installed
* heroku command line client installed
  https://devcenter.heroku.com/articles/heroku-cli

Create root directory of your choice, that we'll call <foo>.

    cd foo
    git clone https://github.com/pete-dnae/assay-screening-proj .
    # activate your virtual env
    pip install -r requirements.txt

Run the unit tests

    # These work automatically on a transient, in-memory database. They are not
    # dependent on you having initialised a database, and won't touch your real
    # database even if you have one set up.

    cd foo

    # To run all the unit tests
    python manage.py test

    # To run a particular unit test.
    python manage.py test app.tests.test_xxx # no .py extension


Smoke test the API server will serve

    python manage.py runserver # just to see if python env is viable.
    # then quit the server

Database initialisation

When running locally you get a pre-configured sqlite database, which is 
included in the pip install above.

To build for the first time or to stomp on any previous database and re
baseline it to a suitable virgin state that contains one reference experiment
object and its deep tree of dependencies do this:

    Automated for Linux as follows:
    For more information, see documentation the script source.

    cd foo
    ./complete_reset.bash

    Nb. Under the hood this uses a custome python manage.py script, which can be
    found (as required) in foo/app/management/commands.

    See also the scripts in the commands directory, for some more
    finely-grained maintenance automation.

Run the server to test the REST API

python manage.py runserver # point browser at: http://localhost:8000/

# Getting Started for web application

## Prerequisites

#Tools for development
-Node https://nodejs.org/en/
-Yarn https://yarnpkg.com/en/docs/install
#Tool for debugging
-Vue devtools https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd?hl=en

#Placeholder
<webapp>=assay-screening-proj/webapp/

Installation of packages:
From root directory <webapp>
yarn install

Starting up dev server:
From root directory <webapp>
yarn dev
#point browser at http://localhost:8080/

#heroku installation
Download heroku client at https://devcenter.heroku.com/articles/heroku-cli#getting-started

Open command prompt 
    cd <foo>
Type in
    heroku login 
    username:pete.howard@dnae.com
    pass:qa3ZU5Q7
After login
    heroku create
This will create a remote repo under the name heroku in git config.

#Deployment

The app is served from https://assay-screening.herokuapp.com/

This is a PAAS infrastructure.
Account User name and credentials are:
    pete.howard@dnae.com
    Pass: qa3ZU5Q7

    Admin superuser
    admin, pass kTaDN5RV
    Backup admin email pete.howard@dnae.com

The API is served from lives at /
The Web App lives at /static/index.html

Make a deployable build and commit it
    (assumes no schema changes, and not the first ever time!)

    git checkout master # We're deploying from master right now
    git pull (whatever you've called your upstream github)
    Build the app for deployment:
    From root directory <webapp>
    yarn build
    git add --all
    git commit (say this is a deployed build in the commit comment)
    git push (whatever you've called your upstream github)

Send it to heroku
    heroku login
    git push heroku master # the heroku remote is set up automatically
    # if you want confirmation of the URL being served from...
    heroku open

Tips for editing production DB:
Point browser to admin ulr https://assay-screening.herokuapp.com/admin
Use the following credentials to log in
User :admin, 
pass :kTaDN5RV

On successful login you will be provided with a list of tables
available in the current DB.
Click on change button to proceed to editing.


Resetting Production DB:
    
    Take a copy of existing rulescripts and note their experiment name
    Take a copy of existing units

    Log in to https://dashboard.heroku.com using below credentials
    pete.howard@dnae.com
    Pass: qa3ZU5Q7

    Under Installed add-ons click on Heroku Postgres:
        Go to durablity tab to take a manual backup of db in case of
        emergency
        Go to settings tab and click on reset database , enter project
        name when prompted.

    In app dashboard(https://dashboard.heroku.com/apps/assay-screening)
    Run a web console by clicking on 'Run Console' option from 'More^'
    dropdown
    Type 'bash' to open a bash console when prompted.
    on bash prompt type in the following commands from project root:
        hint:bash defaults to project root

        # Remove the migration files if there are any.       
        rm -rf app/migrations

        # Make the Django migrations and run them to create the db and tables.
        python manage.py makemigrations app
        python manage.py migrate

        # Further populate the database with the reference experiment.
        python manage.py pop_with_ref_exp

        # Now bulk load reagents and groups
        python manage.py bulk_load_reagents app/model_builders/customers-seed-data/reagents.csv

        python manage.py bulk_load_groups app/model_builders/customers-seed-data/pools.csv

        # populate units manually from http://assay-screening.herokuapp.com/api/units/

        re-enter rulescripts on front end 


Tips for upgrading production DB:
    Note: Before upgrading production db you should have already purchased db addon for 
    upgraded version of the db ex foo db
    
    In Heroku Client :
        Run heroku config --app assay-screening to know all the db addons available
        Run heroku maintenance:on --app assay-screening to take down the application 
        temporarily to prevent any db writes
        Run heroku pg:copy DATABASE_URL HEROKU_POSTGRESQL_foo_URL --app assay-screening 
        to copy data from current db to foo db  
        Run heroku pg:promote HEROKU_POSTGRESQL_foo_URL --app assay-screening to promote
        the foo db as primary db for the app
        Run heroku maintenance:off --app assay-screening to bring app back online
        Run heroku addons:destroy HEROKU_POSTGRESQL_CHARCOAL_URL --app assay-screening
        to delete the old db
