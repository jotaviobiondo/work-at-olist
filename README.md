# Library API 
![Django CI](https://github.com/jotaviobiondo/work-at-olist/workflows/Django%20CI/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/jotaviobiondo/work-at-olist/badge.svg?branch=master)](https://coveralls.io/github/jotaviobiondo/work-at-olist?branch=master)

This project is an implementation of [this test specification](#work-at-olist). It's a API to manage a library, providing operations to store and retrieve data of authors and books.

Application running at https://jotaviobiondo-library.herokuapp.com/

REST API Docs [here](API.md).

## Usage

### Requirements

- Python 3.8+
- PIP

### Running locally

1. Clone this repository.
2. Create virtualenv with `python -m venv library_venv`.
3. Activate virtualenv:
    - Unix or MacOS: `source venv/Scripts/activate`.
    - Windows: `venv\Scripts\activate`.
4. Install requirements with `pip install -r requirements-local.txt`.
5. Use the `local.env` file as a template to create a `.env` file.
6. Run `python library_project/manage.py migrate` to create the database structure.
7. Run the app with `python library_project/manage.py runserver`.

The app will run on http://localhost:8000/.

### Running tests

Execute the following command to run the tests:

```
python library_project/manage.py test library
```

## Importing Authors

To import a .csv file containing authors data, run the command `python library_project/manage.py import_authors <file.csv>` where `<file.csv>` is the path to the file to be imported.

For example, assuming there is a file named *authors.csv* in project's root directory, you can run the following command:

```
python library_project/manage.py import_authors authors.csv
```

## Development

I developed this project using PyCharm IDE on PC running Windows 10. I used some parts of [this template](https://github.com/osantana/quickstartup-template), from [@osantana](https://github.com/osantana), mainly for configuring the application to deploy to [Heroku](https://www.heroku.com/) (the PaaS provider of choice).

These are the libraries I used to build this project:

- [Django](https://www.djangoproject.com/): Framework to build web apps more quickly with Python.
- [django-rest-framework](https://www.django-rest-framework.org/): Library to help building REST APIs with django.
- [django-filter](https://github.com/carltongibson/django-filter): Library to help creating filters from URL parameters.
- [drf-yasg](https://github.com/axnsan12/drf-yasg): Library to generate Swagger/OpenAPI 2.0 specifications from a Django Rest Framework API.
- [dj-database-url](https://github.com/jacobian/dj-database-url): Django utility that allows to utilize the 12factor inspired DATABASE_URL environment variable to configure Django applications.
- [prettyconf](https://github.com/osantana/prettyconf): Python library to make easy the separation of configuration and code following the recommendations of 12 Factor's topic about configs.
- [psycopg2](https://www.psycopg.org/): A PostgreSQL adapter for Python.
- [coverage](https://github.com/nedbat/coveragepy/tree/coverage-5.1): Library to measure code coverage, typically during test execution.



# Work at Olist

[Olist](https://olist.com/) is a company that offers an integration platform for sellers and marketplaces allowing them to sell their products across multiple channels.

The Olist development team consists of developers who love what they do. Our agile development processes and our search for the best development practices provide a great environment for professionals who like to create quality software in good company.

We are always looking for good programmers who love to improve their work. We give preference to small teams with qualified professionals over large teams with average professionals.

This repository contains a problem used to evaluate candidate skills. It's important to notice that satisfactorily solving the problem is just a part of what will be evaluated. We also consider other programming disciplines like documentation, testing, commit timeline, design and coding best practices.

Hints:

* Carefully read the specification to understand all the problem and artifact requirements before starting, if you don't understand something tell us;
* Check the recommendations and reference material at the end of this specification;
* We appreciate simplicity, so create a good project setup that will help us in your evaluation;
* Please make tests ... we appreciate tests <3... tests make the world better.

## How to participate

1. Make a fork of this repository on Github. If you can't create a public fork of this project, make a private repository (bitbucket/gitlab/github offers free private repos) and add read permission for one of these users below:
    * [tech-hiring on github](https://github.com/tech-hiring);
    * [tech-hiring on bitbucket](https://bitbucket.org/tech-hiring);
    * [tech-hiring on gitlab](https://gitlab.com/tech-hiring).
2. Follow the instructions of README.md (this file);
3. Deploy your project on a hosting service (we recommend [Heroku](https://heroku.com));
4. Apply for the position at our [career page](https://olist.gupy.io/) with:
    * Link to the fork on Github (or bitbucket/gitlab);
    * Link to the deployed project in a hosting service.

## Specification

You should implement an application for a library to store book and authors data.

**This application must provide an HTTP REST API to attend the requirements.**

### 1. Receive a CSV with authors and import to database

Given a CSV file with many authors (more than a million), you need to build a command to import the data into the database. The CSV file will have the following format:

```
name
Luciano Ramalho
Osvaldo Santana Neto
David Beazley
Chetan Giridhar
Brian K. Jones
J.K Rowling
```

Each author record in the database must have the following fields:

* id (self-generated)
* name

You need to store the authors' data to complement the book data that will be stored afterward (see item #3).

_Extra tip: If you use Django Framework you can do something like this..._

```
python manage.py import_authors authors.csv
```

### 2. Expose authors' data in an endpoint

This endpoint needs to return a paginated list with the authors' data. Optionally the authors can be searched by name.

### 3. CRUD (Create, Read, Update and Delete) of books

You need to implement these actions in your API:

* Create a book
* Read book's data
* Update book's data
* Delete book's data

Each book record has the fields:

* id (self-generated)
* name
* edition
* publication_year
* authors (more than one author can write a book)

To retrieve a book (in easy mode) we can filter by 4 fields (or a composition of these four):

* name
* publication_year
* edition
* author

But these 4 filters are optional. It must be possible to navigate all the books' data without any filter.

To create a book you need to send this payload (in json format) below:

```
{
 "name": // Name of the book;
 "edition": // Edition number;
 "publication_year": // Publication year of the book;
 "authors": // List of author ids, same ids of previous imported data
}
```

## Project Requirements:

* Provide a working environment with your project (eg. Heroku)
* Application must be written in Python or Go.
* Python
    * Use Python >= 3.5
    * Choose any Python web framework you want to solve the problem
    * Use PEP-8 for code style
    * [Python Coding Style](http://docs.python-guide.org/en/latest/writing/style/)
* Go
    * Go >= 1.10
    * [Effective Go](https://golang.org/doc/effective_go.html)
* Every text or code must be in English
* Write the project documentation containing:
    * Description;
    * Installing (setup) and testing instructions;
    * If you provide a [docker](https://www.docker.com/) solution for setup, ensure it works without docker too.
    * Brief description of the work environment used to run this project (Computer/operating system, text editor/IDE, libraries, etc).
* Provide API documentation (in English);
* Variables, code and strings must be all in English.

## Recommendations

* Write tests! Please make tests ... we appreciate tests <3... tests make the world better;
* Practice the [12 Factor-App](http://12factor.net) concepts;
* Use [SOLID](https://en.wikipedia.org/wiki/SOLID_(object-oriented_design)) design principles;
* Use programming good practices;
* Use [git best practices](https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/best-practices), with clear messages (written in English);
* Be aware when modeling the database;
* Be careful with REST API details. They can bite you!

**Have fun!**
