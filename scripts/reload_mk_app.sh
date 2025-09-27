APP_NAME=$1
DASH_APP_NAME=${APP_NAME/_/-}

kubectl delete -f k8s/$DASH_APP_NAME-deployment.yaml
sleep 1
minikube image rm $APP_NAME:3.0.0
sleep 1
docker image rm $APP_NAME:3.0.0
sleep 1
docker build -t $APP_NAME:3.0.0 -f $APP_NAME/Dockerfile $APP_NAME
sleep 1
minikube image load $APP_NAME:3.0.0
sleep 1
kubectl apply -f k8s/$DASH_APP_NAME-deployment.yaml
