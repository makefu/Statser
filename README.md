# Statser
Statser gathers basic stats from the operating system with the help of psutil
and python.
Focus is portability and therefore the ability to have a usable stats generator
working under windows and linux. primarily windows as currently there is
nothing usable under windows which generates stats and writes them to for
example graphite.

# Graphite Support
Primary target is the ability to write stats to a graphite node, still it
should not be too hard to append more possible targets, even though these are
not in scope.

# Develop
virtualenv .
. bin/activate
pip -r deps.lst
