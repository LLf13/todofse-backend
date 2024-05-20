# todofse-backend
A backend for the Todo-App 

## How to use
- Download and install docker: https://www.docker.com/products/docker-desktop/
- Clone this repository
- Open the project in a text editor or IDE and open its terminal
- Make sure docker is running
- Run `docker-compose build` in the terminal to build the stack
- Run `docker-compose up` and the API is available under http://0.0.0.0:5001/ and can be accessed from the frontend
- Press `Ctrl + C` to stop

### General Information
- A MongoDB Admin-Panel is installed to make interacting with the Database easier 
  - Username: admin
  - Password: pass
- I didn't have time to make a proper API documentation, If you want to know how the API works take a look at the flask_api.py file

