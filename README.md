# FeatureRequest
Simple CRUD with a decoupled backend (Flask) and frontend (knockout.js). Deployed with Docker, Nginx, Gunicorn.

## Deploy
### Tested on AWS EC2 ubuntu

Install Docker

`
apt-get install docker docker.io
`

Clone the application

`
git clone https://github.com/pjryan93/FeatureRequest.git
`

`
cd FeatureRequest
`

Next you need to create the Dockerfile for postgres

`
cd web 
`

`
python create_db.py
`

`
cd ..
`

Build and run the application

`
docker-compose build
`

`
docker-compose up
`

Now we need to initialize the database.  To do this you need to open a shell in the flask applicaitons container.

`
docker exec -it <featurerequest_container_id> /bin/bash
`

Now in the shell run

`
python manage.py db init
`

`
python manage.py db migrate
`

`
python manage.py db upgrade
`

Press ctrl-d to exit the shell. You should now be able to connect on port 80
