#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until curl -sSf "http://${host}:8080/health" >/dev/null; do
  >&2 echo "Waiting for ${host} to be ready..."
  sleep 5
done

>&2 echo "${host} is up - executing command"
exec $cmd
