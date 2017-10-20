import json
import sys

import logging

sys.path.append("/home/woo/git_repos/expediascraperoneway")
import requests
from lxml import html
from collections import OrderedDict
import getexceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This is to Scrape the expedia.com site for airticket prices
def scrapeTheInformation(source, destination, date):

    for i in range(5):
        try:

            url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search".format(
                source, destination, date)
            logger.info("Creating URL: "+ url)

            #Thus is to check the Exceptions
            json_data_xpath = getexceptions.checkingForNonEmptyList(url)

            raw_json = json.loads(json_data_xpath[0])
            flight_data = json.loads(raw_json["content"])


            flight_info = OrderedDict()
            lists = []

            for i in flight_data['legs'].keys():
                total_distance = flight_data['legs'][i]["formattedDistance"]
                exact_price = flight_data['legs'][i]['price']['totalPriceAsDecimal']

                departure_location_airport = flight_data['legs'][i]['departureLocation']['airportCity']
                departure_location_city = flight_data['legs'][i]['departureLocation']['airportCity']
                departure_location_airport_code = flight_data['legs'][i]['departureLocation']['airportCode']

                arrival_location_airport = flight_data['legs'][i]['arrivalLocation']['airportCity']
                arrival_location_airport_code = flight_data['legs'][i]['arrivalLocation']['airportCode']
                arrival_location_city = flight_data['legs'][i]['arrivalLocation']['airportCity']
                airline_name = flight_data['legs'][i]['carrierSummary']['airlineName']

                no_of_stops = flight_data['legs'][i]["stops"]
                flight_duration = flight_data['legs'][i]['duration']
                flight_hour = flight_duration['hours']
                flight_minutes = flight_duration['minutes']
                flight_days = flight_duration['numOfDays']

                if no_of_stops == 0:
                    stop = "Nonstop"
                else:
                    stop = str(no_of_stops) + ' Stop'

                total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days, flight_hour, flight_minutes)

                departure = departure_location_airport + ", " + departure_location_city
                arrival = arrival_location_airport + ", " + arrival_location_city
                carrier = flight_data['legs'][i]['timeline'][0]['carrier']
                plane = carrier['plane']
                plane_code = carrier['planeCode']
                formatted_price = "{0:.2f}".format(exact_price)

                if not airline_name:
                    airline_name = carrier['operatedBy']

                timings = []
                for timeLine in flight_data['legs'][i]['timeline']:
                    if 'departureAirport' in timeLine.keys():
                        departure_airport = timeLine['departureAirport']['longName']
                        departure_time = timeLine['departureTime']['time']
                        arrival_airport = timeLine['arrivalAirport']['longName']
                        arrival_time = timeLine['arrivalTime']['time']
                        flight_timing = {
                            'departureairport': departure_airport,
                            'departuretime': departure_time,
                            'arrivalairport': arrival_airport,
                            'arrivaltime': arrival_time
                        }
                        timings.append(flight_timing)

                flight_info = {'stops': stop,
                               'ticketprice': "$"+formatted_price,
                               'departure': departure,
                               'arrival': arrival,
                               'flightduration': total_flight_duration,
                               'airline': airline_name,
                               'plane': plane,
                               'timings': timings,
                               'planecode': plane_code,
                               'departuredate':date
                               }
                lists.append(flight_info)

            # sortedList = sorted(lists, key=lambda ticketPrice: float(ticketPrice['ticket price']), reverse=False)
            # print lists
            #This sorts the list into increasing order of ticket prices
            sortedList = sorted(lists, key=lambda ticketPrice: float(ticketPrice['ticketprice'].lstrip("$")))

            # This checks for the best five ticket deals and prints them out to the user
            bestFiveTicketDeals = sortedList[:5]
            #This then requests a user if he is interested in purchasing the tickets.
           # ticketdeals.openBrowserToPurchaseTicket(url)


            return bestFiveTicketDeals

        except ValueError:
            print "Retrying to connect..."

        return {"error": "failed to process the page", }


