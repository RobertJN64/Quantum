import TestCircuit
import matplotlib.pyplot as pyplot

def run():
    cm = TestCircuit.circuitManager()

    if input("Run on IBM Q? ") == "y":
        cm.sendToIBM()
    else:
        cm.simulate()

    print(cm.counts)

    figa = pyplot.figure()
    plta = figa.add_subplot()
    cm.histogram(plt=plta)

    figb = pyplot.figure()
    pltb = figb.add_subplot()
    cm.circuit.draw(output="mpl", ax=pltb)


    print('\n+++++++\n')
    print(cm.printQubitStates())
    print('\n+++++++\n')
    print(cm.printTable())
    print('\n+++++++\n')
    print(cm.printTable(allStates=True))
    print('\n+++++++\n')
    print(cm.printEntanglementTable())
    cm.printEntanglements()
    print('\n+++++++\n')

    #pyplot.show()

