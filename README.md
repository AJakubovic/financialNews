# Django REST Financial news
 This is Django based REST api service for financial news. Service has two parts: *REST api service* and *scraping service*. REST api is primarily used for fetching data and scraping service collects and stores data from Yahoo finance site. 
 
 ## Initialization and setting up the project
  Prerequisites for starting services in Docker containers are:
  * install Docker Desktop
  * install WSL2 linux kernel update package
  * navigate to folder *...\financialNews\Scripts* in command window and start *activate*
  * navigate to folder *...\financialNews\src* and type ```make build```
  * type ```make compose-manage-py cmd="makemigrations"``` for creating migrations
  * type ```make compose-start``` for starting all services

 The initial page Api Root (http://localhost:8000/) contains paths for three REST apis: feeds, feedNews and symbols. All objects are empty and cannot be created without a successful logIn, what is not possible unless there is created SuperUser. To create a SuperUser, please type in cmd the following command:
 ```
 make compose-manage-py cmd=“createsuperuser“
 ```, 
and fill-in the data for username, email and password.
Then it is possible to enter the initial data in objects Symbols, Feeds and Periodic task (through Admin module). Financial news will be then collected and listed in FeedNews api.
