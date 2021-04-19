from qiskit import QuantumCircuit, transpile, execute
from qiskit import IBMQ
from qiskit.providers.aer import AerSimulator as Aer
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as pyplot
import GraphingExtended as ge

import copy
import math

colors = ["red", "orange", "yellow", "green", "blue", "white", "black", "grey", "lightblue",
          ]

def possibleOutcomes(count):
    out = ['0', '1']
    for i in range(0, count-1):
        a = copy.deepcopy(out)
        for j in range(0, len(a)):
            a[j] = a[j] + '0'
        b = copy.deepcopy(out)
        for j in range(0, len(b)):
            b[j] = b[j] + '1'
        out = a + b
    return out

def expand(states):
    lout = possibleOutcomes(len(list(states.keys())[0]))
    out = {}
    for l in lout:
        out[l] = 0
    for state in states:
        out[state] = states[state]
    return out

def difference(states, xpos, ypos):
    total = 0
    count = 0
    for state in states:
        total += states[state]
        if state[xpos] == state[ypos]:
            count += states[state]
    return count/total

def countStates(counts, measures):
    qStates = []
    for i in range(0, len(measures)):
        qStates.append([0,0])
    for state in counts:
        for i in range(0, len(state)):
            s = state[::-1][i]
            if s == "0":
                qStates[i][0] += counts[state]
            elif s == "1":
                qStates[i][1] += counts[state]
            else:
                print("ERROR: state not 0 or 1")
    return qStates

