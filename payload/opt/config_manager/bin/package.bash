#!/bin/bash

set -u
set -e

declare -r module="package"

action="$1"

package_install()
{
	local name="$1"

	export DEBIAN_FRONTEND=noninteractive
	apt-get install -y "${name}"
	return 0
}

package_remove()
{
	local name="$1"

	export DEBIAN_FRONTEND=noninteractive
	apt-get remove -y "${name}"

	return 0
}

### module begins here

case "$action" in
	"install"|"remove")
		apt-get update
		echo "$@"
		shift 1
		${module}_${action} "$@"
	;;

	*)
		echo "unsupported action [$action]"
		exit 1
	;;
esac
