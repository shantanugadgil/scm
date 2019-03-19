#!/bin/bash

set -u
set -e

declare -r module="file"

action="$1"

file_create()
{
	echo $@

	local destination="$1"
	local is_dir=${2:-"0"}

	#HACK: allow "group" to be specified separately
	local owner=${3:-"root:root"}
	local mode=${4:-"0644"}

	local encoded=${5:-""}
	local content=$(echo -n $encoded | base64 -d)

	# for future ...
	local source=${6:-""}
	local checksum=${7:-""}

	if [[ "$is_dir" == "1" ]]; then
		mkdir -p "${destination}"
		chown ${owner} "$destination"
		chmod ${mode} "$destination"
		return 0
	fi

	# check if content is defined
	if [[ "$content" != "" ]]; then
		cat > "${destination}" <<EOF
$content
EOF

		chown ${owner} "$destination"
		chmod ${mode} "$destination"

		return 0
	fi

	if [[ "$source" == "" ]]; then
		echo "you must define either one of 'content' or 'source'"
		return 1
	fi

	# only support curl for now
	curl -sS "${source}" > "${destination}"
	chown ${owner} "$destination"
	chmod ${mode} "$destination"

	return 0
}

file_delete()
{
	echo $@
	
	local destination="$1"
	local recursive=${2:-"0"}

	if [[ "$recursive" == "1" ]]; then
		rm -rf "${destination}"
		return $?
	fi

	rm -f "${destination}"
	return $?

	return 0
}

file_rename()
{
	echo $@
	
	local old_name="$1"
	local new_name=${2}

	mv -fv "${old_name}" "${new_name}"
	return $?

	return 0
}

### module begins here

case "$action" in
	"create"|"delete"|"rename")
		echo "$@"
		shift 1
		${module}_${action} "$@"
	;;

	*)
		echo "unsupported action [$action]"
		exit 1
	;;
esac
