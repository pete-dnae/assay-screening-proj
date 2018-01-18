# Assay Screening Technical Briefing

# Table of Contents
- Intro and Overview
- Computing Architecture Overview
- Developer getting started instructions

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
represent universally used things. These will include things like the Organisms
we are working with, Strains, bought-in reagents, and our ever-evolving
standardised primers for example. The Web App will aid the scientists in
managing and curating these shared resources.

The other side to the database is that it contains Experiments. Scientists can
create and then design experiments in the Web App, which get saved in the
database. An experiment design will for example declare which primers are going
to be used in that experiment and similar, and then will go on to define a set
of allocation rules that reflect the scientists strategy. As you would expect
the scientist will be able to see the plate layouts visually in the App - but
unlike today's spreadsheets, these allocations will be automatically generated
on the fly from the allocation rules the scientist has put in, and consequently
become very much easier to change and iterate on, and immune from spreadsheet
thinking and typing errors.

We anticipate the app being extended fairly continuously to cover things like
automating the programming of lab robots. And helping to keep track of such
things as reagent batch numbers.

# Computing Architecture Overview

What you see is a Web App that shows you visually, the experiments avaiable,
the details of each of them, the various primers, organisms, etc that are
registered in the system. And then offers various forms and screens and so on
to let you create new experiments, and edit them etc. This Web App is a modern
Javascript application that runs in your browser. It follows the *Single Page 
Application* architecture. And uses the *Vue.js* web framework, with the Vuex
extension to manage application state. Plus the *Bootstrap* CSS library.

Most of the logic and intelligence for the application resides in a back-end web
service running in the Cloud. The Web App has a conversation with the back-end
web service in order to decide what to show, at any one time, and it also sends
messages to it when the user edits things, so that the web service can reply with
changes in what to show in the new state. This conversation uses the *REST*
communication methodology. The backend web service is implemented in Python using
the *Django* framework, plus the *Django Rest Framework* extension. There is only
one backend web service, but there can be multiple simultaneous Web App's being
used by scientists all talking to the back end at once.

The web service in the cloud is hosted on the *Heroku* Platform-As-A-Service
(PAAS). Behind the web service is a database as the permanent data-store, and
this is a *Relational* type database. In this case a cloud deployment of
*PostgreSQL* provided as part of Heroku's PAAS.

# Developer Getting Started Instructions

## Prerequisites
- Python 3 installed
- A virtual env installed
- git installed
- heroku command line client installed 
    https://devcenter.heroku.com/articles/heroku-cli

Create root directory of your choice, that we'll call <foo>.

    cd foo
    # activate your virtual env
    git clone https://github.com/pete-dnae/assay-screening-proj .
    pip install -r requirements.txt

Quick test so far...

    python manage.py runserver # just to see if python env is viable.
    # then quit the server

Database initialisation
    
    # When running locally you get a pre-configured sqlite database, which
    # is included in the pip install above.
    Find and delete the sqlite3 file in foo
    Find and delete any migration files in foo/app
    python manage.py makemigrations 
    python manage.py migrate

    # If you want to populate the database automatically with our reference
    # experiment do this bit...

    python manage.py reset_db


Run the server to test the REST API
    
    python manage.py runserver
    # point browser at: http://localhost:8000/
