# Assay Screening Technical Briefing

# Table of Contents

* Intro and Overview
* Computing Architecture Overview
* Developer getting started instructions

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
database. An experiment design is centered around what we call a *Rules
Script*. This is a mini-program in a very simple domain specific language. It's
little more than a series of *plate* declarations, interspersed with lines of
text that say "I want to put this *reagent* and this *concentration* into these
cells". You can specify the cells singly, in blocks or in sets. You can also
put in similar lines that describe the *transfer* of some liquid from a well on
plate into some well(s) on another.

The Web App provides an editor for this script, and shows alongside the
resultant allocation that the user is defining with the rules script, by way of
feedback.

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

Most of the logic and intelligence for the application resides in a back-end web
service running in the Cloud. The Web App has a conversation with the back-end
web service in order to decide what to show, at any one time, and it also sends
messages to it when the user edits things, so that the web service can reply
with changes in what to show in the new state. This conversation uses the _REST_
communication methodology. The backend web service is implemented in Python
using the _Django_ framework, plus the _Django Rest Framework_ extension. There
is only one backend web service, but there can be multiple simultaneous Web
App's being used by scientists all talking to the back end at once.

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


Smoke test the server will serve

    python manage.py runserver # just to see if python env is viable.
    # then quit the server

Database initialisation

When running locally you get a pre-configured sqlite database, which is 
included in the pip install above.

To build for the first time or to stomp on any previous database and re baseline
it to a suitable virgin state that contains one reference experiment object and
its deep tree of dependencies do this:

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

Building the app for deployment:
From root directory <webapp>
yarn build
