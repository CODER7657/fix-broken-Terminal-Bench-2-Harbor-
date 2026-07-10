#!/bin/bash

mkdir -p /logs/verifier

pytest /tests/test_outputs.py -rA --ctrf=/logs/verifier/ctrf.json
exit_code=$?

if [ $exit_code -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
