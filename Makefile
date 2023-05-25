docker-restart:
	docker-compose down
	docker-compose up -d --build

setup: 
	docker exec newspaper-backend-app bash -c 'php artisan key:generate'
	docker exec newspaper-backend-app bash -c 'php artisan config:clear'
	docker exec newspaper-backend-app bash -c 'php artisan migrate:fresh --seed'
	docker exec newspaper-backend-app bash -c 'php artisan passport:install'
	docker exec newspaper-backend-app bash -c 'php artisan python:install-requirement'
	docker exec newspaper-backend-app bash -c 'php artisan python:run-get-data'