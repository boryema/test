import datetime

from django.shortcuts import render
from django.http import JsonResponse

from travelagent import wordmanipulator, searchairport, scraper
from .forms import SendConversation



def index(request):
    return render(request, 'index.html', {})

def conversation(request):
    sentime= datetime.datetime.today()
    sentime = sentime.strftime("%d-%B-%Y %H:%M:%S")

    if request.method == 'POST':
        # POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            # Always use get on request.POST. Correct way of querying a QueryDict.
            sentmessage = request.POST.get('message')
            trackingagentresponse = request.POST.get('trackingagentresponse')
            agentResponse = ''
            scraped_data = []

            # Returning same data back to browser.It is not possible with Normal submit

##################Processing agent response starts from here##########
            questionList = ['Where do you plan to go?',
                            'When do you plan to go?',
                            'Why are you travelling?',
                            'Are you travelling alone?'
                            ]
            sentenceResponseList = []


            if(sentmessage in {'CESLeA', 'ceslea','CESLEA', 'Ceslea'}):
                agentResponse = "How may I help you?"

                # Creating a file and Writes the questions on a file
                file = open("questions.txt", "w+")
                questionNumber = 1

                for question in questionList:
                    file.write(question+"\n")
                    questionNumber = questionNumber+1
                file.close()

            else:
                # Pick first question from the file
                questionFile = open("questions.txt", "r+")
                contentLine = questionFile.readlines()
                questionFile.seek(0)
                questionFile.truncate()

                for line in contentLine:
                ######################## Update the sentence ###############
                    if (trackingagentresponse == line):
                        strToSearchFor = trackingagentresponse
                        strToReplace = trackingagentresponse.replace("\n", '')+" "+sentmessage +"\n"
                        line = line.replace(strToSearchFor, strToReplace)

                    questionFile.write(line)
                questionFile.close()

                ########################End of this #################################

                ######################## This is to pick the next question ###############
                with open("questions.txt", "r+") as file:
                    fileLine = file.readlines()

                    for line in fileLine:
                        index = ''
                        letters = set('?')
                        splitString = line.split()
                        indexOfLastElement = len(splitString) - 1

                        for word in splitString:
                            if letters & set(word):
                                index = splitString.index(word)  # Index of the word with a question mark

                        if (splitString[index] == splitString[indexOfLastElement]):
                            agentResponse = line
                            break
                ######################## End of picking the next question ###############

##This is Checking the End of the conversation to begine processing the air ticket
                    if(agentResponse==""):
                        agentResponse = "Please I will suggest cheaper flights to your destination"
                    if(sentmessage in {"Okay", "Please do"}):
                    #Pick all the responses from the user
                    #Then format to get the parameters
                        sentence = []
                        destinationAirportCode = ''
                        airportname = ''
                        with open("questions.txt", "r+") as file:
                            extractedLines = file.readlines()
                            questionEnding = set('?')
                            for line in extractedLines:
                                splitStr =line.split()
                                for word in splitStr:
                                    if questionEnding & set(word):
                                        index = splitStr.index(word)
                                        listWord = splitStr[index+1:] #This is picking user responses from the file.
                                        constructedWord = " ".join(listWord)

                                        sentence.append(constructedWord) #This is then appended to the sentence list


                        results = wordmanipulator.formatargvalues(sentence)
                        destinationreults = searchairport.searchairportdata(results['destinationairport'])
                        if (len(destinationreults) != 0):
                            airportname = destinationreults['airportname']
                            destinationAirportCode =  destinationreults['airportcode']
                        else:
                            print 'There are no airports selected'

                        departureDate = results['traveldate']

                        print "AirportName:{0} \nAirportCode:{1} \nTravel Date: {2} ".format(airportname, destinationAirportCode, departureDate)

                        scraped_data = scraper.scrapeTheInformation("ICN", destinationAirportCode, departureDate)
                        print scraped_data
                        exit()

            if len(scraped_data)== 0:
                # ################## Processing agent response ends here##############
                data = {"textedmessage": sentmessage, "time": sentime, 'agentresponse':agentResponse}
                return JsonResponse(data)
            ###This is to print the scraped data finally after the conversation is made
            else:
                return render(request, 'conversation.html', scraped_data)


            # Get goes here
    return render(request,'conversation.html')


















def getMessage(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SendConversation(request.POST)

        if form.is_valid():
            data = form.clean_sent_data()
            return render(request, 'conversation.html', {'sent': "Brian"})
    else:
        # Check if the form is valid:
        form = SendConversation()

        return render(request, 'conversation.html', {'form': form})

#
# # Create your views here.
# def home(request):
#     if request.method == 'POST':
#         # POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
#         if request.is_ajax():
#             # Always use get on request.POST. Correct way of querying a QueryDict.
#             sentmessage = request.POST.get('message')
#             data = {"message": sentmessage}
#             # Returning same data back to browser.It is not possible with Normal submit
#
#             return JsonResponse(data)
#             # Get goes here
#     return render(request,'conversation.html')




