import QCircuitTools as qct
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere
import matplotlib.pyplot as pyplot
import numpy as np

cm = qct.CircuitManager(4)
c = cm.circuit

#init
c.initialize([1/np.sqrt(2), -1/np.sqrt(2)], 3)
c.h(0)
c.h(1)

#oracle
c.cx(0,2)
c.cx(1,2)
c.mct([2],3)
c.cx(0,2)
c.cx(1,2)
c.barrier()

#diffuser
c.h(0)
c.h(1)
c.x(0)
c.x(1)
c.barrier(0)
c.h(1)
c.mct([0],1)
c.h(1)
c.barrier(0)
c.x(0)
c.x(1)
c.h(0)
c.h(1)

c.draw(output="mpl")
pyplot.show()

state = Statevector.from_instruction(cm.circuit)
plot_state_qsphere(state)
pyplot.show()


