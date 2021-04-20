import QCircuitTools as qct
from matplotlib import pyplot
from qiskit.providers.aer import AerSimulator
#import math

def run():
    cmA = qct.CircuitManager(2, measures=['PreMeasure'], qMeasures=["Qubit A", "Qubit B"])

    circuit = cmA.circuit

    circuit.h(0)
    cmA.measure(0,'PreMeasure')
    cmA.measureAll(barrier=True)

    cmA.simulate(AerSimulator(), 1000)

    # Draw the circuit
    circuit.draw(output='mpl')
    pyplot.get_current_fig_manager().set_window_title('Circuit A')
    cmA.printEntanglementTable()
    cmA.printEntanglements()
    pyplot.show(block=False)
