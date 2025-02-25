# MLBTracker

A web application designed to track and display MLB Players and Statistics. Built with Python, Django, SQLite, Bootstrap, and jQuery.

## About This Project:
This is my first project using Django. Throughout development, I've leveraged Django's powerful features to create a structured and scalable application. While new to Django, I applied my prior experience with web development frameworks like Flask to quickly get up to speed with Django's best practices. The project demonstrates my ability to learn and adapt to new technologies, and I look forward to refining my Django skills through further projects.

## Features:
 - Player Information
 - Player Statistics

## Setup/Installation
Your tool-chain is up to you, but for this application it is recommended you use a python virtual environment. </br>

Clone the repository at ```git@github.com:kjeverson/MLBTracker.git```

To create the virtual environment run the following commands:
```bash
cd ~/$path_to/MLBTracker
python3 -m venv venv
source venv/bin/activate
## To leave the virtual environment simply run 'deactivate'
```

You are now in a python virtual environment. The need to install the required packages:

```bash
pip install -r requirements.txt
```

Lastly, you will need to initialize the database. The expected Database Initialization Process is as follows:

Make a database migration:
```bash
python manage.py makemigrations
```

Migrate the database:
```bash
python manage.py migrate
```

Get MLB team data:
```bash
python manage.py get_teams
```

Load player data (this expects a Path to the data file, use the one provided in ```MLBTracker/data/players.json``` or provide a new one. 
```bash
python manage.py run_etl ~/$path_to/MLBTracker/MLBTracker/data/players.json
```

After this you are now ready to run the MLB Tracker Application!

### Running the Application
First run the following on the command line:
```bash
python manage.py runserver
```

Open your browser, navigate to:
```bash
http://localhost:8000/
```

