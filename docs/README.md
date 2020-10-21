# <img src="images/junglebook-logotype.png" alt="JungleBook" width="380"/>

</br>

API for managing your plants.

JungleBook web client app: https://github.com/EmilTheSadCat/JungleBook-web-client

You can easily check status of your plants. See if they need water.

## Tech Stack

-   Python 3.8
-   Flask
-   SQLAlchemy (PostgreSQL)
-   AWS S3 Python SDK

## Project setup

#### Installation

You should have PostgreSQL and Python 3.8 installed in your system.

Create virtual environment with Python 3.8 installed preferably in directory named `.venv`.

```shell
source .venv/bin/activate
pip install -r requirements.txt

python manage.py create_all_tables   # create tables in database

python -m run flask

```

#### Database migrations

```shell
python manage.py db migrate # run database migrations
python manage.py db upgrade # run database upgrade ( accept migration database changes )

python manage.py create_all_tables   # create tables in database
python manage.py drop_all_tables   # drop tables in database

```

#### Environmental variables

In root folder create `.env` file.

```
export APP_SETTINGS=<CONFIG_PROPERTY_FROM_CONFIG.PY>
export DATABASE_URL=<POSTGRESQL_DB_URL>
export GOOGLE_CLIENT_SECRET=<GOOGLE_CLIENT_SECRET>
export GOOGLE_CLIENT_ID=<GOOGLE_CLIENT_ID>
export REDIRECT_URI=<GOOGLE_AUTH_REDIRECT_URI>   // for Development localhost port 5000
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

```

## Links

-   API host address: https://junglebook-api.herokuapp.com/api

</br>

-   Repository: https://github.com/EmilTheSadCat/JungleBook-api

-   Web Client Repository: https://github.com/EmilTheSadCat/JungleBook-web-client

## Licensing

The code in this project is licensed under MIT license.
