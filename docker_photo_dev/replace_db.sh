#!/bin/bash
cd "$(dirname "$0")"

rm ../photo_project/db.sqlite3
rm ../photo_project/photo_app/migrations/0*
rm -r ../photo_project/photo_app/media/images/

docker exec -it \django_photo_dev python manage.py makemigrations photo_app
docker exec -it \django_photo_dev python manage.py migrate
#docker exec -it \django_photo_dev python manage.py loaddata photo_app/fixtures/f1.json
chown $USER:$USER ../photo_project/db.sqlite3

docker exec -it \django_photo_dev python manage.py loaddata f1.json