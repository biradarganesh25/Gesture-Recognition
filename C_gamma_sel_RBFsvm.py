import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib

# Used to calculate the best gamma and C values for Gaussian SVC model.
# Used GridSearchCV to calculate the best values for the parameters
# and the best accuracy possible using these parameters.

train_data = np.genfromtxt('training_selected_random.txt')
test_data = np.genfromtxt('testing_selected_random.txt')
X_train = train_data[:,1:]
y_train = train_data[:,0]
X_test = test_data[:,1:]
y_test = test_data[:,0]
X = np.concatenate((X_train,X_test),axis = 0)
y = np.concatenate((y_train,y_test),axis = 0)

C_range = np.logspace(-2, 10, 13)
gamma_range = np.logspace(-9, 3, 13)
param_grid = dict(gamma=gamma_range, C=C_range)
cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
grid = GridSearchCV(SVC(), refit=True,param_grid=param_grid, cv=cv)
grid.fit(X, y)
joblib.dump(grid,'RBFSVC_model.pkl')


print("The best parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))
