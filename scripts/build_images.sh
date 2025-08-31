source scripts/define_images.sh

echo "Enter tag:"
read TAG
echo "Using tag: $TAG"

for IMG_NAME in "${IMG_LIST[@]}"; do
    IMG_DIR=$(echo "$IMG_NAME" | sed 's/-/_/')
    docker build -t $IMG_NAME:$TAG -f $IMG_DIR/Dockerfile $IMG_DIR/.
done
