source ./scripts/define_stacks.sh
source ./scripts/styles.sh

read -p "Enter the environment: " ENV
read -p "Enter the stack: " STACK

# Apply terraform changes for each stack
make tfinit CURDIR=$(pwd) STACK=$STACK ENV=$ENV
make tfplan CURDIR=$(pwd) STACK=$STACK ENV=$ENV
make tfapply CURDIR=$(pwd) STACK=$STACK ENV=$ENV
