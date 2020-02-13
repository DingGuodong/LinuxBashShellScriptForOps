#!/usr/bin/env bash
# restart java service by pid

pid=$1
app_user="ebt"
app_subpath="scripts/post_deploy.sh"

if [[ "pid$pid" == "pid" ]]; then
  echo "pid is missing"
  exit 1
fi

function show_current_running() {
  current_running=$(su - ${app_user} -c "jps -l" | grep "^${pid}")
  retvar="$?"
  if [[ $retvar != 0 ]]; then
    echo "java pid is not found"
    exit 1
  fi
  current_service=$(echo "$current_running" | awk '{print $2}')
  echo "$current_running"

}

function show_service_health() {
  pgrep -f "$current_service" >&/dev/null
  retvar="$?"
  if [[ $retvar != 0 ]]; then
    return $retvar
  else
    return $retvar
  fi
}

function do_sleep() {
  local seconds=$1
  local msg=$2
  [ "$seconds" -lt 1 ] && return
  echo "sleep $seconds for $msg"
  sleep 1
  do_sleep $((seconds - 1)) "${msg}"
}

function keep_waiting_until_service_up() {
  used_seconds=0
  max_try_times=10
  sleep_seconds=3
  while [[ $max_try_times -gt 0 ]]; do
    show_service_health
    retvar="$?"
    if [[ $retvar != 0 ]]; then
      echo "waiting $sleep_seconds seconds for service startup"
      sleep $sleep_seconds
      max_try_times=$((max_try_times - 1))
      used_seconds=$((used_seconds + sleep_seconds))
    else
      echo "service startup in $used_seconds seconds"
      return $retvar
    fi
  done
}

show_current_running

app_path=$(lsof -p "${pid}" | awk '$4=="cwd"{print $NF}')
restart_script_path="${app_path}/${app_subpath}"
echo "$restart_script_path"
# why cd? because: JAVA_ARGS in $restart_script_path: -cp 'classes/:lib/*'
# e.g.: exec /application/jdk/bin/java -server -Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Djava.io.tmpdir=/tmp -Djava.net.preferIPv6Addresses=false -Dlog.path=/opt/ebt/logs/dataexchange -Xmx1g -Xms1g -XX:SurvivorRatio=8 -XX:+HeapDumpOnOutOfMemoryError -XX:ReservedCodeCacheSize=128m -XX:InitialCodeCacheSize=128m -XX:+DisableExplicitGC -XX:+PrintGCDetails -XX:+PrintHeapAtGC -XX:+PrintTenuringDistribution -XX:+UseConcMarkSweepGC -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -XX:CMSInitiatingOccupancyFraction=80 -Xloggc:/opt/ebt/logs/dataexchange/dataexchange.gc.log -XX:ErrorFile=/opt/ebt/logs/dataexchange/dataexchange.vmerr.log -XX:HeapDumpPath=/opt/ebt/logs/dataexchange/dataexchange.heaperr.log -cp 'classes/:lib/*' com.ebt.platform.dataexchange.Application
su - ${app_user} -c "cd $app_path && bash $restart_script_path"

keep_waiting_until_service_up
