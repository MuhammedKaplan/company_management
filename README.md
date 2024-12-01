# Project Setup

This project uses environment variables for configuration and runs on Docker for easy setup. Follow the steps below to get started.

---

## 1. Environment Variables

You can just change email information on .env file.

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend  
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587  
EMAIL_USE_TLS=True  
EMAIL_HOST_USER=ex@email.com
EMAIL_HOST_PASSWORD=your_password
```

## 2. Running the Project with Docker

1.  **Build and Run Docker Containers**:
    ```bash
    docker-compose up --build -d
    ``` 
    
2.  **Migration**:
	```bash
	docker-compose run web python manage.py makemigrations
	docker-compose run web python manage.py migrate
	```
3. **Create Admin User**
	```bash
	docker-compose run web python manage.py createsuperuser
	```
## Login Urls
- Manager login page: [http://localhost:8000/manager/login](http://localhost:8000/manager/login)
- Employee login page: [http://localhost:8000/login](http://localhost:8000/login)

## Example Data
You can use the seed_data.sql file to add example data to the database. Password is 'cmpass12' for all users.
```bash
docker cp seed_data.sql company_management-db-1:/opt/seed_data.sql
docker exec -it company_management-db-1 psql -U postgres -d company_management_db -f /opt/seed_data.sql
```