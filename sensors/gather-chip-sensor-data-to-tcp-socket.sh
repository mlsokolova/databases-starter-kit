#!/bin/bash
#send data of sensors to TCP socket
chip=$1
port=$2
host=$3
interval=$4
echo "The sctipt is gathering sensor data  of $chip chip of this computer and sending it to the port $port on the host $host each $interval seconds"
echo "Press [CTRL+C] to stop.."
while :
do
	sensors $chip -j|jq --arg ts `date +"%s"` --arg hostname `hostname` '. + {ts: $ts, hostname: $hostname}'|jq -c| nc $host $port
	sleep $interval
done