class CircuitManager:
    def __init__(self, qubits, measures=None, qMeasures=None):
        self.qubits = qubits
        if measures is None:
            measures = []
        if qMeasures is None:
            qMeasures = [None] * qubits
        self.measures = []
        for i in range(0, qubits):
            if qMeasures[i] is None:
                self.measures.append("Qubit #" + str(i))
            else:
                self.measures.append(qMeasures[i])
        self.measures += measures
        self.circuit = QuantumCircuit(qubits, len(self.measures))
        self.isMeasured = [False] * len(self.measures)
        self.measureLine = [None] * len(self.measures)

        self.counts = {}
        self.provider = None

    def measure(self, line, measure=None):
        if measure is None:
            measure = self.measures[line]
        self.circuit.measure([line], [self.measures.index(measure)])
        if self.isMeasured[self.measures.index(measure)]:
            print("WARNING: Line already measured, continuing anyway.")
        self.isMeasured[self.measures.index(measure)] = True
        self.measureLine[self.measures.index(measure)] = line

    def measureAll(self, remeasure=False, barrier=False):
        if barrier:
            self.circuit.barrier()
        for i in range(0, self.qubits):
            if not self.isMeasured[i] or remeasure:
                self.measure(i)

    def simulate(self, simulator = Aer(), shots = 1000):
        compiled_circuit = transpile(self.circuit, simulator)
        job = simulator.run(compiled_circuit, shots=shots)
        result = job.result()
        self.counts = result.get_counts(self.circuit)
        return self.counts

    def histogram(self, plt=None):
        if plt is None:
            fig = pyplot.figure()
            plt = fig.add_subplot()
        plot_histogram(self.counts, ax=plt)
        return plt

    def getBackend(self):
        if self.provider is None:
            self.provider = IBMQ.load_account()

        return least_busy(self.provider.backends(filters=lambda x: x.configuration().n_qubits >= 5
                                                                   and not x.configuration().simulator
                                                                   and x.status().operational == True))

    def sendToIBM(self, backend=None, shots=1000):
        if backend is None:
            backend = self.getBackend()
        job = execute(self.circuit, backend, shots=shots)
        print("Job Queued")
        self.counts = job.result().get_counts()

    def printTable(self, allStates = False, colorize=False, states=None, min_tol = 0.05):
        if states is None:
            states = copy.deepcopy(self.counts)

        total = 0
        for num in states.values():
            total += num

        if allStates:
            states = expand(self.counts)
        else:
            delete = []
            for state in states:
                if states[state] / total < min_tol:
                    delete.append(state)

            for i in delete:
                states.pop(i)

        outstr = ""
        for measure in self.measures:
            outstr += "| " + measure + " "
        outstr += "|  %  "

        if colorize:
            outstr += "|   color   "

        outstr += '|\n'
        outstr += "-" * (len(outstr)-1) + '\n'

        counter = 0
        for state in states:
            count = states[state]
            revstate = state[::-1]
            for i in range(0, len(revstate)):
                val = revstate[i]
                length = len(self.measures[i])/2
                outstr += "|" + " " * math.ceil(length) + val + " " * math.floor(length + 1)
            percent = str(round(count*100/total))
            outstr += "|" + " " * (3 - len(percent)) + percent + "%" + " "

            if colorize:
                length = (11 - len(colors[counter]))/2
                outstr += "|" + " " * math.ceil(length) + colors[counter] + " " * math.floor(length)

            outstr += "|" + '\n'
            counter += 1

        print(outstr)

    def multiGraph3D(self, x, y, colored=True, min_tol = 0.05, block=True):
        fig = pyplot.figure()
        plt = fig.add_subplot(111, projection="3d")
        states = expand(self.counts)
        total = 0
        for num in states.values():
            total += num
        xpos = self.measures.index(x)
        ypos = self.measures.index(y)
        xout = []
        yout = []
        hout = []
        zout = []

        heights = [0,0,0,0]

        delete = []
        for state in states:
            if states[state] / total < min_tol:
                delete.append(state)

        for i in delete:
            states.pop(i)

        for state in states:
            x0 = state[::-1][xpos] == "0"
            y0 = state[::-1][ypos] == "0"
            count = round((states[state] / total) * 100)

            if x0:
                xout.append(0)
            else:
                xout.append(0.5)

            if y0:
                yout.append(0)
            else:
                yout.append(0.5)

            zout.append(count)

            if x0 and y0:
                hout.append(heights[0])
                heights[0] += count
            if x0 and not y0:
                hout.append(heights[1])
                heights[1] += count
            if not x0 and y0:
                hout.append(heights[2])
                heights[2] += count
            if not x0 and not y0:
                hout.append(heights[3])
                heights[3] += count

        if colored:
            color = colors[0:len(xout)]
        else:
            color = "blue"
        plt.bar3d(xout, yout, hout, 0.5, 0.5, zout, color=color)
        plt.set_xlabel(x)
        plt.set_ylabel(y)
        plt.set_zlabel("%")
        pyplot.xticks([0, 1])
        pyplot.yticks([0, 1])
        if colored:
            self.printTable(colorize=True, states=states, min_tol=min_tol)
        pyplot.get_current_fig_manager().set_window_title('Graph')
        pyplot.show(block=block)

    def multiGraph2D(self, x, y, min_tol = 0.05, block=True):
        fig = pyplot.figure(figsize=(4,4))
        plt = fig.add_subplot(111)

        states = copy.deepcopy(self.counts)

        total = 0
        for num in states.values():
            total += num

        delete = []
        for state in states:
            if states[state] / total < min_tol:
                delete.append(state)

        for i in delete:
            states.pop(i)

        xpos = self.measures.index(x)
        ypos = self.measures.index(y)
        xout = [0,0,1,1]
        yout = [0,1,0,1]
        size = [0,0,0,0]



        for state in states:
            x0 = state[::-1][xpos] == "0"
            y0 = state[::-1][ypos] == "0"
            count = round((states[state] / total) * 100)

            if x0 and y0:
                size[0] += count * 10
            if x0 and not y0:
                size[1] += count * 10
            if not x0 and y0:
                size[2] += count * 10
            if not x0 and not y0:
                size[3] += count * 10

        delete = []
        for i in range(0,3):
            if size[i] < min_tol * 100 * 10:
                delete.append(i)

        delete.reverse()
        for i in delete:
            size.pop(i)
            xout.pop(i)
            yout.pop(i)

        color = "blue"
        plt.scatter(xout, yout, s=size, c=color)

        for i in range(0, len(xout)):
            plt.annotate(str(size[i]/10) + "%", (xout[i]+0.1, yout[i]+0.1))

        plt.set_xlabel(x)
        plt.set_ylabel(y)
        plt.set_xlim(-0.5,1.5)
        plt.set_ylim(-0.5,1.5)
        pyplot.xticks([0, 1])
        pyplot.yticks([0, 1])
        pyplot.get_current_fig_manager().set_window_title('Graph')
        pyplot.show(block=block)

    def multiPieGraph(self, x, y, min_tol = 0.05, block=True):
        fig = pyplot.figure(figsize=(4, 4))
        plt = fig.add_subplot(111)
        states = expand(self.counts)
        total = 0
        for num in states.values():
            total += num

        delete = []
        for state in states:
            if states[state] / total < min_tol:
                delete.append(state)

        for i in delete:
            states.pop(i)

        xpos = self.measures.index(x)
        ypos = self.measures.index(y)
        xout = [0, 0, 1, 1]
        yout = [0, 1, 0, 1]
        size = [0, 0, 0, 0]
        pchartdata = [[], [], [], []]
        pchartcolors = [[], [], [], []]

        colorcounter = 0
        for state in states:
            x0 = state[::-1][xpos] == "0"
            y0 = state[::-1][ypos] == "0"
            count = round((states[state] / total) * 100)

            if x0 and y0:
                size[0] += count * 25
                pchartcolors[0].append(colors[colorcounter])
                pchartdata[0].append(count * 25)
            if x0 and not y0:
                size[1] += count * 25
                pchartcolors[1].append(colors[colorcounter])
                pchartdata[1].append(count * 25)
            if not x0 and y0:
                size[2] += count * 25
                pchartcolors[2].append(colors[colorcounter])
                pchartdata[2].append(count * 25)
            if not x0 and not y0:
                size[3] += count * 25
                pchartcolors[3].append(colors[colorcounter])
                pchartdata[3].append(count * 25)

            colorcounter += 1

        delete = []
        for i in range(0, 3):
            if size[i] < min_tol * 100 * 25:
                delete.append(i)

        delete.reverse()
        for i in delete:
            size.pop(i)
            xout.pop(i)
            yout.pop(i)
            pchartcolors.pop(i)
            pchartdata.pop(i)

        for i in range(0, len(pchartdata)):
            for j in range(0, len(pchartdata[i])):
                pchartdata[i][j] = pchartdata[i][j] / size[i]

        for i in range(0, len(pchartcolors)):
            ge.drawPieMarker(xout[i], yout[i], pchartdata[i], size[i], pchartcolors[i], plt)

        for i in range(0, len(xout)):
            plt.annotate(str(size[i] / 25) + "%", (xout[i] + 0.15, yout[i] + 0.15))

        plt.set_xlabel(x)
        plt.set_ylabel(y)
        plt.set_xlim(-0.5, 1.5)
        plt.set_ylim(-0.5, 1.5)
        pyplot.xticks([0, 1])
        pyplot.yticks([0, 1])
        pyplot.get_current_fig_manager().set_window_title('Graph')
        self.printTable(colorize=True, states=states, min_tol=min_tol)
        pyplot.show(block=block)

    def trueEntangle(self, x, y, states, tol):
        if self.measureLine[self.measures.index(x)] == self.measureLine[self.measures.index(y)]:
            return False
        count0 = 0
        count1 = 0
        xpos = len(self.measures) - 1 - self.measures.index(x)
        for state in states:
            if state[xpos] == '0':
                count0 += states[state]
            else:
                count1 += states[state]

        if count0 / (count0 + count1) < tol or count1 / (count0 + count1) < tol:
            return False
        return True

    def printEntanglementTable(self, cutDiagonal=True, cutRepeats=True, cutEmpty = True,
                               colorize=True, requireTrueEntangle=True, tol = 0.05):
        states = expand(self.counts)

        header = copy.deepcopy(self.measures)
        out = [['E Table'] + header]

        for y in self.measures:
            row = [y]
            for x in header:
                if (x != y or not cutDiagonal) and (self.measures.index(x) > self.measures.index(y) or not cutRepeats):
                    xpos = len(self.measures) - 1 - self.measures.index(x)
                    ypos = len(self.measures) - 1 - self.measures.index(y)
                    if not requireTrueEntangle or self.trueEntangle(x, y, states, tol):
                        row.append(str(round(difference(states,xpos,ypos) * 100)) + '%')
                    else:
                        row.append(str(round(difference(states,xpos,ypos) * 100)) + '*')
                else:
                    row.append('-')
            out.append(row)

        if cutEmpty:
            delete = []
            for row in out:
                dele = True
                for i in range(1, len(row)):
                    item = row[i]
                    if item != "-":
                        dele = False
                if dele:
                    delete.append(row)

            for row in delete:
                out.remove(row)

            delete = []
            for i in range(0, len(out[0])):
                dele = True
                for j in range(1, len(out)):
                    if out[j][i] != "-":
                        dele = False
                if dele:
                    delete.append(i)

            delete.reverse()
            for item in delete:
                for row in out:
                    row.pop(item)

        textlength = [0] * len(out[0])
        for row in out:
            for i in range(0, len(row)):
                if len(row[i]) > textlength[i]:
                    textlength[i] = len(row[i])

        printtable = []
        for row in out:
            printrow = ""
            for i in range(0, len(row)):
                item = row[i]
                spaces = (textlength[i] - len(item))/2
                if colorize:
                    if '%' in item:
                        val = int(item[:-1])
                        if val < tol * 100:
                            item = '\033[94m' + item + '\033[0m'
                        if val > 100 - (tol * 100):
                            item = '\033[92m' + item + '\033[0m'
                    if '*' in item:
                        val = int(item[:-1])
                        if val < tol * 100:
                            item = '\033[91m' + item + '\033[0m'
                        if val > 100 - (tol * 100):
                            item = '\033[91m' + item + '\033[0m'
                printrow += "| " + " " * math.floor(spaces) + item + " " * math.ceil(spaces) + " "
            printrow += "|"
            printtable.append(printrow.replace('*', '%'))

        for row in printtable:
            print(row)
            if row == printtable[0]:
                print("-" * len(row))

    def printEntanglements(self, tol = 0.05, useTrueEntanglement=True):
        states = expand(self.counts)
        for y in self.measures:
            for x in self.measures:
                if (x != y and self.measures.index(x) < self.measures.index(y)
                    and (self.trueEntangle(x, y, states, tol) or not useTrueEntanglement)):
                    xpos = len(self.measures) - 1 - self.measures.index(x)
                    ypos = len(self.measures) - 1 - self.measures.index(y)
                    dif = difference(states,xpos,ypos)
                    if dif < tol:
                        print(x, "is inverse entangled with", y)
                    if dif > 1 - tol:
                        print(x, "is entangled with", y)

    def printQubitStates(self):
        total = 0
        for num in self.counts.values():
            total += num
        qubitcounts = countStates(self.counts, self.measures)
        qcounts = []
        for i in qubitcounts:
            qcounts.append([str(round(i[0] * 100 / total)) + "%",
                            str(round(i[1] * 100 / total)) + "%"])

        maxlength = 0
        for text in self.measures:
            maxlength = max(maxlength, len(text)+2)

        header = " Measure "
        if maxlength > len(header):
            header = " " * math.floor((maxlength - len(header))/2) + header + " " * math.ceil((maxlength - len(header))/2)

        outstr = "|" + header + "|  0  |  1  |"
        print(outstr)
        print("-" * len(outstr))
        for i in range(0, len(self.measures)):
            txt = self.measures[i]
            length = len(txt)
            outstr = "|"
            outstr += " " * math.floor((maxlength - length)/2) + txt + " " * math.ceil((maxlength - length)/2)
            outstr += "|"
            txt = qcounts[i][0]
            length = len(txt)
            outstr += " " * math.floor((5 - length) / 2) + txt + " " * math.ceil((5 - length) / 2)
            outstr += "|"
            txt = qcounts[i][1]
            length = len(txt)
            outstr += " " * math.floor((5 - length) / 2) + txt + " " * math.ceil((5 - length) / 2)
            outstr += "|"
            print(outstr)

        #html table
        out = "<table>" + '\n'
        out += "<tr>" + '\n'
        out += "<th>Measure</th>" + '\n'
        out += "<th>0</th>" + '\n'
        out += "<th>1</th>" + '\n'
        out += "</tr>" + '\n'

        for i in range(0, len(self.measures)):
            out += "<tr>" + '\n'
            out += "<td>" + self.measures[i] + "</td>" + '\n'
            out += "<td>" + qcounts[i][0] + "</td>" + '\n'
            out += "<td>" + qcounts[i][1] + "</td>" + '\n'
            out += "</tr>" + '\n'
        out += "</table>"
        return out




