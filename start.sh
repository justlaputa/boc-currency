#!/bin/bash

cd /home/laputa/workspace/boc-currency
source .pyvenv/bin/activate
echo 'python version: '
python --version
cd spider
python start.py
