nohup ./bokeh_run_websocket.sh > bokeh.log 2>bokeh.err &
screen -dmS bokeh ./bokeh_run_websocket.sh > bokeh.log

screen -dmS bokeh bokeh serve bokeh --allow-websocket-origin=quantcypher.com --allow-websocket-origin=quantcypher.com
