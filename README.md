# tiktokjam24

Repo for team RCH4CKERS

# INIT

1. Install and run Docker Desktop in the background
2. Enter and run docker compose airflow-init (for first time users)
3. Run docker compose up
4. Go to http://localhost:8080 and enter airflow for user and pw
5. Find ml_pipeline in the list of dags
6. Press the run button (top right)
7. Press graph and select node to see logs
8. To stop press Ctrl + C and run docker compose down


# Backend 

1. Obtain supabase credentials
2. add credentials to local .env file in backend folder
3. run the fastapi backend with `fastapi dev main.py`
