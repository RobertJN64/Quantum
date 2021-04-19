import QCircuitTools as qct
import matplotlib.pyplot as pyplot

def run():
    print("Creating Circuit...")
    cm = qct.CircuitManager(2)
    c = cm.circuit
    c.h(0)
    c.cx(0, 1)
    cm.measureAll(barrier=True)
    c.draw(output="mpl")
    pyplot.savefig("IBMQ_DEMO_IMG")

    cm.sendToIBM()

    cm.printTable(allStates=True)
    cm.printEntanglementTable(tol=0.1)
    cm.printEntanglements(tol = 0.1)