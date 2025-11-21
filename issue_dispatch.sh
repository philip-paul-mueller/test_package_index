#!/bin/bash

REPO="test_package_index"
OWNER="philip-paul-mueller"

SOURCE_REPO="dace"
SOURCE_ORG="gridtools"
DEPENDENCY_REF="gt4py-next-integration"

if [ ! -e ".token" ]
then
	echo "The file with the token, '.token' does not exist."
	echo " According to 'https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-a-repository-dispatch-event'"
	echo " a fine grained token with '\"Contents\" repository permissions (write)' is needed."
	exit 1
fi

curl -L -v \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $(cat .token)" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/${OWNER}/${REPO}/dispatches \
  -d '{"event_type":"update_package_index","client_payload":{"source_repo":"'"${SOURCE_REPO}"'","source_org":"'"${SOURCE_ORG}"'","dependency_ref":"'"${DEPENDENCY_REF}"'"}}'
