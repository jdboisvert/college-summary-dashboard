# College Summary Dashboard
A simple web application that shows you the latest stats for a given school (such as [Dawson College](https://www.dawsoncollege.qc.ca/)). This can also scrap the websites in the background every 12 hours.

![Animated gif demoing the web app dashboard.](demo.gif)

### Getting started

```shell
# install pyenv (if necessary)
brew install pyenv pyenv-virtualenv
echo """
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init --b)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
""" > ~/.zshrc
source ~/.zshrc

# create a virtualenv
pyenv install 3.11.1
pyenv virtualenv 3.11.1 college_summary_dashboard
pyenv activate college_summary_dashboard

# install dependencies
pip install -U pip
pip install -r requirements.txt -r requirements-dev.txt
```

### Pre-commit

A number of pre-commit hooks are set up to ensure all commits meet basic code quality standards.

If one of the hooks changes a file, you will need to `git add` that file and re-run `git commit` before being able to continue.

To Install:
    pre-commit install


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

## Quick Start 
These steps are to quickly set up the application and get it running.

1. The quickest and easier way to get started is to set up a database on MonggoDB Atlas and set the `MONGO_URI` in the `.env` file to the connection string. You can also set up a local instance of MongoDB and set the `MONGO_URI` to `mongodb://localhost:27017/college_dashboard_db`.

2. Run the command `flask scrape` to scrape the website and populate the database.

3. Run the command `flask run` to start the application.

4. Navigate to `http://localhost:5000/` to see the dashboard in action.


## Custom Commands

### Running Dawson College Scrapper Manually
```
flask scrape
```

## Contributing

### Initialize pre-commit
`pre-commit` is used to format commits according to our coding standards. Initializing it here will install hook scripts into your local git repo.
```
pre-commit install
```

### Testing

[pytest](https://docs.pytest.org/en/6.2.x/) is used for testing.

    # just the unit tests against your current python version
    pytest

    # just the unit tests with a matching prefix
    pytest -k test_some_function
