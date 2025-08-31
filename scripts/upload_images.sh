# Terraform config for registry stack must be applied before running this script.
source scripts/define_images.sh

echo "Enter tag:"
read TAG
echo "Using tag: $TAG"

echo "Enter ECR URI:"
read ECR_URI
echo "Using ECR URI: $ECR_URI"

for IMG_NAME in "${IMG_LIST[@]}"; do
    docker tag $IMG_NAME:$TAG $ECR_URI/$IMG_NAME:$TAG
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_URI
    docker push $ECR_URI/$IMG_NAME:$TAG
done
