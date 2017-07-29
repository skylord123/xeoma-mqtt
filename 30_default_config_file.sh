#!/bin/bash

set -e

DEFAULT_CONFIG_FILE=/files/config.ini.default
CONFIG_FILE=/config/config.ini
FIXED_CONFIG_FILE=/tmp/config.ini

#-----------------------------------------------------------------------------------------------------------------------

function ts {
  echo [`date '+%b %d %X'`]
}

#-----------------------------------------------------------------------------------------------------------------------

echo "$(ts) Processing config file"

# Create default config file if necessary
if [ ! -f "$CONFIG_FILE" ]
then
  echo "$(ts) Creating config file $CONFIG_FILE. Please set the password and rerun this container."
  cp "$DEFAULT_CONFIG_FILE" "$CONFIG_FILE"
  chmod a+w "$CONFIG_FILE"
  exit 1
fi

# Deal with \r caused by editing in windows
tr -d '\r' < "$CONFIG_FILE" > "$FIXED_CONFIG_FILE"

exit 0
