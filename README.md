# Repo-1.04
**Team members**
* Carter Figgins
* Brock Francom
* Waseca Hodson
* Sterling Tolley

## Building and Starting Application
0. Run `git clone https://github.com/usu-cs-3450/Repo-1.04`
1. If desired, follow the unit testing instructions to test the system. 
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Create a Django admin user
   * Run `python manage.py createsuperuser`
   * Enter desired username and password and press enter. 
5. Run `python manage.py runserver 0.0.0.0:80`
6. After creating a Django admin start the server and register the user, which will become the auction admin, by going to <a href="/register">the registration page</a>, or by going to the <a ref="/login">login page</a> and clicking "Register Here". Once you have registered go to the <a href="/admin">Django Admin Portal</a>. Go to "Access" and then select the user you registered. Click the Admin Level checkbox so it is selected. That user is now an auction admin.</p>
7. Create aucitons and items as desired. 
8. Add photos to items.
9. Anyone should be able to access the auction by entering the ip address of the the machine hosting the auction. 

## Important Note of Prototype
All prototypes are high fidelity and cover most of the high priority feature in the system.

***This document needs to contain***
* An explanation of the organization and name scheme for the workspace
* Version-control procedures
* Tool stack description and setup procedure
* Build instructions
* Unit testing instructions
* System testing instructions
* Other development notes, as needed

***Explanation of our organization and name scheme of our workspace***  
The organization of our workspace will follow the organization necessary for a Django project.

The name scheme of our workspace will be the following:

newFileDemonstratingNameScheme.py

newVariableDemonstratingNameScheme = 0

***Version-control procedures***  
Version control will be implemented using git and GitHub. The workflow will be as follows:

* The master branch should always be a working version of the system. (For initial development, this might not always be the case.)
* Under no circumstances will a developer ever push changes directly to the master branch.
* No developer will approve thier own pull request.

1. Each developer will clone the repository into thier workspace. 
2. Make a new feature branch off of master to work on a feature/update.
3. Make needed changes to the feature branch.
4. Test changes.
5. Pull and rebase any new changes to master into the feature/update branch. Do this by checking out your branch, and running 'git pull --rebase origin master'
6. Fix any confilcts.
7. Test again. If behavior is not as expected, go back to step two. 
8. Once the branch has been tested, the developer will push thier branch to a remote feature branch on GitHub.
9. Submit a pull request from feature/fix branch to the master branch. A teammate should review the pull request on GitHub. 
10. Upon approval of the changes by someone other than the author of the pull request, the pull request will be approved and merged into master. 
11. The feature/update branch will be deleted. 

Documentation files  
The files used for documentation of the system will be created and maintained on Google Docs. The night before the Milestone is to be completed, a member of our group will download the most current fileand update the copy that is in our GitHub repo. 

***Tool stack description and setup procedure***  
The tool stack will be comprised of the following tools:
* Python 3.7.4
* Django 2.2.5

Setup Instructions:
Python 3.7.4 -- Follow the instructions on https://www.python.org/downloads/ to download and install Python 3.7.4, or update python to version 3.7.4 using your system's package manager. 
To make sure the install worked, run `python -V` and the output should be '3.7.4'

Django 2.2.5 -- Follow the instructions on https://docs.djangoproject.com/en/2.2/topics/install/
To make sure the install worked, run `python -m django --version` and the output should be '2.2.5'


***Unit testing instructions***
Unit tests should be ran when the project is first downloaded from github. Testing requires that the database is deleted prior to running the tests, and all data in the database will be lost. 

Instructions for testing:
1. Move into the directory containing the manage.py file, then run the following commands:
* rm db.sqlite3
* python manage.py makemigrations 
* python manage.py migrate
* python manage.py runserver
2. In a seperate terminal, run the following command:
* python manage.py test

All tests should pass. 

Once finished with testing, repeat step one above to prepare the system for hosting an auction.  

***System testing instructions***

***Other development notes, as needed***

