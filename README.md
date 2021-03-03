# solar-irradiance-predictor
An AWS EBS-deployed solar irradiance prediction tool that utilizes API calls to the National Solar Radiation Database to determine profitability of solar panel use.

## Technologies
- AWS Elastic Beanstalk
- Flask
- HTML/Jquery
- Javascript
- Mongodb

## Team Members

Anthony, Tom, Narasimha

## Architecture
Architecture: Flask web app framework
Front-End: HTML/CSS/JS/jQuery, Bootstrap
Back-End: Python
Database: MongoDB

## Usage/Installation
1. Ensure that the latest version of Python is installed on your machine.
2. Ensure that PIP is installed on your machine.
3. Clone this repository.
4. Open up a command prompt/terminal in the repository directory
5. SetUp the python enviroment by following the link (https://flask.palletsprojects.com/en/1.1.x/installation/)
6. Activate the enviroment after created
7. Ensure that the Flask package is installed on your machine. "pip install flask"
8. Ensure that the PyMongo driver is installed in the Scripts folder on your machine. "pip install pymongo"
9. Ensure that the dnspython package is installed on your machine. "pip install dnspython"
10. Move the static and templates folders and the app.py file into the virtual environment directory just created
11. Run "flask run" in the terminal while in the virtual environment
12. The server is running on default localhost:5000 or 127.0.0.1:5000
13. Open index.html in a browser of your choice by typing either of the following urls: localhost:5000, localhost:5000/index