source ./scripts/define_images.sh
source ./scripts/define_stacks.sh
source ./scripts/styles.sh

read -p "Enter AWS Account ID: " ACCOUNT_ID
read -p "Enter the app version: " APP_VERSION
read -p "Enter the environment: " ENV
read -p "Enter the cluster's name: " CLUSTER_NAME

# Apply terraform changes for each stack
for STACK in "${STACKS[@]}"; do
    printf "${BOLD_CYAN}Building stack: $STACK${RESET}\n"
    make tfinit CURDIR=$(pwd) STACK=$STACK ENV=$ENV
    make tfplan CURDIR=$(pwd) STACK=$STACK ENV=$ENV
    make tfapply CURDIR=$(pwd) STACK=$STACK ENV=$ENV
done

# Build and push Docker images for each app
make dklogin ACCOUNT_ID=$ACCOUNT_ID
for IMG_NAME in "${IMG_LIST[@]}"; do
    printf "${BOLD_CYAN}Building and pushing image: $IMG_NAME${RESET}\n"
    make dkbuild APP_NAME=$IMG_NAME APP_VERSION=$APP_VERSION DIR=$IMG_NAME ACCOUNT_ID=$ACCOUNT_ID
    printf "${BOLD_CYAN}Pushing image: $IMG_NAME${RESET}\n"
    make dkpush APP_NAME=$IMG_NAME APP_VERSION=$APP_VERSION ACCOUNT_ID=$ACCOUNT_ID
done

# Apply K8s
printf "${BOLD_CYAN}Configuring EKS cluster${RESET}\n"
make eksconfig CLUSTER_NAME=$CLUSTER_NAME

printf "${BOLD_CYAN}Installing Ingress${RESET}\n"
make eksingress

printf "${BOLD_CYAN}Applying K8s manifests${RESET}\n"
make eksapply CURDIR=$(pwd)
