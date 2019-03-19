#!/bin/bash

set -u
set -e

declare -r module="service"

action="$1"

service_start()
{
	local name="$1"

	service ${name} start
	return 0
}

service_stop()
{
	local name="$1"

	service ${name} stop || { echo "failure is ok"; }
	return 0
}

service_restart()
{
	local name="$1"

	service_stop ${name}
	service_start ${name}
	return 0
}

service_enable()
{
	local name="$1"

	service ${name} enable || { echo "failure is ok"; }
	return 0
}

service_disable()
{
	local name="$1"

	service ${name} disable || { echo "failure is ok"; }
	return 0
}
### module begins here

case "$action" in
	"start"|"stop"|"restart"|"enable"|"disable")
		echo "$@"
		shift 1
		${module}_${action} "$@"
	;;

	*)
		echo "unsupported action [$action]"
		exit 1
	;;
esac
