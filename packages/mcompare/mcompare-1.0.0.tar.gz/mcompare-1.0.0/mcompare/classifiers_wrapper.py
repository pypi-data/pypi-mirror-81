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
#from catboost import CatBoostClassifier, Pool, cv - note used
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.base import BaseEstimator, TransformerMixin
# metrics
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, plot_confusion_matrix
from sklearn.metrics import roc_auc_score, roc_curve, precision_score, recall_score, f1_score 
from sklearn.metrics import classification_report
# sampling
from imblearn import under_sampling, over_sampling
from imblearn.over_sampling import SMOTE

class ClassificationModelData(model_wrapper.ModelData):
    def __init__(
        self, 
        x, y, x_train, x_test, y_train, y_test, 
        model, model_label_name, 
        column_names, class_names, 
        is_multi_classification=False
    ):
        ''' Create a model object to capture model information regarding the classification model.
        
        Params:
            - x (DataFrame) : The X dataset (independent variables)
            - y (array) : The label (dependent variable)
            - x_train (DataFrame) : The training split set from our X dataset
            - x_test (DataFrame) : The test split set from our X dataset
            - y_train (array) : The training split set from our y dataset
            - y_test (array) : The test split set from our y dataset
            - model (SKLearn Model) : The SKLearn fitted model
            - model_label_name (string) : Label - the same as the pipeline reference name
            - is_catboost (bool) : indicator for if it is a catboost model
            - class_names : the names of the classes
        '''
        super().__init__(x, y, x_train, x_test, y_train, y_test)
        self.name = model_label_name
        self.model = model
        self.column_names = column_names
        self.class_names = class_names
        if is_multi_classification is not True:
            self.calculate_metrics(self.get_predictions(self.x_test), self.x_test, self.y_test)
        else:
            self.calculate_metrics_multiclassification(self.get_predictions(self.x_test), self.x_test, self.y_test)

    def get_predictions(self, x):
        '''Returns predictions from our fitted model'''
        model = self.model
        return model.predict(x)

    def calculate_metrics(self, predictions, x, y, set_metrics=True):
        '''Calculate metrics associated with model & visualise them
        
        Parameters:
            - predictions : The predictions from the model
            - y_test : the y_test set to use to build metrics from
        '''
        #make predictions
        conf_matrix = confusion_matrix(y, predictions)
        accuracy = np.round(accuracy_score(y, predictions),2)
        precision = np.round(precision_score(y, predictions),2)
        recall = np.round(recall_score(y, predictions),2)
        auc = np.round(roc_auc_score(y, predictions),4)
        f1 = np.round(f1_score(y, predictions, average='weighted'),4)
        if set_metrics:
            self.set_metrics(conf_matrix, accuracy, precision, recall, auc, f1)
        self.print_metrics_pretty(x, y, conf_matrix, accuracy, precision, recall, auc, f1)



    def calculate_metrics_multiclassification(self, predictions, x, y, set_metrics=True):
        self.conf_matrix = confusion_matrix(y, predictions, self.class_names)
        self.get_confusion_matrix_plot(x, y, 'vertical')
        print(classification_report(y, predictions, digits=len(self.class_names)))

    def set_metrics(self, conf_matrix, accuracy, precision, recall, auc, f1):
        self.conf_matrix = conf_matrix
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.auc = auc
        self.f1 = f1
    
    def get_metrics(self):
        return self.conf_matrix, self.accuracy, self.precision, self.recall, self.auc, self.f1
    
    def print_metrics_pretty(self, x, y, conf_matrix, accuracy, precision, recall, auc, f1):
        '''prints metrics to screen'''
        print(f'Metrics for: {self.name}.')
        self.print_header('Metrics:')
        print(f'Accuracy: {accuracy*100}%')
        print(f'Precision: {precision*100}%')
        print(f'Recall: {recall*100}%')
        print(f'AUC: {auc}')
        print(f'F1 Score (weighted): {f1}')
        self.print_header('Confusion Matrix:')
        self.get_confusion_matrix_plot(x, y)

    def print_cross_validation_pretty(self):
        print('Scores: ', self.evaluation_scores)
        print('Mean of Scores: ', np.round(self.evaluation_scores.mean(), 2))
        print('Standard Deviation of Scores: ', np.round(self.evaluation_scores.std(), 2))

    def get_confusion_matrix_plot(self, x, y, xticks_rotation_val='horizontal'):
        '''This prints a visual Confusion Matrix to screen'''
        self.confusion_matrix_plot = plot_confusion_matrix(
            self.model, 
            x, 
            y,
            display_labels=self.class_names,
            cmap=plt.cm.Blues,
            normalize=None,
            xticks_rotation=xticks_rotation_val
        )
        self.confusion_matrix_plot.ax_.set_title('Confusion Matrix')
        #print(self.confusion_matrix_plot.confusion_matrix)
        
    def get_cross_validation_scores(self, scoring_metric, cv_folds, print_pretty=False):
        '''This method returns the cross validation scores'''
        model = self.model
        evaluation_scores = cross_val_score(
            estimator= model,
            X= self.x, 
            y= self.y,
            scoring= scoring_metric,
            cv=cv_folds
        )
        self.evaluation_scores = np.round(evaluation_scores,2)
        if print_pretty == True:
            self.print_cross_validation_pretty()
    
    def set_cv_prediction_results(self, cv_folds):
        '''This sets the prediction
        '''
        self.cv_predictions = self.get_cross_validation_predictions(cv_folds)
        self.calculate_metrics(self.cv_predictions, self.x, self.y, set_metrics=False)

    def get_cross_validation_predictions(self, cv_folds):
        '''This method returns the predictions from cross validation
        
        Parameters:
            - cv_folds (int) : no of folds used in Cross Validation
            
        Returns:
            - predictions (list[<integers>]) : returns a list of integer predictions (class)
        '''
        model = self.model
        predictions = cross_val_predict(
            estimator= model,
            X= self.x, 
            y= self.y,
            cv=cv_folds
        )
        return predictions

    def print_header(self, header):
        print()
        print('*'*20)
        print(f'{header}', )
        print('*'*20,)

    @staticmethod
    def calculate_tpr_fpr(model, x, y):
        # calculate probability
        preds_proba = model.predict_proba(x)
        # extract probability
        preds = preds_proba[:, 1]
        # work out fpr, tpr
        _fpr, _tpr, _ = roc_curve(y, preds)
        return _fpr, _tpr

    @staticmethod
    def plot_models_auc_combined(list_of_models):
        ''' Plot AUC for models combined
        '''

        for single_model in list_of_models:
            print(f'{single_model.name}: {single_model.auc}')
        
        plt.rcParams['figure.figsize'] = 10, 10
        
        y_test = list_of_models[0].y_test
        
        # work out random fpr, tpr
        ns_probs = [0 for _ in range(len(y_test))]
        ns_auc = roc_auc_score(y_test, ns_probs)
        ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
        
        print('\nPlotting charts...')
        
        # plot the roc curve for random line
        plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No model')

        for single_model in list_of_models:
            print(f'Plotting for: {single_model.name}...')
            _fpr, _tpr = ClassificationModelData.calculate_tpr_fpr(single_model.model, single_model.x_test, single_model.y_test)
            plt.plot(_fpr, _tpr, label = f'{single_model.name}')

        # axis labels
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC AUC chart')
        # show the legend
        plt.legend()
        # show the plot
        plt.show()