#!/bin/bash
for NAME in $(ls test | egrep ^test.*\.py$)
do
  python -m test.$NAME > results/$NAME.out
done
