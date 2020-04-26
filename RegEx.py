import re

# FILE I/O
file = open("pham.txt", "r")
lines = file.readlines()
file.close()

# VARIABLES
linesSearched = 10
dataset = {
    "Case ID": "",
    "First Name": "",
    "Middle Name": "",
    "Last Name": "",
    "Gender": "",
    "Date of Birth": "",
    "Jurisdiction Name": "",
    "Jurisdiction County": "",
    "Jurisdiction State": "",
    "Offense Date": "",
    "Arrest Date": "",
    "File Date": "",
    "Disposition Date": "",
    "Charge Text": "",
    "Charge Status": "",
    "Disposition Text": "",
    "Sentencing Notes": "",
    "Jail Time": "",
    "Probation Time": "",
    "Fine(s)": ""
}

# REGEX PATTERNS
namePat = re.compile(r"\w+(,)?\s\w+(\s\w+)?")
datePat = re.compile(r"(\d+)?(-)?\d+-\d+")
moneyPat = re.compile(r"\$(\d{1,3})?(,)?(\d{1,3})?(,)?\d{1,3}(.)?(\d+)?")
jailPat = re.compile(r"\d+\s\b(?:year|years|month|months)\b")
statePat = re.compile(r"state\sof\s\w+")
genderPat = re.compile(r"\b(?:male|female|m|f)\b")
countyPat = re.compile(r"\w+\scounty")
idPat = re.compile(r"(?<=case\s)\w+\s\w+")
statPat = re.compile(r"\w+\s\w+\s-\s\w+\s\w+")

# FUNCTIONS
def searchFor(var):
    searchSection = []
    # print(var.upper(), ":")
    countName = 0
    testLine = ""
    for idx, line in enumerate(lines):
        line = line.strip().lower()
        # print line
        if (line.find(var)!= -1):
            for i in range(linesSearched):
                testLine = lines[idx + i].strip().lower()
                searchSection.append(testLine);
                # print(testLine)
            countName += 1
    # print("---------------------------\n")
    return searchSection

def matchRegex(array, pat, specified):
    result = None
    for string in array:
        result = re.search(pat, string)
        if result and (specified not in result.group()):
            # print(result.group())
            return result.group()

# SEARCHING...
dataset["First Name"] = matchRegex(searchFor("defendant name"), namePat, "name")
dataset["Date of Birth"] = matchRegex(searchFor("date of birth"), datePat, "X")
dataset["Fine(s)"] = matchRegex(searchFor("bond amount"), moneyPat, "X")
dataset["Jurisdiction State"] = matchRegex(searchFor("state"), statePat, "X")
dataset["Gender"] = matchRegex(searchFor("sex"), genderPat, "X")
dataset["Jurisdiction County"] = matchRegex(searchFor("county"), countyPat, "X")
dataset["Offense Date"] = matchRegex(searchFor("violation"), datePat, "X")
dataset["File Date"] = matchRegex(searchFor("filing"), datePat, "X")
dataset["Case ID"] = matchRegex(searchFor("case"), idPat, "X")
dataset["Charge Status"] = matchRegex(searchFor("status"), statPat, "X")
dataset["Jail Time"] = matchRegex(searchFor("time"), jailPat, "X")

# FINAL PRINT
print()
for x in dataset:
    print(x,":",dataset[x])
print()
