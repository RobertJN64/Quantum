import QCircuitTools as qct
from matplotlib import pyplot
from qiskit.providers.aer import AerSimulator
#import math

def run():
    circuitManager = qct.CircuitManager(2, measures=['PreMeasure'], qMeasures=["Qubit A", "Qubit B"])

    circuit = circuitManager.circuit

    circuit.h(0)
    circuitManager.measure(0, 'PreMeasure')
    circuit.cx(0,1)
    circuit.h(0)
    circuit.h(1)
    circuitManager.measureAll(barrier=True)

    circuitManager.simulate(AerSimulator(), 1000)

    # Draw the circuit
    circuit.draw(output='mpl')
    pyplot.get_current_fig_manager().set_window_title('Circuit')
    circuitManager.printEntanglementTable()
    circuitManager.printEntanglements()
    pyplot.show(block=True)

