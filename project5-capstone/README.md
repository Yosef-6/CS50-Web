# CS50 WEB PROGRAMMING WITH PYTHON AND JAVASCRIPT PROJECT CAPSTONE NEWSARCHIVER
## Main idea
I've created a web app that's both a data aggregator and news station, that lets users get the news(breaking,sports,tech etc..) from different sources and navigate through dates to see an article form that date.  More on this [How it works](#how-it-works)

## Distinctiveness and Complexity

This project is distinctive from the other projects covered in the portions of the course. Additionally, besides demonstrating the skills acquired through learning the course, the project has a potential to be monetized due to its high practicality and applicability.

This project has been implemented as follows:
> Frontend technologies: html5, CSS3, bootsrap5 ,JavaScript.
>Backend technologies: python Django framework.

### Detailed implementation

 - Easy to use UI design with simple calendar and ability to download aggregated content.
 - Responsive and fluid design suitable for various screen sizes  
 - Dynamic website
 - Python-Django framework with 2 models i.e., Configuration , Articles
 - Uses sessions to figure out if logged in user is using web app for the first time and opens config modal 
 - Request and APScheduler python modules used
 
 ### How it works
 After registering the user is provided with config menu which has options to configure what type of news the user wants to view/aggregate. After saving the backend queues users configs and runs (a daemon process) a job every hour(getting real time news) sending requests to news api using those configs .If the results returned are zero or or some error occurred the user config will be deactivated and no longer queued for  further requests and this will be notified to the frontend whenever the user logs in or is active and is required to reconfigure in order to start the aggregation. On the frontend we have simple calendar  that shows the registration date, todays date and filled dates the user can navigate thought any date(filled contents are from registration date any date before that will not have any content ) and view the content(as well as download the aggregated content)

# Files structure
I have removed any  .pyc and migration files for clarity and // for description
```
┣ 📦Capstone  
┃	 ┣ 📜asgi.py  
┃	 ┣ 📜settings.py  
┃	 ┣ 📜urls.py  
┃	 ┣ 📜wsgi.py  
┃	 ┗ 📜__init__.py
┣📦jobs  
┃	 ┣ 📜jobs.py // server side job that is run once every hour    
┃	 ┗ 📜updater.py // background scheduler configured to perform Interval-based execution of jobs.py
┣📦NewsArchive  
┃	 ┣ 📂static  
┃	 ┃ ┗ 📂NewsArchive  
┃	 ┃ ┃ ┣ 📜dashboard.JS // javascript used for updating dashbard.html 
┃	 ┃ ┃ ┗ 📜styles.css  
┃	 ┣ 📂templates  
┃	 ┃ ┗ 📂NewsArchive  
┃	 ┃ ┃ ┣ 📜dashboard.html  
┃	 ┃ ┃ ┣ 📜index.html  
┃	 ┃ ┃ ┣ 📜login.html  
┃	 ┃ ┃ ┗ 📜register.html  
┃	 ┣ 📜admin.py  
┃	 ┣ 📜apps.py  
┃	 ┣ 📜models.py //contains configuration and Articles 
┃	 ┣ 📜tests.py  
┃	 ┣ 📜urls.py  
┃	 ┣ 📜views.py  
┃	 ┗ 📜__init__.py
┣📜db.sqlite3
┣📜manage.py
┗📜requirements.txt


📜views.py  
inside the views.py
views.index            // renders the landing page
views.dashboard_view   // renders dashboar.html with context arguments about config info and session info
views.login_view       // login
views.logout_view      // logout
views.register_view    // register
views.config_save      //API Route//  checks wether witch endpoint is choosen and save users config or updates the existing one 
views.aggregate_info   //API Route// returns information regarding the config
views.month_info       //API Route// returns marker info about which dates have a filled content  
views.day_data         //API Route// returns requested days articles
views.month_data       //API Route// returns requested month articles
```
##
### How to run

 - Clone the repo
 -  Install project dependencies by running  `pip install -r requirements.txt`. Dependencies include Django, Requests and APScheduler
 - Make and apply migrations by running  `python manage.py makemigrations`  and  `python manage.py migrate`.
 -  Go to website address and register an account.
 - Configure the pop up modal
 - `optional-step` You can change the seconds in `updater.py` from the default 3600(1hr) to whatever u want to run job faster and get your articles sooner and also the same thing on `dashboard.js` regular polling is done every 20min to  update dashboard.html 


