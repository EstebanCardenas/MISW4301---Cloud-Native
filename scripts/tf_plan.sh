STACK=$1
if [[ -z "$STACK" ]]; then
    echo "No stack defined"
    exit 1
fi
ENV=$2
if [[ -z "$ENV" ]]; then
    echo "No environment defined"
    exit 1
fi

terraform -chdir=$(pwd)/terraform/stacks/$STACK plan -var-file=$(pwd)/terraform/envs/$ENV/$STACK/terraform.tfvars -out=.tfplan
