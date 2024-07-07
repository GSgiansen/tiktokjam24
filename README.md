# TikTok TechJam '24

Repo for team RCH4CKERS

# SimplifyML

This project aims to democratise access to Machine Learning (ML) by implementing an Automated Machine Learning (AutoML) pipeline which does eveything for the user from data processing to model training and testing. Users can then apply their model using other datasets. Additionally, this project also allows user to generate synthetic data using genAI.

Main features include:
- AutoML pipeline
    - Data preprocessing
    - Model training and testing
    - Evaluation
    - Prediction
- Synthetic Data generation

# Installation / Usage
1. Our project is hosted on http://143.198.216.162:3000/
2. To run it locally, read the installation for devs

# Project Structure

This project contains several key folders and files.

In `/backend`, you can find code pertaining to FastAPI and Supabase.
In `/dags`, you can find the AutoML and Data generation pipeline implemented using Apache Airflow DAGs.
In `/frontend`, you can find relevant components for the wbepage.
`Dockerfile` and `docker-compose.yml` contains the necessary information to build the docker image.


# Errors

1. If rateLimited error hit in the console, it means that too many users have tried to register to supabase, and thus need to give it about an hour to reset

# Installation for Devs

1. Install and run Docker Desktop in the background
2. Run `pip install "apache-airflow==2.9.2" apache-airflow-providers-google==10.1.0`
2. Add .env file with `AIRFLOW_UID=501`
2. Enter and run `docker compose up airflow-init` (for first time users)
3. Run `docker compose up`
4. Go to `http://localhost:8080` and enter airflow for user and pw
5. Find ml_pipeline in the list of dags
6. Press the run button (top right)
7. Press graph and select node to see logs
8. To stop press `Ctrl + C` and run `docker compose down`

1. Obtain supabase credentials
2. add credentials to local .env file in backend folder
3. run the fastapi backend with `fastapi dev main.py `
4. On the top righ, there is an authorise button. This is to inform the fastapi who is the current user.
5. This function uses Supabase Auth, and when you use this for the first time to you have to first navigate to the register_supabase function and register using a *valid email* address and password
6. Navigate to the sign in email sent to the email address and click on the link. Nothing wrongs if redirected to link not file
7. Proceed to the sign_in function and place your own credentials. Upon executing an access token will be generated.
8. Save the access token somewhere
9. You can now insert the access token in the top right authorise button and can use the restricted functions