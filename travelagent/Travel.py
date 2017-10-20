import json

import sys
sys.path.append("/home/asdf/git_repos/Travel_agent")
import searchairport
import scraper
import nltk
import voicerecogition
import pyttsx

def Keyword_extracting(sen):

    word = []   #extracting place(airport)
    LaSen = sen[0].replace(" ", "")
    LaLow = LaSen.lower()
    if 'losangeles' in LaLow:
        word.append("La")
    else:
        text = nltk.word_tokenize(sen[0])
        pos = nltk.pos_tag(text)
        n = len(text)
        for j in range(n):
            if pos[j][1] == 'NNP' or 'NN':
                word.append(pos[j][0])

    for i in range(4):   #extracting date
        text = nltk.word_tokenize(sen[i])
        pos = nltk.pos_tag(text)
        n = len(text)
        for j in range(n):
            if pos[j][1] == 'CD':
                word.append(pos[j][0])

    word[0] = word[0][0].upper()+word[0][1:].lower()

    return word


# This is the Main class
if __name__ == "__main__":

    continueruning = "Y"
    while (continueruning=="Y"):

        print("")
        print("")
        print("===============Travel Agent: CESLeA=======================")

        questionList = ['Where do you plan to go?',
                        'When do you plan to go?',
                        'Why are you travelling?',
                        'Are you travelling alone?'
                        ]
        sentenceResponseList = []

        #        agent = raw_input('User : ')
        #This is the change from 'raw_input' to speech recognition.
        agent = voicerecogition.voicerecognition()
        print("User: " + agent)

        if agent == 'CESLeA' or 'ceslea' or 'CESLEA' or 'Ceslea':

            engine = pyttsx.init()
            engine.say('How may I help you? ')
            engine.runAndWait()
            print('CESLeA : How may I help you? ')
            print("")

            for i in range(4):

                #                userResponse = raw_input('User : ')
                userResponse = voicerecogition.voiceRecognitionUser()
                while(userResponse=="Waiting..."):
                    userResponse = voicerecogition.voiceRecognitionUser()
                if(i==1):
                    place=userResponse
                    #print("Place: "+ place)
                if(i==2):
                    dateSentence = userResponse

                print("User: " + userResponse)
                #                engine = pyttsx.init()
                #                for word in questionList[i].split():
                #                    engine.say(word)
                #                engine.runAndWait()

                print(questionList[i])
                print("")
                sentenceResponseList.append(userResponse)

        else:
            print('I am not %s.' %agent)
            exit()

        keyword = Keyword_extracting(sentenceResponseList)

        originInformationList = searchairport.searchAirport("Incheon")
        originAirportName = originInformationList[0]
        originAirportCode = originInformationList[1].strip()

        destinationInformationList = searchairport.searchAirport(keyword[0])
        destinationAirportName = destinationInformationList[0]
        destinationAirportCode = destinationInformationList[1].strip()
        # print destinationAirportName

        departureDate = voicerecogition.formatedDate(dateSentence)

        while (searchairport.validateDate(departureDate)==False):
            departureDate = raw_input ("Please enter the correct departure date(mm/dd/yy): ")

        print("CESLeA: Okay these are the best 5 airticket deals for your travel")
        scraped_data = scraper.scrapeTheInformation(originAirportCode, destinationAirportCode, departureDate)

        # "All the ticket prices are then written to the json file..."
        with open('%s-%s-flight-results.json' % (originAirportCode, destinationAirportCode), 'w') as fp:
            json.dump(scraped_data, fp, indent=4)


        print("")
        continueruning=raw_input("Do you still want to use CESLeA?(Y/N)").strip().capitalize()

        if(continueruning=="Y"):
            continueruning="Y"
        else:
            continueruning="N"
            print("Thank you. Bye...");
            exit();
            
        
     
