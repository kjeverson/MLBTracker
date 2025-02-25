# MLBTracker

A web application designed to track and display MLB Players and Statistics. Built with Python, Django, SQLite, Bootstrap, and jQuery.

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

Lastly, you will need to initialize the database (I am not sure the one provided works and should probably be removed).

The expected Database Initialization Process is as follows:

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

