import datetime
import os


def searchairportdata(mystr):
    airports=[]
    stripedline =[]
    results = {}
    airportname = ""
    airportcode = ""
    MYDIR = os.path.dirname(__file__)

    with open(os.path.join(MYDIR, 'airport/final_airports.txt'), 'r+') as inF:
        for line in inF:
            stripedline = line.split(",")
            airportcountrylocation = stripedline[1].strip()
            airportname = stripedline[0].strip()
            airportcode = stripedline[2].strip()

            if  mystr in {airportcountrylocation,airportname}: #Checking for bot the country and the airport name
                print (airportname + "," + airportcountrylocation + "," + airportcode)
                airport = airportname + "," + airportcountrylocation + "," + airportcode
                airports.append(airport)
                break

        airportsNumber = len(airports) #Number of airports selected from the file
        if (airportsNumber>1):
            #Change this to cater for the many airports selected
            results = results
        elif(airportsNumber==1):
            #When only one airport selected
            results.update({"airportname": airportname})
            results.update({"airportcode": airportcode})
        elif (airportsNumber == 0):
            results = results

    return results
    
def validateDate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
        value = True
    except ValueError:
        value = False

    return value




















