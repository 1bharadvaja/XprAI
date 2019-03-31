import numpy as np
import cv2
import time
import speech_recognition as sr
import gtts
import playsound


def soundrecognizer():
    global text
    r = sr.Recognizer() 
    mic_list = sr.Microphone.list_microphone_names() 
    with sr.Microphone(device_index = 2, sample_rate = 48000,chunk_size = 2048) as source:
        r.adjust_for_ambient_noise(source) 
        print("Say Something")
        audio = r.listen(source)     
        try: 
            text = r.recognize_google(audio) 
            print("you said: " + text)
            return(text)

        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))



smilecount = 0

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_smile.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
##start=time.time()

while True:
##    end=time.time()
    ret, img = cap.read()
    ret, gray = cap.read()
    #img = cv2.flip(img, -1)
##    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,      
        minSize=(30, 30)
    )

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        eyes = eyeCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors=5,
            minSize=(5, 5),
            )
        
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)
            cv2.rectangle(roi_gray, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)
        
        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors=15,
            minSize=(25, 25),
            )
        
        for (xx, yy, ww, hh) in smile:
            smilecount = smilecount + 1
            cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)
            cv2.rectangle(roi_gray, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)
        cv2.imshow('video', img)
##    if end-start>10:
##        break
        
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    print('Your smile count is', smilecount)
time.sleep(5)
pos=['why not','really good','cool','sure','okay','very nice','very very nice','pretty good','ok','alright','happy','good','fine','I have been feeling good','I have been feeling fine','I am happy','pretty good','yes','Yes','YES','Ok','yeah']
neg=['really bad','not really','sad', 'depressed','not good','suicidal','never','no','nah','No','Nah','bad','pretty bad']
ed=0
if smilecount < 100:
    q1='We have detected that you are feelin sad, Could we survey you?'
    vq1=gtts.gTTS(text=q1)
    vq1.save("q1.mp3")
    playsound.playsound("q1.mp3")

    print(q1)
    ans=soundrecognizer()
    print(ans)
    if ans in neg:
        q2='ok thank you for your time'
        vq2=gtts.gTTS(text=q2)
        vq2.save("q2.mp3")
        playsound.playsound("q2.mp3")
        print(q2)
    if ans in pos:
        q3='Ok,first question. How have you been feeling lately.'
        vq3=gtts.gTTS(text=q3)
        vq3.save("q3.mp3")
        playsound.playsound("q3.mp3")
        print(q3)
        ed=ed+1
        ans1=soundrecognizer()

        if ans1 in pos:
            q4='Next question, are you having a hard time trusting your friends'
            vq4=gtts.gTTS(text=q4)
            vq4.save("q4.mp3")
            playsound.playsound("q4.mp3")
            print(q4)
            ed=ed+1
            ans2=soundrecognizer()
            if ans2 in neg:
                ed=ed+1
                print('You have a positivity counter of',ed)
            if ans2 in pos:
                q5='Have you been feeling depressed'
                vq5=gtts.gTTS(text=q5)
                vq5.save("q5.mp3")
                playsound.playsound("q5.mp3")
            

                print(q5)
                ed=ed-1
                ans4=soundrecognizer()
                if ans4 in pos:
                    ed=ed-1
                    print('You have a positivity counter of',ed)
                if ans4 in neg:
                    ed=ed+1
                    print('You have a positivity counter of',ed)
                    

            
        if ans1 in neg:
            ed=ed-1
            q6='Next question, have you been feeling depressed?'
            vq6=gtts.gTTS(text=q6)
            vq6.save("q6.mp3")
            playsound.playsound("q6.mp3")
            print(q6)
            ans3=soundrecognizer()
            if ans3 in pos:
                ed=ed-1
                print('you have a positivity counter of',ed)
            elif ans3 in neg:
                ed=ed+1
                print('you have a positivity counter of',ed)

    if ed==1:
        print('Processing your emotion...')
        time.sleep(4)
        print('Looks like your having a good day')
    elif ed==-1:
        print('Processing your emotion...')
        time.sleep(4)
        print('Hmm seems like you are having a bad day. Having a more positive outlook might help you')
    elif ed==2:
        print('You seem like you are generally a happy person')
    elif ed== -2:
        print('You seem sad. You should maybe talk to a loved one about our emotions.')
    elif ed==3:
        print('Wow... your happiness made my day. Keep it up')
    elif ed== -3:
        print('You might have chronic dpression. Try to schedule an appointment with your counselor.')
else:
    print('Looks like you are very happy!')




    
    

    



    
    
cap.release()
cv2.destroyAllWindows()
