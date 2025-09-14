echo "Enter port:"
read PORT
if [[ -z "$PORT" ]]; then
    echo "Port is required"
    exit 1
fi

echo "Enter host for required services:"
read HOST
if [[ -z "$HOST" ]]; then
    echo "Host is required"
    exit 1
fi

echo "Enter app version:"
read APP_VERSION

SERVER_URL=0.0.0.0 SERVER_PORT=$PORT USERS_HOST=$HOST ROUTES_HOST=$HOST POSTS_HOST=$HOST go run main.go
docker run -e SERVER_URL=0.0.0.0 -e SERVER_PORT=$PORT -e USERS_HOST=$HOST -e ROUTES_HOST=$HOST -e POSTS_HOST=$HOST rf003:$APP_VERSION
