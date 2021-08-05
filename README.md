# Gesture-Recognition

The aim of the project was to build a ML model that can convert ASL gestures to spoken English. We managed to recognize the first 10 digits of ASL with an accuracy of around 91%. We made the dataset manually using LMC(Leap Motion Controller). It is an optical hand tracking module that can capture the movement of hand accurately. The dataset contains around 20 samples per gesture (the features of each sample are explained below). A Gaussian SVC model was trained on this dataset, which was used to predicting the gestures. 

The main challenge was creating the dataset. Scikit-learn was used extensively throughout the project.

For each training example, the features were taken for 100 frames for a particular gesture. Per frame, the
distance of all the bone joints from the palm centre and the distance of the thumb from all the finger tips were used.
That means 20 features from bone joints in all the finger tips, and 4 more for distance between each finger and thumb,
per frame. So, 24 feature x 100 frames i.e total of 2400 features per example were used.

Overfitting was a major problem with this large number of features. It would have been mitigated with a much larger dataset. 
Future work could be running PCA on the dataset and then selecting only the major and important features for
classification. 

LeapSDK needs to be downloaded and put in some folder. The path to this folder must be specified in the get_input.py
function which does the prediction.

The main collaborators for this project were: [Ganesh Biradar](https://github.com/biradarganesh25), [Aravind Varier](https://github.com/aravindvarier)
