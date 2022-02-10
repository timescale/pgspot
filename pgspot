#!/usr/bin/python

from visitors import visit_sql
from state import GlobalState
import sys

state = GlobalState()

if len(sys.argv) > 1:
  data = "\n".join([open(f).read() for f in sys.argv[1:]])
else:
  data = sys.stdin.read()

visit_sql(state, data)
print(state)

if not state.is_clean():
  sys.exit(1)

