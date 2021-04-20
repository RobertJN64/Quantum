import QCircuitTools as qct

def circuitManager():
    cm = qct.CircuitManager(2, ["PreMeasure"])
    c = cm.circuit
    c.h(0)
    cm.measure(0, "PreMeasure")
    c.cx(0, 1)
    c.h(0)
    c.h(1)
    cm.measureAll()
    return cm