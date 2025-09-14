source ./scripts/define_images.sh
source ./scripts/define_stacks.sh
source ./scripts/styles.sh

read -p "Enter the environment: " ENV

printf "${BOLD_CYAN}Deleting K8s manifests${RESET}\n"
make eksdestroy CURDIR=$(pwd)

printf "${BOLD_CYAN}Deleting Ingress${RESET}\n"
make eksdeleteingress

for STACK in "${STACKS[@]}"; do
    printf "${BOLD_CYAN}Destroying stack: $STACK${RESET}\n"
    make tfdestroy CURDIR=$(pwd) STACK=$STACK ENV=$ENV
done
