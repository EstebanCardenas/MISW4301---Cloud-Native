source ./scripts/define_images.sh
source ./scripts/styles.sh

read -p "Enter the app version: " APP_VERSION

FULL_IMG_LIST=()

for IMG_NAME in "${IMG_LIST[@]}"; do
    printf "${BOLD_CYAN}Building and pushing image: $IMG_NAME${RESET}\n"
    docker build -t ${IMG_NAME}:${APP_VERSION} -f ${IMG_NAME}/Dockerfile ${IMG_NAME}
    sleep 1
    FULL_IMG_LIST+=("${IMG_NAME}:${APP_VERSION}")
done

printf "${BOLD_CYAN}Loading images to minikube: $IMG_NAME${RESET}\n"
minikube image load "${FULL_IMG_LIST[@]}"

printf "${BOLD_GREEN}All images built and loaded successfully!${RESET}\n"
