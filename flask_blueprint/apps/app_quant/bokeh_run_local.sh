#!/bin/sh
#set -x

bokeh serve bokeh #--allow-websocket-origin=www.quantbloq.com:8008 &

# nohup ./bokeh_run_local.sh > bokeh.log 2>bokeh.err &

# ps -ef | grep [b]okeh
