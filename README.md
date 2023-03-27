# head_pose_validation


## Requirements
### MongoDB on port 27017
#### MongoDB
```bash
docker run --name mongodb -d -p 27017:27017 -v $(pwd)/data:/data/db mongodb/mongodb-community-server:$MONGODB_VERSION
```
### Redis on port 6379
#### Redis
```bash
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```
### RabbitMQ on port 5672
#### RabbitMQ
```bash
docker run -d --hostname my-rabbit --name rabbitmq-local -p 5672:5672 -p 15672:15627 rabbitmq:3-management
```


### Installation
##### Preferably create venv and install the requirements
```bash
python3 -m venv venv
source venv/bin/activate
```

##### Run the following command to install the required packages
```bash
    pip3 install -r requirements.txt
```
##### Create .env file and add the following variables
```bash
    MONGO_URI=mongodb://localhost:27017
    MONGO_DB=photo_moderator
    BROKER_URI=amqp://guest:guest@localhost:5672//
    BACKEND_URI=redis://localhost:6379/0
    APPLICATION_API_KEY="application_api_key"
    APPLICATION_API_KEY_ADMIN="application_admin_key"
```


### Usage for development
```bash
cd service
uvicorn main:app --port 8000 --reload 
celery -A celery_task_app.worker worker -l info
```

### Usage for production
```bash
cd service
gunicorn -b 127.0.0.1:7007 -w 4  -k uvicorn.workers.UvicornWorker main:app
celery -A celery_task_app.worker worker
```


### Create systemd service for celery
```bash
sudo nano /etc/systemd/system/celery_photo_moderator.service
```
```bash
#Example of a systemd service file for celery
[Unit]
Description=Face duplicate detection with external backend
After=syslog.target network.target

[Service]
User=www-data
Group=www-data

WorkingDirectory=/srv/path
PrivateTmp=true
#EnvironmentFile=/srv/path/env

ExecStart=/srv/path/venv/bin/celery -A celery_task_app.worker worker -l info
ExecReload=/bin/kill -HUP ${MAINPID}
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target

```
```bash
sudo systemctl daemon-reload
sudo systemctl enable celery_photo_moderator.service
sudo systemctl start celery_photo_moderator.service
```

### Create systemd service for gunicorn
```bash
sudo nano /etc/systemd/system/gunicorn_photo_moderator.service
```
```bash
#Example of a systemd service file for gunicorn 
[Unit]
Description=Face duplicate detection with external backend
After=syslog.target network.target

[Service]
User=www-data
Group=www-data

WorkingDirectory=/srv/path
PrivateTmp=true
#EnvironmentFile=/srv/path/env

ExecStart=/srv/path/venv/bin/gunicorn -b 127.0.0.1:7007 -w 7 --max-requests 60 --max-requests-jitter 10  -k uvicorn.workers.UvicornWorker main:app
ExecReload=/bin/kill -HUP ${MAINPID}
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target
    
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn_photo_moderator.service
sudo systemctl start gunicorn_photo_moderator.service
```

