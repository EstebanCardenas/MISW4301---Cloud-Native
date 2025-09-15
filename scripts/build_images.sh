source ./scripts/define_images.sh
source ./scripts/styles.sh

read -p "Enter AWS Account ID: " ACCOUNT_ID
read -p "Enter the app version: " APP_VERSION

make dklogin ACCOUNT_ID=$ACCOUNT_ID
for IMG_NAME in "${IMG_LIST[@]}"; do
    printf "${BOLD_CYAN}Building and pushing image: $IMG_NAME${RESET}\n"
    make dkbuild APP_NAME=$IMG_NAME APP_VERSION=$APP_VERSION DIR=$IMG_NAME ACCOUNT_ID=$ACCOUNT_ID
    printf "${BOLD_CYAN}Pushing image: $IMG_NAME${RESET}\n"
    make dkpush APP_NAME=$IMG_NAME APP_VERSION=$APP_VERSION ACCOUNT_ID=$ACCOUNT_ID
done

printf "${BOLD_GREEN}All images built and pushed successfully!${RESET}\n"
printf "${BOLD_CYAN}Inputs:\n\tACCOUNT_ID: $ACCOUNT_ID\n\tAPP_VERSION: $APP_VERSION${RESET}\n"
