#!/bin/bash

set -e

function ts {
  echo [`date '+%b %d %X'`]
}

#-----------------------------------------------------------------------------------------------------------------------

echo "$(ts) Starting the server."
/usr/bin/python /usr/sbin/xeoma-mqtt.py