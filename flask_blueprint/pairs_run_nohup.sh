#!/bin/sh
#set -x

# nohup python pair.py > pair.log 2>pair.err &

nohup python run_pairs.py > pairs.log 2>pairs.err &

# ps -ef | grep [p]airs
