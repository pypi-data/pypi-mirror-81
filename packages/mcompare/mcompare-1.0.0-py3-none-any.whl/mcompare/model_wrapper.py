# --------------------------------------------------------------    
# Helper Function python script
# -------------------------------------------------------------- 
# general python packages
import pandas as pd
import numpy as np

__VERSION__ = '0.0.1'
__CREATOR__ = 'Abdi_Timer'

# --------------------------------------------------------------    
# generic Modeling helper functions
# --------------------------------------------------------------  
class ModelData(object):
    '''This class captures the data used to build models.
    '''
    def __init__(self, x, y, x_train, x_test, y_train, y_test):
        '''
         Params:
                - x (DataFrame) : The X dataset (independent variables)
                - y (array) : The label (dependent variable)
                - x_train (DataFrame) : The training split set from our X dataset
                - x_test (DataFrame) : The test split set from our X dataset
                - y_train (array) : The training split set from our y dataset
                - y_test (array) : The test split set from our y dataset
        '''
        self.x = x
        self.y = y
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
    
    @staticmethod
    def get_models_by_metric(models, metric_name, is_regression):
        if is_regression:
            model_df = pd.DataFrame([single_model.name, single_model.get_rmse()] for single_model in models)
        else:
            model_df = pd.DataFrame([single_model.name, single_model.auc] for single_model in models)
        metric_name = f'Model_{metric_name}'
        model_df.columns = ['Model_Name', metric_name]
        return model_df
    
    @staticmethod
    def get_pipeline_columns(model, x_train, cols_to_encode, is_custom=False, is_std=False):
        '''
        This returns the columns for the new transformed dataset

        Assumption:
            - The last step before we fit our model in the pipeline, is a DateExtractor object
            - DateExtractor step is defined in pipeline as: 'date-extractor-step'
            - Encoding step is defined in pipeline as: 'ohe-step'
            
        Parameters:
            model: Fitted model
            x_train: X dataset used to train model
            cols_to_encode: columns used for encoding
        '''
        if is_custom is False:
            # get columns from date-extractor - this should always be run
            original_columns_list_new = model.named_steps['date-extractor-step'].get_all_column_names()
        else:
            original_columns_list_new = x_train.columns.tolist()

        # TODO: refactor the below
        if is_custom is True:
            # get encoded columns - if this has been run
            date_extr_list_new = model.named_steps['ohe-step'].transformers_[0][1].get_all_column_names().tolist()
            ohe_columns_list_new = model.named_steps['ohe-step'].transformers_[1][1].get_feature_names(cols_to_encode).tolist()
            # determine difference
            remaining_columns_new = [col_name for col_name in original_columns_list_new if col_name not in cols_to_encode and col_name not in ['Creation_Date', 'DOB']]
            #combine
            transformed_columns_labels_new = date_extr_list_new + ohe_columns_list_new + remaining_columns_new
        elif is_std is False:
            # get encoded columns - if this has been run
            ohe_columns_list_new = model.named_steps['ohe-step'].transformers_[0][1].get_feature_names(cols_to_encode).tolist()
            # determine difference
            remaining_columns_new = [col_name for col_name in original_columns_list_new if col_name not in cols_to_encode]
            #combine
            transformed_columns_labels_new = ohe_columns_list_new + remaining_columns_new
        else:
            # get encoded columns - if this has been run
            std_columns_list_new = x_train.select_dtypes(include=[np.float]).columns.tolist()
            # get encoded columns - if this has been run
            ohe_columns_list_new = model.named_steps['ohe-step'].transformers_[1][1].get_feature_names(cols_to_encode).tolist()
            # determine difference
            remaining_columns_new = [i for i in original_columns_list_new if i not in cols_to_encode and i not in std_columns_list_new]
            #combine
            transformed_columns_labels_new = std_columns_list_new + ohe_columns_list_new + remaining_columns_new
        return transformed_columns_labels_new


        
