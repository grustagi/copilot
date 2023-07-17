#!/usr/bin/env bash
set -eo pipefail

#./auto.py

function pnlyear()
{
    nifty=$1
    echo "START:$nifty"
    q -d , -H -O "select sum(strategy) from $nifty"
    q -d , -H -O "select Stock,Date,buy,sell from $nifty where (buy <> 0 OR sell <> 0)"
    echo "END:$nifty"
}

pnlyear "nifty50.NS.csv"
pnlyear "nifty100.NS.csv"
pnlyear "nifty500.NS.csv"
pnlyear "niftysmallcap100.NS.csv"
pnlyear "niftymicrocap250.NS.csv"
