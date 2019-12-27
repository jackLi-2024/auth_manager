/usr/local/python3/bin/uwsgi --stop server.pid

if [ $? -ne 0 ];
then
    echo "[ERROR] stop uwsgi server failed."
    exit -1
else
    echo "[INFO] stop uwsgi server ok."
fi

#cat celery.pid | xargs kill
#if [ $? -ne 0 ];
#then
#    echo "[ERROR] stop celery server failed."
#    exit -1
#else
#    echo "[INFO] stop celery server ok."
#fi

rm -rf server.pid
rm -rf nohup.out
rm -rf celery.pid