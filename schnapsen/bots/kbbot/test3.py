import sys

import kb
from kb import KB, Boolean, Constant, Integer

# Define our integer symbols
x = Integer('x')
y = Integer('y')

q = x == y
a = x + y > 2
b = x + y < 5
c = x + y < -2
d = x + y > -5

kb = KB()

kb.add_clause(q)
kb.add_clause(a, c)
kb.add_clause(a, d)
kb.add_clause(b, c)
kb.add_clause(b, d)

for model in kb.models():
    print model

print kb.satisfiable()
