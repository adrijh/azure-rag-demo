cd ${source}
az acr login --name ${registry_name}
docker build --platform linux/amd64 -t ${registry_name}.azurecr.io/${image_name}:${image_tag} .
docker push ${registry_name}.azurecr.io/${image_name}:${image_tag}
