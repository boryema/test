from bs4 import BeautifulSoup
import requests


def scrapeHotels(destination, checkIn, checkOut):
    latLong = pickLatLongFromALocation(destination)
    latitude = latLong['latitude']
    longitude = latLong['longitude']
    address = latLong['address']
    allHotels = []

    url = "https://www.expedia.co.kr/Hotel-Search-Data?responsive=true&destination={0}&startDate={1}&endDate={2}&rooms=1&adults=2&timezoneOffset=32400000&siteid=16&langid=1033&hsrIdentifier=HSR&?1507581116345".format(
        address, checkIn, checkOut)

    response = requests.post(url)
    data = response.json()

    for i in range(0, 5):
        hotelName = data['searchResults']['retailHotelModels'][i]['retailHotelInfoModel']['hotelName']
        hotelPrice = data['searchResults']['retailHotelModels'][i]['retailHotelPricingModel']['price']
        hotelRating = data['searchResults']['retailHotelModels'][i]['hotelStarRating']
        hotelImageLocation = pickExactHotelImageAddress(data['searchResults']['retailHotelModels'][i]['infositeUrl'])
        hotelAddress = address

        hotelDictionary = {"hotelName": hotelName, "hotelPrice": hotelPrice, "hotelRating": hotelRating,
                           "hotelImageLocation": hotelImageLocation, "hotelAddress": hotelAddress}
        allHotels.append(hotelDictionary)
        # print "\n"
        # print "=====================Deal " + str(i) + "============================="
        # print "Hotel Name: {0}".format(
        #     data['searchResults']['retailHotelModels'][i]['retailHotelInfoModel']["hotelName"])
        # print "Hotel Price: {0}".format(
        #     data['searchResults']['retailHotelModels'][i]['retailHotelPricingModel']["price"])
        # print "Hotel Rating".format(data['searchResults']['retailHotelModels'][i]['hotelStarRating']) + "\n"
        # print "Location {0}".format(address) + "\n"
        # print "Hotel address {0}".format(hotel.pickExactHotelImageAddress(data['searchResults']['retailHotelModels'][i]["infositeUrl"])) + "\n"


    return allHotels


def writingToAfile(fileName, content):
    with open(fileName, "w+") as file:
        file.writelines(str(content))

def pickLatLongFromALocation(location):
    # api-endpoint for picking latitude and longitude
    URL = "http://maps.googleapis.com/maps/api/geocode/json"
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {"address": location}

    # sending get request and saving the response as response object
    getRequest = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = getRequest.json()

    # extracting latitude, longitude and formatted address
    # of the first matching location
    latitude = data['results'][0]['geometry']['location']['lat']
    longitude = data['results'][0]['geometry']['location']['lng']
    formattedAddress = data['results'][0]['formatted_address']

    results = {"latitude": latitude, "longitude": longitude, "address": formattedAddress}

    return results


def pickExactHotelImageAddress(hotelExpediaAddress):
    exactAddress = []
    getResponse = requests.post(hotelExpediaAddress)
    javascriptContent = BeautifulSoup(getResponse.text, 'lxml')

    writingToAfile("hotelinfo.txt", javascriptContent)

    with open("hotel.txt", "a+") as readingFile:
        lines = readingFile.readlines()

        for line in lines:
            if line.startswith("infosite.url"):
                resultsList = line.split("'")
                exactAddress = resultsList[1]

    return exactAddress
