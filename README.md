# Gesture-Recognition

A simple Gaussian SVC model which can predict ten ASL digits 1-10 which is taken from the user with the
help of LMC(Leap Motion Controller). All the text files contain the dataset created. Very few examples were
used (Only about 20 per gesture), but the algorithm performed reasonably well with an accuracy of around 84%.

The main challenge was creating the dataset. Scikit-learn was used extensively throughout the project.

For each training example, the features were taken for 100 frames for a particular gesture. Per frame, the
distance of all the bone joints from the palm centre and the distance of the thumb from all the finger tips were used.
That means 20 features from bone joints in all the finger tips, and 4 more for distance between each finger and thumb,
per frame. So, 24 feature x 100 frames i.e total of 2400 features per example were used.

Overfitting was a major problem with this large number of examples. It would have been mitigated with more examples.
Future work could be running PCA on the dataset and then select only the major and important features for
classification.

LeapSDK needs to be downloaded and put in some folder. The path to this folder must be specified in the get_input.py
function which does the prediction.

The main collaborators for this project were: [Ganesh Biradar](https://github.com/biradarganesh25), [Aravind Varier](https://github.com/aravindvarier)
