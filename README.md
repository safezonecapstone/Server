# Setup

After cloning the repo, in the folder execute these commands:

- Be sure to have `virtualenv` installed for python
   
```
virtualenv venv

source venv/bin/activate

pip install -r requirements.txt
```

## Setting Environment Variables

Set Flask Enviroment Variables in `.flaskenv`

- Example: FLASK_ENV=development

Set Credentials in `.env`

- Example: DB_USER=user

## Connecting to Google Cloud SQL

- Download and install [Google Cloud SDK](https://cloud.google.com/sdk/docs/downloads-interactive)

  - Once installation is completed you must run `gcloud init` in your terminal and login with the google account associated with the Google Cloud Platform. Allows for easy authentication when running the cloud_sql_proxy

  - For the Cloud Project select **united-triode-233023**

  - For the Google Compute Engine zone select **us-east1-d**

- Download or compile [Cloud SQL Proxy](https://cloud.google.com/sql/docs/mysql/connect-external-app#proxy)

## Running Server

- Run the cloud_sql_proxy executable
  - Linux/Mac
    ```
    ./cloud_sql_proxy -instances=united-triode-233023:us-east1:database=tcp:5234
    ```
  - Windows
    ```
    cloud_sql_proxy.exe -instances=united-triode-233023:us-east1:database=tcp:5234
    ```

- If the port is in use change the port in the above command to anything else and in the `__init__.py` of the **server** folder change the port value in this snippet:

  ```
    sqlalchemy.engine.url.URL(
        drivername='postgres',
        username = db_user,
        password = db_pass,
        database = db_name,
        host='127.0.0.1',
        port='5234'
    ),
  ```

* You can then run the server locally by issuing the command

  ```
  python main.py
  ```
## Documentation

  - Description of all routes and the way they are used can be found at __127.0.0.1:5000/api/ui__