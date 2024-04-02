#!/bin/bash

printenv | grep -v "no_proxy" >> /etc/environment

# cron -f &
# service cron start
/etc/init.d/cron start

tail -f /dev/null
