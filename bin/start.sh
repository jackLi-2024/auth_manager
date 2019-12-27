if [ ! -d log ];
then
    mkdir log
fi


# 1.0 start celery worker.
# nohup celery -A API.tasks worker --loglevel=info --logfile=./log/celery.log --pidfile=celery.pid &
#if [ $? -ne 0 ];
#then
#    echo "[ERROR] start celery worker failed."
#    exit -1
#else
#    echo "[INFO] start celery worker ok."
#fi

# 2.0 start web api
nohup /usr/local/python3/bin/uwsgi uwsgi.ini  &
if [ $? -ne 0 ];
then
    echo "[ERROR] start uwsgi server failed."
    exit -1
else
    echo "[INFO] start uwsgi server ok."
fi

echo "server is ready."
