# Los pasos en este archivo pueden ser usados para su pipeline de Unit testing
# en el caso que usted decida usar Python.

.PHONY: lintfix lintcheck unittest

lintfix:
	poetry --directory=${DIR} install
	poetry --directory=${DIR} run black .
	poetry --directory=${DIR} run isort . --profile black
	poetry --directory=${DIR} run bandit -c pyproject.toml -r .
	poetry --directory=${DIR} run ruff check --fix

lintcheck:
	poetry --directory=${DIR} install
	poetry --directory=${DIR} run black --check .
	poetry --directory=${DIR} run isort --check . --profile black
	poetry --directory=${DIR} run bandit -c pyproject.toml -r .
	poetry --directory=${DIR} run ruff check

unittest:
	poetry --directory=${DIR} install
	poetry --directory=${DIR} run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing

# login to AWS ECR
dklogin:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com

# build and tag docker image
dkbuild:
	docker build --rm --platform linux/amd64 -t ${APP_NAME}:${APP_VERSION} --target runner --label version=${APP_VERSION} -f ${DIR}/Dockerfile ${DIR} --provenance=false --no-cache
	docker tag ${APP_NAME}:${APP_VERSION} ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/${APP_NAME}:${APP_VERSION}

# push docker image to AWS ECR
dkpush:
	docker push ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/${APP_NAME}:${APP_VERSION}

# load docker image to minikube
mkbuild: dkbuild
	minikube image load ${DIR}:latest

# delete all resources in default namespace
mkdelete:
	kubectl delete all --all -n default

# terraform initialize
tfinit:
	terraform -chdir="${CURDIR}/terraform/stacks/${STACK}" init -backend-config="${CURDIR}/terraform/envs/${ENV}/${STACK}/backend.tfvars"

# terraform plan and create a plan file
tfplan:
	terraform -chdir="${CURDIR}/terraform/stacks/${STACK}" plan -var-file="${CURDIR}/terraform/envs/${ENV}/${STACK}/terraform.tfvars" -out=.tfplan

# apply the created plan file
tfapply:
	terraform -chdir="${CURDIR}/terraform/stacks/${STACK}" apply .tfplan

# terraform destroy all resources
tfdestroy:
	terraform -chdir="${CURDIR}/terraform/stacks/${STACK}" destroy -var-file="${CURDIR}/terraform/envs/${ENV}/${STACK}/terraform.tfvars"

# configure kubectl to use the EKS cluster
eksconfig:
	aws sts get-caller-identity
	aws eks update-kubeconfig --region us-east-1 --name ${CLUSTER_NAME}

# install nginx ingress controller on EKS
eksingress:
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
	helm repo update
	helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=LoadBalancer

# delete nginx ingress controller from EKS
eksdeleteingress:
	kubectl -n ingress-nginx delete svc ingress-nginx-controller
	helm uninstall ingress-nginx -n ingress-nginx
	kubectl delete ns ingress-nginx

# watch for the external url of the ingress controller
eksingressurl:
	kubectl get svc -n ingress-nginx ingress-nginx-controller -w 

# apply k8s manifests to the EKS cluster
eksapply:
# 	envsubst < "${CURDIR}/k8s/producer_deployment.yml" | kubectl apply -f -
#	envsubst < "${CURDIR}/k8s/publisher_deployment.yml" | kubectl apply -f -
	kubectl apply -f ${CURDIR}/k8s

# delete all k8s resources from the EKS cluster
eksdestroy:
	kubectl delete -f ${CURDIR}/k8s
# 	envsubst < "${CURDIR}/k8s/producer_deployment.yml" | kubectl delete -f -
# 	envsubst < "${CURDIR}/k8s/publisher_deployment.yml" | kubectl delete -f -
