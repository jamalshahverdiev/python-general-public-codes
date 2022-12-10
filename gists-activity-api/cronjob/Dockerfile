FROM python:3.8-alpine
WORKDIR /app
COPY ["requirements.txt", "check_users_activity.py", "separated_func_file.py", "./"]
RUN pip install -r requirements.txt 
#&& chown -R nobody:nobody /app/*
#RUN apk add --update --no-cache libcap && \
#    setcap cap_setgid=ep /bin/busybox
#USER nobody
RUN mkdir /tmp/crontabs \
    && echo 'SHELL=/bin/sh' > /tmp/crontabs/root && echo '* * * * * /app/check_users_activity.py >> /tmp/cron.log 2>&1'  >> /tmp/crontabs/root 
CMD ["crond", "-c", "/tmp/crontabs", "-l", "8", "-d", "0", "-f"] 
