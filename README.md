## DRF + Vue application for managing equipment
<br/>

Uses *Django Rest Framework 3.16.0*, *MySQL 8.4.5*, *Vue 3.5.13*

Prepared to deploy with docker-compose

Full backend requirements are listed in [requirements.txt](/backend/app/requirements.txt)

Full frontend requirements are listed in [package-lock.json](/frontend/equipment-frontend/package-lock.json)

DB is prepopulated with test data by initial migration

Task description for the API: [task_description.docx](/task_description.docx)

<br/><br/>

### To use locally run following steps:

Build containers: `docker-compose up --build -d`

Check containers are up and running: `docker ps -a` (might be about 10 sec delay to be fully operational after containers "started" because of healthchecks)

Open in browser: `http://localhost/`

API docs: `http://localhost/api/docs/`

Shutdown: `docker-compose down -v`
