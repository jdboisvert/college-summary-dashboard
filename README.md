# College Summary Dashboard
A simple web application that shows you the latest stats for a given school (such as [Dawson College](https://www.dawsoncollege.qc.ca/)). This can also scrap the websites in the background every 12 hours.
You can view a live demo [here](https://college-summary-dashboard.herokuapp.com/)

## Getting started

### Set up a Python Virtual Environment

#### Create
```
python3 -m venv <path to venv>
```
Note that Python 3.7 was used to develop this application but 3.7 or later should be fine.

#### Activate
#### Windows
```
<path to venv>\Scripts\activate
```
#### Unix based (macOS and Linux)
```
source <path to venv>/bin/activate
```

### Install Dependencies
```
pip install -r requirements.txt
```


### Database
This application uses [MongoDB](https://www.mongodb.com/try/download/community) to store data. Ensure to have it installed locally or have an instance to connect to before starting.

#### Seeding
Seeding is not needed but if you wish to see the dashboard with initial data simply import `fixtures/college_metrics.json` into a database called `college_dashboard_db` with a collection called `college_metrics`.

### Set up Environment Variables

Simply copy `.env-example` to a file named `.env` and set the variables as needed such as `MONGO_URI`.

### Run application
```
flask run
```

## Custom Commands

### Running Dawson College Scrapper Manually
```
flask scrap
```

## Contributing

### Initialize pre-commit
`pre-commit` is used to format commits according to our coding standards. Initializing it here will install hook scripts into your local git repo.
```
pre-commit install
```

### Running Tests
`pytest` is used for conducting unit tests (should have been installed via the requirements.txt).
To run tests simply run the command:
```
pytest
```
