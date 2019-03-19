#!/bin/bash

set -u

if (( $# < 1 )); then
	echo "invalid parameter count ($#)"
	echo "usage: $0 <server> [init]"
	exit 1
fi

server="$1"
bootstrap=${2:-"0"}

target_dir="/opt/config_manager"

export SSHPASS="foobarbaz"

if [[ "$bootstrap" != "0" ]]; then
	# ensure that rsync is installed on the remote machine
	sshpass -e ssh root@${server} "apt-get -qy update && apt-get -qy install rsync"
fi

# rsync the config "modules" the remote server
rsync --rsh="sshpass -e ssh" -Pa --delete payload/opt/config_manager/ root@${server}:${target_dir}/

# fixup perms
sshpass -e ssh root@${server} "chown -R root:root ${target_dir}/; find ${target_dir}/ -type d -exec chmod 0755 '{}' \\;; chmod 0755 ${target_dir}/bin/*.bash"
