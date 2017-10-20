import webbrowser

def findBestTicketDeals(ticketDealList):

    editedTicketDealList = ticketDealList[:5]
    count = 0

    for values in editedTicketDealList:
        count = count + 1

        print("===========================Deal {0}=================================").format(count)
        
        airline = values['airline']

        if (airline == ""):
            airline = "Multiple"
        else:
            airline = airline

        print("Departure: " + values['departure'])
        print("Destination: " + values['arrival'])
        print("Departure Date: " + values['departure date'])
        print("Airline: " + airline)
        print("Flight Duration: " + values['flight duration'])
        print("Stop: " + values['stops'])
        print("Cost: " + values['ticket price'] + '\n')
        

        print("---------Layovers---------")
        for arrivalAirports in values['timings']:
            print(arrivalAirports['arrival_airport'] + " :" + arrivalAirports['arrival_time'])

