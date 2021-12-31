# College Summary Dashboard
A simple web application that shows you the latest stats for a given school (such as [Dawson College](https://www.dawsoncollege.qc.ca/)).

## Getting started

### Set up a Python Virtual Environment

#### Create
```
python3 -m venv <path to venv>
```

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

### Run application
```
flask run
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
