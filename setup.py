statser = Target(
    # used for the versioninfo resource
    description = "The Statser Windows Service",
    # what to build. For a service, the module name (not the
    # filename) must be specified!
    modules = ["statser"],
    cmdline_style='pywin32',
    )

setup(
    service = [statser],
    )

