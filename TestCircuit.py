import QCircuitTools as qct

def circuitManager():
    cm = qct.CircuitManager(2)
    c = cm.circuit
    c.h(0)
    c.cx(0, 1)
    cm.measureAll()
    return cm