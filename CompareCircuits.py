import QCircuitTools as qct
from matplotlib import pyplot
from qiskit.providers.aer import AerSimulator
#import math

def run():
    cmA = qct.CircuitManager(2, measures=['PreMeasure'], qMeasures=["Qubit A", "Qubit B"])

    circuit = cmA.circuit

    circuit.h(0)
    cmA.measure(0, 'PreMeasure')
    circuit.cx(0,1)
    circuit.h(0)
    circuit.h(1)
    cmA.measureAll(barrier=True)

    cmA.simulate(AerSimulator(), 1000)

    # Draw the circuit
    circuit.draw(output='mpl')
    pyplot.get_current_fig_manager().set_window_title('Circuit A')
    cmA.printEntanglementTable()
    cmA.printEntanglements()
    pyplot.show(block=False)

    print('\n\n++++++++\n')

    cmB = qct.CircuitManager(2, measures=['PreMeasure'], qMeasures=["Qubit A", "Qubit B"])

    circuit = cmB.circuit

    circuit.h(0)
    #cmB.measure(0, 'PreMeasure')
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.h(1)
    cmB.measureAll(barrier=True)

    cmB.simulate(AerSimulator(), 1000)

    # Draw the circuit
    circuit.draw(output='mpl')
    pyplot.get_current_fig_manager().set_window_title('Circuit B')
    cmB.printEntanglementTable()
    cmB.printEntanglements()
    pyplot.show(block=False)

    print('\n\n++++++++\n')

    cmC = qct.CircuitManager(2, measures=['PreMeasure'], qMeasures=["Qubit A", "Qubit B"])

    circuit = cmC.circuit

    circuit.h(0)
    cmC.measure(0, 'PreMeasure')
    circuit.cx(0, 1)
    cmC.measureAll(barrier=True)

    cmC.simulate(AerSimulator(), 1000)

    # Draw the circuit
    circuit.draw(output='mpl')
    pyplot.get_current_fig_manager().set_window_title('Circuit C')
    cmC.printEntanglementTable()
    cmC.printEntanglements()
    pyplot.show(block=True)


