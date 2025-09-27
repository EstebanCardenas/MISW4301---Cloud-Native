APP_NAME=$1

POD_NAME=$(kubectl get pods | grep $APP_NAME | cut -d " " -f 1)
kubectl logs $POD_NAME --follow
