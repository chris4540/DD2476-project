#!/bin/bash
sqlite3 user_profile.db .schema > schema.sql.bak
sqlite3 user_profile.db .dump > dump.sql.bak

cat  dump.sql.bak