mode = input("Mode: ")

if mode == "e":
    import CircuitExperimenter
    CircuitExperimenter.run()

elif mode == "c":
    import ExpirementCombiner
    ExpirementCombiner.run()