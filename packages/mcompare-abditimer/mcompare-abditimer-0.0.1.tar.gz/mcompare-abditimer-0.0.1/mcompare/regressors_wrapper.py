# --------------------------------------------------------------    
# Helper Function python script
# -------------------------------------------------------------- 
from . import model_wrapper
# general python packages
import pandas as pd
import numpy as np
# for visualisations
import matplotlib.pyplot as plt
import seaborn as sns
# for data engineering work
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, learning_curve
from sklearn.preprocessing import LabelEncoder
from math import sqrt
# models
# from catboost import CatBoostClassifier, Pool, cv - not used
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.base import BaseEstimator, TransformerMixin
# metrics
from sklearn.metrics import mean_squared_log_error,mean_squared_error, r2_score,mean_absolute_error
from sklearn.metrics import classification_report
# sampling
from imblearn import under_sampling, over_sampling
from imblearn.over_sampling import SMOTE

class RegressionModelData(model_wrapper.ModelData):
    def __init__(self, x, y, x_train, x_test, y_train, y_test, model, model_label_name, column_names):
        ''' Create a model object to capture all model info.
        
        Params:
            - X (DataFrame) : The X dataset (independent variables)
            - y (array) : The label (dependent variable)
            - X_train (DataFrame) : The training split set from our X dataset
            - X_test (DataFrame) : The test split set from our X dataset
            - y_train (array) : The training split set from our y dataset
            - y_test (array) : The test split set from our y dataset
            - model (SKLearn Model) : The SKLearn fitted model
            - model_label_name (string) : Label - the same as the pipeline reference name
        
        Methods:
            - set_metrics_regression : This is called when the object is instantiated and sets the metrics.
            - get_metrics_regression : This returns the metric values
            
        '''
        super().__init__(x, y, x_train, x_test, y_train, y_test)
        self.name = model_label_name
        self.model = model
        self.column_names = column_names
        self.set_metrics_regression()
        
    def set_metrics_regression(self):
        '''Store metrics for a regression model.'''
        model = self.model
        self.predicted = model.predict(self.x_test)
        self.mse = mean_squared_error(self.y_test, self.predicted)
        self.mape = np.mean(np.abs((self.y_test - self.predicted) / self.y_test)) * 100
        self.print_metrics_regression()
        
    def get_metrics_regression(self):
        '''Returns regression metrics.'''
        return self.mse, sqrt(self.mse), round(self.mape,2)
    
    def get_rmse(self):
        return round(sqrt(self.mse),2)
    
    def get_cross_validation(self, scoring_metric, cv_folds):
        '''This method returns the cross validation scores'''
        model = self.model
        evaluation_scores = cross_val_score(
            estimator= model,
            X= self.x, 
            y= self.y,
            scoring= scoring_metric,
            cv=cv_folds
        )
        if scoring_metric == 'neg_mean_squared_error':
            rmse_evaluation_scores = np.round(np.sqrt(-evaluation_scores),2)
            print('Scores: ', np.round(rmse_evaluation_scores))
            print('Mean of Scores: ', np.round(rmse_evaluation_scores.mean()))
            print('Standard Deviation of Scores: ', np.round(rmse_evaluation_scores.std()))
        return evaluation_scores

    def print_metrics_regression(self, rounding=2):
        '''prints regression metrics.'''
        print(f'Mean squared error: {np.round(self.mse,rounding)}')
        print(f'Root mean squared error:{np.round(sqrt(self.mse), rounding)}')
        print(f'MAPE: {np.round(self.mape,rounding)}%')
    
    def plot_learning_curves(self, step_size=500):
        '''This plots a learning curve based on our model. This plots the models performance
        on the training set and the validation set - depending on a function of the training
        sets size.

        Hence, the model is trained multiple times on different sized subsets of the training data.

        Params:
            - step_size (int):
                This is the iteration step size the model will build for 
                (e.g. if = 500, it will build models using 500 rows at a time.)

        Returns:
            matplotlib chart - which is plotted to screen.
        '''
        model = self.model
        #X_tr, X_vl, y_tr, y_vl = train_test_split(self.x, self.y, test_size=0.2)
        train_errors = []
        validation_errors = []
        
        # loop over all rows in our data
        for ith_step_size in range(1, len(self.x_train)):
            # if the count of rows is within our step size
            if ith_step_size % step_size == 0:
                # fit our model to our current dataset size
                temp_xtrain = self.x_train[:ith_step_size].copy()
                temp_xtest = self.x_test.copy()
                temp_ytrain = self.y_train[:ith_step_size]
                temp_ytest = self.y_test
                model.fit(temp_xtrain, temp_ytrain)
                # make predictions on our training set and test set
                y_train_predict = model.predict(temp_xtrain)
                y_val_predict = model.predict(temp_xtest)
                # add it to our lists
                train_errors.append(mean_squared_error(temp_ytrain, y_train_predict))
                validation_errors.append(mean_squared_error(temp_ytest, y_val_predict))
        # plot our charts
        plt.plot(np.sqrt(train_errors), 'r-+', linewidth=2, label='train')
        plt.plot(np.sqrt(validation_errors), 'b-', linewidth=3, label='val')
        plt.legend(loc='upper right', fontsize=14)   
        plt.xlabel(f'Training set size (every {step_size})', fontsize=14) 
        plt.ylabel('RMSE', fontsize=14) 
        plt.title(f'Learning Curve for {self.name}')    
        
    def plt_learning_curve(self):
        train_sizes = [1, 100, 1000, 5000, 10000, 15000, 22712]
        train_sizes, train_scores, validation_scores = learning_curve(
            estimator = self.model,
            X = self.x,
            y = self.y, 
            train_sizes = train_sizes, 
            cv = 5,
            scoring = 'neg_mean_squared_error'
        )
        train_scores_mean = -train_scores.mean(axis = 1)
        validation_scores_mean = -validation_scores.mean(axis = 1)
        plt.style.use('seaborn')
        plt.plot(train_sizes, train_scores_mean, label = 'Training error')
        plt.plot(train_sizes, validation_scores_mean, label = 'Validation error')
        plt.ylabel('MSE', fontsize = 14)
        plt.xlabel('Training set size', fontsize = 14)
        plt.title('Learning curves for a linear regression model', fontsize = 18, y = 1.03)
        plt.legend()
        plt.ylim(0,40)