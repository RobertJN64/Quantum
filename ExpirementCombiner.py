def run():
    fullreport = "<html><head>"
    #region style

    with open("style.txt") as f:
        style = f.readlines()
    for line in style:
        fullreport += line
    fullreport += "</body>"

    #endregion
    with open("Test-Files/ExpirementList.txt") as f:
        exps = f.readlines()

    for exp in exps:
        with open("Test-Files/" + exp + "/report.html") as f:
            report = ''.join(f.readlines())

        report = report.replace("circuit.png", "Test-Files/" + exp + "/circuit.png")
        report = report.replace("histogram.png", "Test-Files/" + exp + "/histogram.png")

        startindex = report.index('<body>') + len('<body>')
        endindex = report.index('</body>')

        fullreport += '<div>' + report[startindex:endindex] + '</div>'

    #region
    fullreport += "</body></html>"
    with open("QC_Report.html", "w") as f:
        f.writelines(fullreport)


