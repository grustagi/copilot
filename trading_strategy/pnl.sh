#!/usr/bin/env bash
set -exuo pipefail

q -d , -H -O "select sum(strategy) from $1"
q -d , -H -O "select Stock,Date,buy,sell from $1 where (buy <> 0 OR sell <> 0) AND year = 2023 AND month in (6,7)"
