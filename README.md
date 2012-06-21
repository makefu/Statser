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
## General Development
    virtualenv .
    . bin/activate
    pip install -r deps.lst

## Windows Caveats
Statser currently only depends on `psutil`, if pip fails for you for one reason or another (e.g. requiring vc compiler),
consider installing `psutil` by hand from [http://code.google.com/p/psutil/] and set your PATH to c:\\PythonXX\;

# Testing
  python -m unittest discover test

# Run as Windows Service
Open Admin command shell

    cd $HERE/statser
    copy statser.json c:\
    python service.py --startup auto install
    python service.py start
