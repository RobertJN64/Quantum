import QCircuitTools as qct
#from math import pi

def circuitManager():
    cm = qct.CircuitManager(0)
    c = cm.circuit
    c.h(0)
    cm.measureAll()
    return cm