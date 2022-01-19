# Simple Python JSON Server

## Setup

1. Clone repo.
1. In project directory, run `pipenv shell`.
1. Then run `pipenv install`
1. Open the project in Visual Studio Code.
1. Create a `flagons.db` file in the project directory.
1. Create a SQL Tools connection to that database file.
1. Open `flagons.sql`, select all, and run. This will create the tables, and seed them with some sample data you can use.

## Running the Project

* To run the project without the debugger, run the following command in the terminal.
    ```sh
    watchgod request_handler.main
    ```
* To run the project in debug mode, open the `request_handler.py` module in Visual Studio Code, and start a Python debugger session.

## Issues

1. The client can't talk to the server. Every request produces an error in the Chrome dev tools labeled `ERR_CONNECTION_REFUSED`. Find out why the client requests can't phone home.
1. After you get the API able to listen for client requests, then next you will see is when making any request to the API, the following exception is being displayed in the Python output terminal. Look at the stack trace to find out which line of code is wrong and start your investigation from there.
    ```
    IndexError: list index out of range
    ```
1. The following exception keeps happening. Find out why it doesn't like the column name.
    ```sh
    OperationalError: no such column: ts.time_stamp
    ```
1. With the seed data, the Green Wyverns don't have any scores, but the JSON response from the API has one object in the `scores` array of that team.
1. The players array for each team is blank, when the database has three players assigned to every team.
1. Even though the teams have scores in the response from the API, the Leaderboard component in the client still shows a cumulative score of 0 for each team. Make sure the API is giving the client the exact data it needs.

## Deploying to Heroku

1. Create an account on [Heroku](https://heroku.com/), It's free.
1. At the dashboard, click the New button and select "Create a new app". Give the app whatever name you like.
1. [Install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
1. Login to Heroku with `heroku login`.
1. Add `Procfile` to project with the following content.
    ```
    web: python request_handler.py $PORT
    ```
1. Change end of request handler to the following code.
    ```py
    def main():
        host = ''
        port = int(os.environ['PORT'])
        HTTPServer((host, port), HandleRequests).serve_forever()


    main()
    ```
1. Remove `.db` from your `.gitignore` file.
1. `heroku git:remote -a kennel-server`
1. `git push heroku main` and wait for the deploy to complete.
1. Activate dyno with `heroku ps:scale web=1` and wait for confirmation that it started.
1. Open Postman and perform a GET to your deployed app's URL and a resource and you should get a response.

