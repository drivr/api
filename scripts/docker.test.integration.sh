DOCKER_CONTAINER_ID=$(sh ./scripts/docker.db.testing.sh)
echo "Created docker container for integration tests: $DOCKER_CONTAINER_ID"

# Wait a little for postgres connection.
sleep 2s

# Run the integration tests.
poetry run behave

echo "Removing container for integration tests: $DOCKER_CONTAINER_ID"
REMOVE_OUT=$(docker container rm $DOCKER_CONTAINER_ID -f)