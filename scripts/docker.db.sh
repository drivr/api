DB_USER=drivr
DB_PASS=drivr
DB_NAME=drivr
DB_CONTAINER=drivrdb

docker run \
    --name $DB_CONTAINER \
    -p 5432:5432 \
    -e POSTGRES_DB=$DB_NAME \
    -e POSTGRES_USER=$DB_USER \
    -e POSTGRES_PASSWORD=$DB_PASS \
    -d postgres:13
