echo "Input server's url"
read SERVERURL
CONTAINER_NAME=tagize_container
APP_NAME=tagize

#developing environment
#pipreqs . --encoding=utf-8 --force

mkdir .streamlit
cp $HOME/.streamlit/secrets.toml .streamlit

docker --host tcp://$SERVERURL:2375 stop $CONTAINER_NAME
docker --host tcp://$SERVERURL:2375 rm $CONTAINER_NAME
docker --host tcp://$SERVERURL:2375 image rm $APP_NAME
docker --host tcp://$SERVERURL:2375 buildx build --tag $APP_NAME .
docker --host tcp://$SERVERURL:2375 run --detach --publish 8045:8045 --restart always --name $CONTAINER_NAME $APP_NAME 

rm -rf .streamlit