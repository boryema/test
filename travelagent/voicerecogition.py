import speech_recognition as sr
import re

def voicerecognition():
     r = sr.Recognizer()
     with sr.Microphone() as source:
        audio = r.listen(source)
     try:
        agent=r.recognize_google(audio)
        print("")
        print("*****************CESLeA Recognised..."+ "\n")
        if(agent=="Cecilia" or agent=="CESLeA"):
            agent = "CESLeA"
            
        return agent    

     except sr.UnknownValueError:
        waiting = "Waiting..."
        return waiting
       #print("Google Speech Recognition could not understand audio")
        
     except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    #Until this point. Replica of this code have changed those of 'raw_input'.  
        
def voiceRecognitionUser():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        userResponse=r.recognize_google(audio)
        print ("Finally recognised")
        return userResponse
   
    except sr.UnknownValueError:
        waiting = "Waiting..."
        print waiting
        return waiting
    except sr.RequestError as e:
        return ("Could not request results from Google Speech Recognition service; {0}".format(e))



def formatedDate(sentence):
    #sentence = " Sunday 16th of December 2017"
    months={"January":1,"February":2, "March":3, "April":4, "May":5, "June":6,
        "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
    
    dates = re.findall('\d+', sentence)
    
    day = dates[0]
    year = dates[1]
   
    convertedsentenceList = sentence.split()
    month = convertedsentenceList[-2] 
    
    
    if(month in months):
        month = months[month]
        
    else:
        print ("We could not understand the date")
    
    formateddate = str(month)+"/"+str(day)+"/"+str(year)
    
    return formateddate
    
            

        
    
          
              

    
   

    
     
        
        
        
            
        
