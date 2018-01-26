# Creates dataset

import sys,time
sys.path.append('/home/ganesh/PycharmProjects/Gesture To Text/lib/x64')

# Importing Leap SDK
import Leap

# The dataset contains the distance of all the bones in all the fingers
# to the palm center, the distance of thumbs to all the finger tips.
# This is all per frame. For one training example, 100 frames are used.

def main():
    # Creating dataset by asking for the gesture first, and
    # the number of examples we want to add.
    print "Enter the label:"
    label = raw_input('>')
    print "Enter the number of examples:"
    total_ex = int(raw_input('>'))
    controller = Leap.Controller()
    while not controller.is_connected:
        pass
    print "Connected."
    count_ex = 0
    # Used to normalize the finger lengths across people
    # so that dataset can scale well to real world examples.
    calib = calibrate()
    print "The calibrated value is : ",calib
    print "Start training..."
    while controller.is_connected and count_ex < total_ex:
        # This function detects that your hand is moving.
        # We need to start taking input when the hand stops moving.
        moving()
        # The function where the input is taken.
        take_input(label,calib)
        # Again, one more function to loop while the user changes
        # the gesture he's performing.
        not_moving()
        count_ex = count_ex + 1


# Looping function before the user makes the gesture.
def moving():
    controller = Leap.Controller()
    while not controller.is_connected:
        pass
    fingers = []
    while not fingers: #Keep waiting for the fingers to be detected.
        frame = controller.frame()
        fingers = frame.fingers
        pass
    print "Fingers detected."
    time.sleep(1)
    print "Waiting until hand stops moving."
    last_frame = 0
    while controller.is_connected:
        frame = controller.frame()
        if frame.id != last_frame: # Ensuring that we won't process the same frame twice.
            last_frame = frame.id
            fingers_1 = []
            for index_type in range(0,5): #Sort the fingers from thumb to pinky.
                fingers_1.append(frame.fingers.finger_type(index_type)[0])
            check(fingers_1)
            flag = 0
            for finger in fingers_1:
                if finger.tip_velocity.magnitude < 200:
                    # Using the velocity to guess whether
                    # the hand is moving or not.
                    flag = flag + 1

            if flag == 5:
                print "Hand not moving. Starting to take input."
                return 1


# Helper function to ensure that the finger tip is read properly.
def check(fingers_1):
    for i in range(len(fingers_1)):
        if fingers_1[i].tip_position.magnitude == 0:
            print "Finger not detected."
            exit()
            # del fingers_1[i]


# The actual function which takes the input.
def take_input(label,calib):
    print "Taking input."
    file_dataset = open(str(label) + '.txt','a')
    file_temp = open('temp_dataset.txt','a')
    file_dataset.write(str(label) + " ")
    file_temp.write(str(label) + " ")
    controller = Leap.Controller()
    count = 0
    last_frame = 0
    while  count < 100:
        frame = controller.frame()
        if frame.id != last_frame:
            print ".",
            last_frame = frame.id
            fingers_1 = []
            for index_type in range(0,5): #Sort the fingers from thumb to pinky.
                fingers_1.append(frame.fingers.finger_type(index_type)[0])
            check(fingers_1)
            hands = frame.hands
            palm_center = hands[0].palm_position
            for i in range(0,5):
                finger = fingers_1[i]
                for i in range(0,4):
                    bone = finger.bone(i)
                    dist_bone = palm_center.distance_to(bone.next_joint) # Distance of all bones to the palm centre.
                    file_dataset.write(str(dist_bone / calib) + " ")

            thumb = fingers_1[0].tip_position

            for i in range(1,5):
                dist = thumb.distance_to(fingers_1[i].tip_position) # Distance of thumb to all the finger tips.
                file_dataset.write(str(dist / calib) + " ")
            count = count + 1
    file_dataset.write("\n")
    print "\nDone."
    file_dataset.close()
    file_temp.write("\n")
    file_temp.close()


# Wait till the hand starts moving.
# Looping function to wait after the user performs the gesture.
def not_moving():
    controller = Leap.Controller()
    while not controller.is_connected:
        pass
    print "Waiting until hand is moving."
    fingers = []
    while not fingers:  # Keep waiting for the fingers to be detected.
        frame = controller.frame()
        fingers = frame.fingers
        pass
    #print "Fingers detected."
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
                    print "Moving.Going back to main."
                    return


# Function used to normalize all the finger lengths across people.
def calibrate():
    print "Calibrating hand. Please hold it steady."
    moving()
    controller = Leap.Controller()
    frame = controller.frame()
    hands = frame.hands
    fingers = frame.fingers
    for finger in fingers:
        if finger.type == 2:
            middle_finger = finger
            break

    last_frame = 0
    palm_center = hands[0].palm_position
    calib = palm_center.distance_to(middle_finger.tip_position)
    # Using the distance of the middle finger tip to the palm centre as
    # the constant among people.
    print "Calibrating done. Please remove your hand."

    while controller.is_connected:
        frame = controller.frame()
        if frame.id != last_frame:
            last_frame = frame.id
            hands = frame.hands
            if not hands:
                return calib


main()





