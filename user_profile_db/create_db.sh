#!/bin/bash
sqlite3 user_profile.db < schema.sql
sqlite3 user_profile.db < data.sql