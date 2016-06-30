#!/bin/bash

PATH=/bin:/usr/bin:/usr/sbin
app_url=http://$OPENSHIFT_APP_DNS/

curl --insecure --location --silent --fail "$app_url" >/dev/null
