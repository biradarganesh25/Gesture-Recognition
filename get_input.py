import numpy as np
from sklearn.externals import joblib
import sys
sys.path.append('/home/ganesh/PycharmProjects/Gesture To Text/lib/x64')
confidence = 0
import Leap
import pyttsx # Library used for text to speech conversion.

# A very similar version of this program was used to create the dataset.
# Main program which takes input gestures from the user and
# speaks out the answers.

def main():
    global confidence
    model = joblib.load("RBFSVC_model.pkl") # Loading the model dumped by create_model_RBF.py
    controller = Leap.Controller()
    while not controller.is_connected: #Keep waiting until leap is connected
        pass
    print "Connected."
    ans = 'y'
    #Setting up the text to speech API
    engine = pyttsx.init()
    rate = engine.getProperty("rate")
    engine.setProperty("rate",rate - 50)
    engine.say("Place your hand to calibrate:")
    engine.runAndWait()
    engine.say(" ")
    engine.runAndWait()

    #Calibrating the hand values
    calib = calibrate()
    
    
    
    print "Calilbrated value is: ",calib
    print "Enter Input..."
    # Taking inputs and predicting the gestures.
    while controller.is_connected:
        # Keep waiting until the hand is static
        moving()
        # Take the input after hand starts moving until the hand stops moving.
        take_input(calib)
        # Using confidence to determine whether an accurate prediction
        # can be made. This is because Leap does not always detect the
        # hands properly, if they are moving very fast.
        if confidence > 0.5:
            data = np.genfromtxt("input.txt")
            y_predict = model.predict(data.reshape(1, -1)) # Using the saved model to predict.
            answer = int(y_predict)
            engine.say(str(answer))
            print y_predict
        # Stop until the hand starts moving again.
        not_moving()


# Fucntion which loops until the hand stop moving
def moving():
    controller = Leap.Controller()
    while not controller.is_connected:
        pass
    fingers = []
    while not fingers: # Keep waiting for the fingers to be detected.
        frame = controller.frame()
        fingers = frame.fingers
        pass
    last_frame = 0
    while controller.is_connected:
        frame = controller.frame()
        if frame.id != last_frame:
            last_frame = frame.id
            fingers_1 = []
            for index_type in range(0,5): # Sort the fingers from thumb to pinky.
                fingers_1.append(frame.fingers.finger_type(index_type)[0])
            check(fingers_1)
            flag = 0
            for finger in fingers_1:
                if finger.tip_velocity.magnitude < 200:
                    flag = flag + 1
            if flag == 5:
                return 1


# A helper fuction which finds out the number of fingers.
def check(fingers_1):
    for i in range(len(fingers_1)):
        if fingers_1[i].tip_position.magnitude == 0:
            exit()


# Function which take the input and send it to the main function
def take_input(calib):
    global confidence

    file_input = open('input.txt','w')
    controller = Leap.Controller()
    count = 0
    last_frame = 0
    frame = controller.frame() # Getting the frame object to take the inputs.
    confidence = frame.hands[0].confidence
    if confidence < 0.5:
        print "The confidence is very low. Try again. " # Don't take the input if the confidence if very low.
        return

    while  count < 100:# Take the input values for the next 100 frames. Then stop.
        frame = controller.frame()
        if frame.id != last_frame:
            #print ".",
            last_frame = frame.id
            fingers_1 = []
            for index_type in range(0,5): # Sort the fingers from thumb to pinky.
                fingers_1.append(frame.fingers.finger_type(index_type)[0])

            check(fingers_1)

            palm_center = frame.hands[0].palm_position
            for i in range(0,5):
                finger = fingers_1[i]
                for i in range(0,4):
                    bone = finger.bone(i)
                    dist_bone = palm_center.distance_to(bone.next_joint)
                    file_input.write(str(dist_bone / calib) + " ")

            thumb = fingers_1[0].tip_position

            for i in range(1,5):
                dist = thumb.distance_to(fingers_1[i].tip_position)
                file_input.write(str(dist / calib) + " ")

            count = count + 1
    file_input.write("\n")
    file_input.close()


# Wait till the hand starts moving.
def not_moving():
    controller = Leap.Controller()
    while not controller.is_connected:
        pass
    # Waiting until hand is moving.
    fingers = []
    while not fingers:  # Keep waiting for the fingers to be detected.
        frame = controller.frame()
        fingers = frame.fingers
        pass
    # Fingers detected.
    last_frame = 0
    while controller.is_connected:
        frame = controller.frame()
        if frame.id != last_frame:
            last_frame = frame.id
            fingers_1 = []
            for index_type in range(0, 5):  # Sort the fingers from thumb to pinky.
                fingers_1.append(frame.fingers.finger_type(index_type)[0])
            check(fingers_1)
            for finger in fingers_1:
                 if finger.tip_velocity.magnitude > 200:
                     return

# Function which calibrates the hand, i.e normalizes the input hands so that it is uniform for all the users
def calibrate():
    print "Calibrating hand. Please hold it steady."
    moving()
    controller = Leap.Controller()
    frame = controller.frame()
    hands = frame.hands
    fingers = frame.fingers
    middle_finger = fingers[2]
    for finger in fingers:
        if finger.type == 2:
            middle_finger = finger
            break
    last_frame = 0
    palm_center = hands[0].palm_position
    calib = palm_center.distance_to(middle_finger.tip_position)
    #Normalizing with respect to the distance of the middle finger tip to the center of the palm
    print "Calibrating done. Please remove your hand."
    while controller.is_connected:
        frame = controller.frame()
        if frame.id != last_frame:
            last_frame = frame.id
            hands = frame.hands
            if not hands:
                return calib




if __name__ == '__main__':
    main()





