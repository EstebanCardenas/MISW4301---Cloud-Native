source ./scripts/define_images.sh

read -p "Enter the app version: " APP_VERSION

for IMG_NAME in "${IMG_LIST[@]}"; do
    minikube image rm $IMG_NAME:$APP_VERSION
    sleep 1
    echo "Removed $IMG_NAME:$APP_VERSION from minikube."
    docker image rm $IMG_NAME:$APP_VERSION
    sleep 1
    echo "Removed $IMG_NAME:$APP_VERSION from docker."
done
