# tiktokjam24

Repo for team RCH4CKERS

# INIT

1. Install and run Docker Desktop in the background
2. Enter and run `docker compose airflow-init` (for first time users)
3. Run `docker compose up`
4. Go to `http://localhost:8080` and enter airflow for user and pw
5. Find ml_pipeline in the list of dags
6. Press the run button (top right)
7. Press graph and select node to see logs
8. To stop press `Ctrl + C` and run `docker compose down`

# Backend

<<<<<<< HEAD
1. Run `pip install fastapi supabase apache-airflow-client`
2. Obtain supabase credentials via the connect button
3. Add to local .env file in backend folder under SUPABASE_URL and SUPABASE_KEY
4. Run `cd backend` and run the fastapi backend with `fastapi dev main.py`
5. `Ctrl + C` to stop
=======
1. Obtain supabase credentials
2. add credentials to local .env file in backend folder
3. run the fastapi backend with `fastapi dev main.py `
4. On the top righ, there is an authorise button. This is to inform the fastapi who is the current user.
5. This function uses Supabase Auth, and when you use this for the first time to you have to first navigate to the register_supabase function and register using a *valid email* address and password
6. Navigate to the sign in email sent to the email address and click on the link. Nothing wrongs if redirected to link not file
7. Proceed to the sign_in function and place your own credentials. Upon executing an access token will be generated.
8. Save the access token somewhere
9. You can now insert the access token in the top right authorise button and can use the restricted functions


# Errors

1. If rateLimited error hit in the console, it means that too many users have tried to register to supabase, and thus need to give it about an hour to reset
>>>>>>> main
