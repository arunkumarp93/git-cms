# README #

GitHub-Pages Blog Content Management

### What is this repository for? ###

* Quick summary
* Version

### How do I get set up? ###

* Summary of set up
  > **NOTE: Below steps are tested in UBUNTU machine. Follow the
  steps according to the development machine**

    1. create new virtual environment
       ```python3 -m venv venv```
    2. Install the requirements
       ```pip install -r requirements-dev.txt```
    3. Add pre-commit hooks to local repo
       ```pre-commit install --install-hooks```
       **More-info:** [pre-commit git URL](https://github.com/pre-commit/pre-commit-hooks)
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* PEP8 standard must be followed.
* Writing unitest is mandatory.
* All the pre-commit hooks must pass before committing.
* Adding package requirement:  
  ***Common requirement must be added to requirements-common.txt***
    * packages like flask, monogengine       
  
  ***Development requirements must be added to requirements-dev.txt***   
    * packages like flake8, pytest, black (auto code formatter)   
  
  ***Deployment package must be added to requirements-prod.txt***   
    * aws packages

### Who do I talk to? ###

* Repo owner or admin
