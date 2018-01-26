import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib

# Used to create the Radial Bias Function(Gaussian SVC)

train_data = np.genfromtxt('training_selected_random.txt')
test_data = np.genfromtxt('testing_selected_random.txt')
X_train = train_data[:,1:]
y_train = train_data[:,0]
X_test = test_data[:,1:]
y_test = test_data[:,0]

svc = SVC()
svc.set_params(gamma = 0.1, C = 0.01)
model = svc.fit(X_train,y_train)
joblib.dump(model,'RBFSVC_model.pkl')

y_predict = model.predict(X_test)
print y_test, y_predict, model.score(X_test,y_test)

