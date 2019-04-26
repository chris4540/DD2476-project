#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
db=${script_dir}/user_profile.db

rm ${db}
sqlite3 ${db} < ${script_dir}/schema.sql
sqlite3 ${db} < ${script_dir}/data.sql