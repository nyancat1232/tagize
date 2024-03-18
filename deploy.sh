echo "Input server's url"
read SERVERURL
echo "Input server's time zone"
read MYTIMEZONE
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
docker --host tcp://$SERVERURL:2375 run --detach --publish 8043:8043 --restart always --env TZ=$MYTIMEZONE --name $CONTAINER_NAME $APP_NAME 

rm -rf .streamlit