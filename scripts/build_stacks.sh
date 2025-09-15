source ./scripts/define_stacks.sh
source ./scripts/styles.sh

read -p "Enter the environment: " ENV

# Apply terraform changes for each stack
for STACK in "${STACKS[@]}"; do
    printf "${BOLD_CYAN}Building stack: $STACK${RESET}\n"
    make tfinit CURDIR=$(pwd) STACK=$STACK ENV=$ENV
    make tfplan CURDIR=$(pwd) STACK=$STACK ENV=$ENV
    make tfapply CURDIR=$(pwd) STACK=$STACK ENV=$ENV
done

printf "${BOLD_GREEN}All stacks built successfully!${RESET}\n"
printf "${BOLD_CYAN}Inputs:\n\tENV: $ENV${RESET}\n"
