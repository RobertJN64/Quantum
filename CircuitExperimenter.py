import TestCircuit
import matplotlib.pyplot as pyplot
import os

def run():
    cm = TestCircuit.circuitManager()

    if input("Run on IBM Q? ") == "y":
        cm.sendToIBM()
    else:
        cm.simulate()

    print(cm.counts)

    figa = pyplot.figure()
    plta = figa.add_subplot()
    cm.histogram(plt=plta)

    figb = pyplot.figure()
    pltb = figb.add_subplot()
    cm.circuit.draw(output="mpl", ax=pltb)


    print('\n+++++++\n')
    qStateHTML = cm.printQubitStates()
    print('\n+++++++\n')
    tableHTML = cm.printTable()
    print('\n+++++++\n')
    fulltableHTML = cm.printTable(allStates=True)
    print('\n+++++++\n')
    eTableHTML = cm.printEntanglementTable()
    entanglements = cm.printEntanglements()
    print('\n+++++++\n')

    pyplot.show()

    if input("Save Expirement: ") == "y":
        fullHTML = "<html><head>"

        with open("style.txt") as f:
            style = f.readlines()
        for line in style:
            fullHTML += line

        fullHTML += "</head><body>"

        expirementName = input("Expirement Name: ")
        fullHTML += "<h1>" + expirementName + "</h1>" + '\n'
        expirementName = expirementName.replace(" ", "_").replace("/", "-")
        os.mkdir("Test-Files/" + expirementName)
        expirementDesc = input("Description: ")
        fullHTML += "<p>" + expirementDesc + "</p>" + '\n'
        if input("Save Circuit Image: ") == "y":
            figb.savefig(expirementName + '/circuit')
            fullHTML += "<img width=50% src='circuit.png'><br>" + '\n'
        if input("Save Histogram: ") == "y":
            figa.savefig(expirementName + '/histogram')
            fullHTML += "<img width=50% src='histogram.png'><br>" + '\n'
        if input("Qubit State Table: ") == "y":
            fullHTML += qStateHTML + '<br>'
        if input("State Table: ") == "y":
            if input("Full: ") == "y":
                fullHTML += fulltableHTML + '<br>'
            else:
                fullHTML += tableHTML + '<br>'
        if input("Entanglement Table: ") == "y":
            fullHTML += eTableHTML + entanglements

        fullHTML += "</body></html>"

        with open(expirementName + "/report.html", "w") as f:
            f.write(fullHTML)


