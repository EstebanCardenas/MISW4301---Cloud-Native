source scripts/define_images.sh

echo "Enter tag:"
read TAG
echo "Using tag: $TAG"
echo "Enter AWS Account ID:"
read ACCOUNT_ID
echo "Using AWS Account ID: $ACCOUNT_ID"

for IMG_NAME in "${IMG_LIST[@]}"; do
    IMG_DIR=$(echo "$IMG_NAME" | sed 's/-/_/')
    #docker build -t $IMG_NAME:$TAG -f $IMG_DIR/Dockerfile $IMG_DIR/.
    make dkbuild APP_NAME=$IMG_NAME APP_VERSION=$TAG DIR=$IMG_DIR ACCOUNT_ID=$ACCOUNT_ID
done
