STACK=$1
if [[ -z "$STACK" ]]; then
    echo "No stack defined"
    exit 1
fi

terraform -chdir=$(pwd)/terraform/stacks/$STACK apply .tfplan
