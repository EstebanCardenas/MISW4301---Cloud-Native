source ./scripts/define_stacks.sh
source ./scripts/styles.sh

IMG_LIST=("users_app" "notifications_app" "credit_cards_app" "consumer")

read -p "Enter AWS Account ID: " ACCOUNT_ID
read -p "Enter the app version: " APP_VERSION
read -p "Enter the environment: " ENV
read -p "Enter the AWS_ACCESS_KEY_ID: " AWS_ACCESS_KEY_ID
read -p "Enter the AWS_SECRET_ACCESS_KEY: " AWS_SECRET_ACCESS_KEY
read -p "Enter the AWS_SESSION_TOKEN: " AWS_SESSION_TOKEN

# Apply terraform changes for each stack
for STACK in "${STACKS[@]}"; do
    printf "${BOLD_CYAN}Building stack: $STACK${RESET}\n"
    make tfinit CURDIR=$(pwd) STACK=$STACK ENV=$ENV
    make tfplan CURDIR=$(pwd) STACK=$STACK ENV=$ENV
    make tfapply CURDIR=$(pwd) STACK=$STACK ENV=$ENV
done

printf "${BOLD_CYAN} Change the url of the DB and sqs url in the manifests if needed ${RESET}\n"
read -p "Press [Enter] to continue after making the changes..."

# Build and push Docker images for each app
make dklogin ACCOUNT_ID=$ACCOUNT_ID
for IMG_NAME in "${IMG_LIST[@]}"; do
    printf "${BOLD_CYAN}Building and pushing image: $IMG_NAME${RESET}\n"
    make dkbuild APP_NAME=$IMG_NAME APP_VERSION=$APP_VERSION DIR=$IMG_NAME ACCOUNT_ID=$ACCOUNT_ID
    printf "${BOLD_CYAN}Pushing image: $IMG_NAME${RESET}\n"
    make dkpush APP_NAME=$IMG_NAME APP_VERSION=$APP_VERSION ACCOUNT_ID=$ACCOUNT_ID
done

# Configure EKS cluster
printf "${BOLD_CYAN}Configuring EKS cluster${RESET}\n"
make eksconfig CLUSTER_NAME=dann-cluster

# Create AWS secret in Kubernetes
printf "${BOLD_CYAN}Creating AWS credentials secret in Kubernetes${RESET}\n"
make create-aws-secret AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

printf "${BOLD_CYAN}Installing Ingress${RESET}\n"
make eksingress

printf "${BOLD_YELLOW}Waiting for Ingress to be ready...${RESET}\n"
sleep 10

printf "${BOLD_CYAN}Applying K8s manifests${RESET}\n"
make eksapply CURDIR=$(pwd)
