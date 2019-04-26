#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
db=${script_dir}/user_profile.db

sqlite3 ${db} .schema > ${script_dir}/schema.sql.bak
sqlite3 ${db} .dump > ${script_dir}/dump.sql.bak