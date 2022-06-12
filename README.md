# backend-chats

## Run the docker container locally 

~~~
docker build -t backend-chats .
port=8000; docker run -e PORT=$port -p $port:$port backend-chats
~~~
