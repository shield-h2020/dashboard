#!/bin/bash

docker container exec -it -e COLUMNS=`tput cols` docker_dashboard-qa_1 bash -c \
"radish -t --tags smoke --early-exit \
features/system-settings.feature \
features/users.feature \
features/network-services.feature \
features/validations.feature \
features/security-policies.feature"

#!features/vnsf-notifications.feature \
