#!/bin/bash

rc=0

for file in test/sql/*
do
  name="${file/test\/sql\//}"
  name="${name/.sql/}"
  result=${file/\/sql\//\/results\/}
  result="test/results/${name}.out"
  expected="test/expected/${name}.out"
  ./pgspot --plpgsql $file > $result
  if diff -u $expected $result; then
    status="OK"
  else
    status="FAIL"
    rc=1
  fi
  echo "${name}: ${status}"
done

exit $rc
