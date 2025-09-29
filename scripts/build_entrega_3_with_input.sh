source ./scripts/define_stacks.sh
source ./scripts/styles.sh
source ./scripts/define_inputs.sh

printf "${BOLD_BLUE} Starting build using these inputs: ${RESET}\n"
printf "\t${BOLD_MAGENTA}AWS_ACCOUNT_ID:${RESET} $AWS_ACCOUNT_ID\n"
printf "\t${BOLD_MAGENTA}APP_VERSION:${RESET} $APP_VERSION\n"
printf "\t${BOLD_MAGENTA}ENV:${RESET} $ENV\n"
printf "\t${BOLD_MAGENTA}AWS_ACCESS_KEY_ID:${RESET} $AWS_ACCESS_KEY_ID\n"
printf "\t${BOLD_MAGENTA}AWS_SECRET_ACCESS_KEY:${RESET} $AWS_SECRET_ACCESS_KEY\n"
printf "\t${BOLD_MAGENTA}AWS_SESSION_TOKEN:${RESET} $AWS_SESSION_TOKEN\n"

IMG_LIST=("users_app" "notifications_app" "credit_cards_app" "consumer")

# Apply terraform changes for each stack except consumer
for STACK in "${STACKS[@]}"; do
    if [ "$STACK" == "consumer" ]; then
        continue
    fi

    printf "${BOLD_CYAN}Building stack: $STACK${RESET}\n"
    make tfinit CURDIR=$(pwd) STACK=$STACK ENV=$ENV
    make tfplan CURDIR=$(pwd) STACK=$STACK ENV=$ENV
    make tfapply CURDIR=$(pwd) STACK=$STACK ENV=$ENV
done

printf "${BOLD_CYAN} Creating consumer ECR image... ${RESET}\n"
make dklogin ACCOUNT_ID=$AWS_ACCOUNT_ID
make dkbuild APP_NAME="consumer" APP_VERSION=$APP_VERSION DIR="consumer" ACCOUNT_ID=$AWS_ACCOUNT_ID
make dkpush APP_NAME="consumer" APP_VERSION=$APP_VERSION ACCOUNT_ID=$AWS_ACCOUNT_ID

printf "${BOLD_CYAN} Now creating the consumer stack... ${RESET}\n"
STACK="consumer"
make tfinit CURDIR=$(pwd) STACK=$STACK ENV=$ENV
make tfplan CURDIR=$(pwd) STACK=$STACK ENV=$ENV
make tfapply CURDIR=$(pwd) STACK=$STACK ENV=$ENV

printf "${BOLD_CYAN} Change the url of the DB and sqs url in the manifests if needed ${RESET}\n"
read -p "Press [Enter] to continue after making the changes..."

# Build and push Docker images for each app except consumer
for IMG_NAME in "${IMG_LIST[@]}"; do
    if [ "$IMG_NAME" == "consumer" ]; then
        continue
    fi

    printf "${BOLD_CYAN}Building and pushing image: $IMG_NAME${RESET}\n"
    if [ "$IMG_NAME" == "credit_cards_app" ]; then
        DIR="credit_cards"
    else
        DIR=$IMG_NAME
    fi

    make dkbuild APP_NAME=$IMG_NAME APP_VERSION=$APP_VERSION DIR=$DIR ACCOUNT_ID=$AWS_ACCOUNT_ID
    printf "${BOLD_CYAN}Pushing image: $IMG_NAME${RESET}\n"
    make dkpush APP_NAME=$IMG_NAME APP_VERSION=$APP_VERSION ACCOUNT_ID=$AWS_ACCOUNT_ID
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
make eksapply-entrega-3 CURDIR=$(pwd)
