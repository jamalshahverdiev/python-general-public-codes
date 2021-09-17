#!/usr/bin/env bash

socket='10.100.100.100:8000'
# curl -XGET 'http://${socket}/metrics'

for count in `seq 100`; do
    for endpoint in "query_params" "get_lang?language=python" "view/${count}" "buy/${count}" "database" "/"; do
        if [[ 'query_params' == *"${endpoint}"* ]]; then
            for name in ali vali pirvali haqverdi allahverdi qulamali; do
                curl -XGET "http://${socket}/${endpoint}?name=${name}&surname=${name}yev&age=${count}"
            done
        elif [[ '/' == *"${endpoint}"* ]]; then
            curl -XGET "http://${socket}${endpoint}"
        else
            for i in `seq ${count}`; do sleep 1; python3 client.py; done
            curl -XGET "http://${socket}/${endpoint}"            
        fi
    done
done

