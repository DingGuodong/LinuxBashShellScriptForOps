#!/bin/bash
set -x

ENVIRONMENT="$1"
CURRENT_APP_ROOT="$APP_ROOT/$APP_NAME"
POST_DEPLOY_SCRIPT="$CURRENT_APP_ROOT/scripts/post_deploy.sh"

DEPLOY_HOSTS_CONF_FILE="scripts/""$ENVIRONMENT""_deploy_host.conf"


function do_deploy() {
  local DEST_HOST_IP
  local DEST_HOST_PORT
  local DEST_HOST_USER
  DEST_HOST_IP=$(echo "$1" | awk -F":" '{print $1}')
  DEST_HOST_PORT=$(echo "$1" | awk -F":" '{print $2}')
  DEST_HOST_USER=$(echo "$1" | awk -F":" '{print $3}')

  if [[ "$DEST_HOST_USER" == "" ]]; then
    DEST_HOST_USER=$APP_USER
  fi

  ssh -p "$DEST_HOST_PORT" "$DEST_HOST_USER@$DEST_HOST_IP" "mkdir -p $APP_ROOT/$APP_NAME"
  rsync -e "ssh -p $DEST_HOST_PORT" -r --del . "$DEST_HOST_USER@$DEST_HOST_IP:$APP_ROOT/$APP_NAME"
  ssh -p "$DEST_HOST_PORT" "$DEST_HOST_USER@$DEST_HOST_IP" "
        cd $CURRENT_APP_ROOT && \
        chmod +x $POST_DEPLOY_SCRIPT \
        && $POST_DEPLOY_SCRIPT \
    "
}

function deploy() {
  # shellcheck disable=SC2013
  for DEPLOY_HOSTS_SSH_ARGUMENTS in $(cat "$DEPLOY_HOSTS_CONF_FILE"); do
    echo "deploying $DEPLOY_HOSTS_SSH_ARGUMENTS"

    # deploy project
    do_deploy "$DEPLOY_HOSTS_SSH_ARGUMENTS"

    httpstatus=1
    # check project status
    if [ "$HEALTHY_CHECK_OFF" == "true" ]; then
      do_sleep 10 "waiting service to startup"
      continue
    fi

    set +e
    check_healthy 0
    httpstatus=$?
    set -e
    if [ $httpstatus == 0 ]; then
      continue
    else
      echo "fail to deploy $DEPLOY_HOSTS_SSH_ARGUMENTS"
      return $httpstatus
    fi
  done
}

function do_sleep() {
  SECOND=$1
  REASON=$2
  [ "$SECOND" -lt 1 ] && return
  echo "Sleeping $SECOND for $REASON"
  sleep 1
  do_sleep $((SECOND - 1)) "${REASON}"
}

function check_healthy() {
  retrytime=$1
  retrytime=$((1 + retrytime))
  status_code=000
  RETRY_SLEEP_TIMES=6
  RETRY_SLEEP_SECOND=10
  echo "================ HEALTHY_CHECK_URL : $HEALTHY_CHECK_URL ========================="
  if [ "$HEALTHY_CHECK_URL" == "" ]; then
    status_code=$(curl -I -m 10 -o /dev/null -s -w "%{http_code}" "http://127.0.0.1:8091/healthy_check")
  else
    status_code=$(curl -I -m 10 -o /dev/null -s -w "%{http_code}" "${HEALTHY_CHECK_URL/hostip/$DEST_HOST_IP}")
  fi
  if [ "$status_code" == 200 ]; then
    echo "connection is ok!!!"
    return 0
  else
    if [ $retrytime -le $RETRY_SLEEP_TIMES ]; then
      do_sleep $RETRY_SLEEP_SECOND "waiting to do next healthy check"
      check_healthy $retrytime
    else
      echo "disconnected after $RETRY_SLEEP_TIMES retry..."
      return 1
    fi
  fi
}

set -e
echo '----deploy begin # from deploy.sh ----'
deploy
echo '----deploy end # from deploy.sh ----'
