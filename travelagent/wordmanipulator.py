from datetime import datetime, timedelta

import nltk
import re


def formatargvalues(userresponselist):
    value = {}
    airportName = {}
    travelDate = {}
    demAirport= ''
    #userresponselist = userresponselist.split()
    userResponseListLen = len(userresponselist)
    # print userresponselist
    # print userResponseListLen

    for i in range(userResponseListLen):
        tokenizedSentenceUserResponse = nltk.word_tokenize(userresponselist[i])
        tokenizedSentenceUserResponsetag = nltk.pos_tag(tokenizedSentenceUserResponse) #Tokenizing the sentence
        tokenizedSentenceUserResponsetaglen = len(tokenizedSentenceUserResponsetag) #Length of tokenized sentence

        for j in range(tokenizedSentenceUserResponsetaglen):
            indexForTheTagName = 0
            indexForTheTagValue = 1

            #Getting the airportName
            if(tokenizedSentenceUserResponsetag[j][indexForTheTagValue] == 'NNP'):

                demAirport = demAirport+ " " + tokenizedSentenceUserResponsetag[j][indexForTheTagName]
                demAirport = demAirport.strip()

                airportName = {"destinationairport": demAirport}
                value.update(airportName)

            # Getting the travelDate
            if (tokenizedSentenceUserResponsetag[j][indexForTheTagValue] == 'CD'):
                uneditedTravelDate = tokenizedSentenceUserResponsetag[j][indexForTheTagName]
                editedTravelDate = formatFlightDate(uneditedTravelDate)
                travelDate = {"traveldate":editedTravelDate }
                value.update(travelDate)

    return value

def formatFlightDate(strDate):
    split = re.findall('\d+', strDate)
    formatdate = split[1]+"/"+split[0]+"/"+split[2]

    return formatdate

def formatDate(strDate):
    split = re.findall('\d+', strDate)
    strDate = split[1]+"/"+split[0]+"/"+split[2]

    formatdate = datetime.strptime(strDate,'%d/%m/%Y').strftime('%Y.%m.%d')

    return formatdate


def increaseThisDayByTwoDays(strDate):
    date = datetime.strptime(strDate,'%Y.%m.%d')
    modifiedDate = date + timedelta(days=3)
    increasedDateByThree = datetime.strftime(modifiedDate,'%Y.%m.%d')

    return increasedDateByThree