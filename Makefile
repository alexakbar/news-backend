docker-restart:
	docker-compose down
	docker-compose up -d --build

setup: 
	docker-compose up -d --build
	docker exec newspaper-backend-app bash -c 'composer install'
	docker exec newspaper-backend-app bash -c 'chown -R www-data:www-data /var/www/html'
	docker exec newspaper-backend-app bash -c 'chmod -R 755 /var/www/html/storage'
	docker exec newspaper-backend-app bash -c 'php artisan key:generate'
	docker exec newspaper-backend-app bash -c 'php artisan config:clear'
	docker exec newspaper-backend-app bash -c 'php artisan migrate:fresh --seed'
	docker exec newspaper-backend-app bash -c 'php artisan passport:install'
	docker exec newspaper-backend-app bash -c 'php artisan python:install-requirement'
	docker exec newspaper-backend-app bash -c 'php artisan python:run-get-data'
	