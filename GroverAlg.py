import matplotlib.pyplot as pyplot
import numpy as np
import QCircuitTools as qct
from qiskit.circuit import QuantumCircuit

class GroverCircuit:
    def __init__(self, qubits, bonus_q = 0, measures=None, qmeasures=None):
        self.cm = qct.CircuitManager(qubits + bonus_q, measures, qmeasures, override_cbits=qubits)
        self.circuit = self.cm.circuit
        self.qubits = qubits

    def initHGates(self):
        for i in range(0, self.qubits):
            self.circuit.h(i)

    def draw(self):
        self.circuit.draw(output="mpl")
        pyplot.show()

def diffuser(qubits):
    circuit = QuantumCircuit(qubits)
    for i in range(0, qubits):
        circuit.h(i)
    for i in range(0, qubits):
        circuit.x(i)
    circuit.h(qubits-1)
    circuit.mct(list(range(qubits-1)),qubits-1)
    circuit.h(qubits-1)
    for i in range(0, qubits):
        circuit.x(i)
    for i in range(0, qubits):
        circuit.h(i)
    Dif_Gate = circuit.to_gate()
    Dif_Gate.name = "Diffuser"
    return Dif_Gate



def sudokuOracle():
    circuit = QuantumCircuit(8)
    circuit.cx(0, 4)
    circuit.cx(1, 4)
    circuit.cx(0, 5)
    circuit.cx(2, 5)
    circuit.cx(1, 6)
    circuit.cx(3, 6)
    circuit.cx(2, 7)
    circuit.cx(3, 7)
    Oracle = circuit.to_gate()
    Oracle.name = "Oracle"
    return Oracle


def measureInRange(cm, minv, maxv):
    for i in range(minv, maxv):
        cm.measure(i)


def run():
    #create circuitmanager for handling grover's alg
    c = GroverCircuit(4, bonus_q=5)
    c.initHGates() #add h-gates to top 4 lines
    c.circuit.initialize([1/np.sqrt(2), -1/np.sqrt(2)], 8)

    #construct oracle
    c.circuit.barrier()
    c.circuit.append(sudokuOracle(), [0,1,2,3,4,5,6,7])
    c.circuit.mct([4,5,6,7],8)
    c.circuit.append(sudokuOracle(), [0, 1, 2, 3, 4, 5, 6, 7])


    #add grover
    c.circuit.append(diffuser(4), [0,1,2,3])

    #do it again
    # construct oracle
    c.circuit.barrier()
    c.circuit.append(sudokuOracle(), [0, 1, 2, 3, 4, 5, 6, 7])
    c.circuit.mct([4, 5, 6, 7], 8)
    c.circuit.append(sudokuOracle(), [0, 1, 2, 3, 4, 5, 6, 7])

    #add grover
    c.circuit.append(diffuser(4), [0,1,2,3])

    c.circuit.barrier()
    measureInRange(c.cm, 0, 4)
    c.cm.simulate()
    print(c.cm.counts)
    print('\n')
    c.cm.printTable()
    print('\n')
    c.cm.printQubitStates()
    print('\n')
    c.cm.printEntanglementTable()
    c.cm.printEntanglements()
    print(c.circuit.draw())
    c.draw()

def run_tester():
    c = GroverCircuit(4, bonus_q=5, measures=['a', 'b', 'c', 'd', 'e'])
    c.initHGates()
    c.circuit.initialize([1 / np.sqrt(2), -1 / np.sqrt(2)], 8)
    c.circuit.barrier()
    for i in range(0, 2):
        c.circuit.append(sudokuOracle(), [0, 1, 2, 3, 4, 5, 6, 7])
        c.circuit.mct([4, 5, 6, 7], 8)
        c.circuit.append(sudokuOracle(), [0, 1, 2, 3, 4, 5, 6, 7])
        c.circuit.append(diffuser(4), [0,1,2,3])

    c.cm.measureAll()
    c.cm.simulate()
    print(c.cm.counts)
    print('\n')
    c.cm.printTable()
    print('\n')
    c.cm.printQubitStates()
    print('\n')
    c.cm.printEntanglementTable()
    c.cm.printEntanglements()
    print(c.circuit.draw())
    c.draw()
