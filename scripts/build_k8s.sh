source ./scripts/styles.sh

read -p "Enter the cluster's name: " CLUSTER_NAME

printf "${BOLD_CYAN}Configuring EKS cluster${RESET}\n"
make eksconfig CLUSTER_NAME=$CLUSTER_NAME

printf "${BOLD_CYAN}Installing Ingress${RESET}\n"
make eksingress

printf "${BOLD_CYAN}Applying K8s manifests${RESET}\n"
make eksapply CURDIR=$(pwd)

printf "${BOLD_GREEN}K8s manifests applied successfully!${RESET}\n"
printf "${BOLD_CYAN}Inputs:\n\tCLUSTER_NAME: $CLUSTER_NAME${RESET}\n"
