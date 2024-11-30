
##Database for testing
```
docker run --name company_management_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=company_management_db -p 5432:5432 -d postgres
```

##Redis for testing
```
docker run --name redis -p 6379:6379 -d redis
```
