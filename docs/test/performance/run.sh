#!/bin/bash
current_datetime=$(date +%Y%m%d%H%M%S)
mkdir -p "${current_datetime}"
# touch "${current_datetime}/output.jtl"  # 无需先手动创建
mkdir -p "${current_datetime}/results"
jmeter -n -t 202409.jmx -l "${current_datetime}/output.jtl" -e -o "${current_datetime}/results"