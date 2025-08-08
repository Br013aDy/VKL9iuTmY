# 代码生成时间: 2025-08-08 12:46:56
import pandas as pd
from celery import Celery
from celery import shared_task

"""
Data Cleaning and Preprocessing Toolbox
This module provides a set of functions for data cleaning and preprocessing,
including handling missing values, normalizing data, and encoding categorical variables.
"""

# Define a Celery app instance
app = Celery('data_cleaning_toolbox')
app.config_from_object('your_celery_config')

@shared_task(bind=True)
def clean_missing_values(self, data):
    """
    Handle missing values in the dataset.
    Replace missing values with the mean of the column.
    
    Parameters:
    data (pd.DataFrame): The DataFrame to clean.
    
    Returns:
    pd.DataFrame: The cleaned DataFrame.
    
    Raises:
    Exception: If data is not a pandas DataFrame.
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise ValueError('Input data must be a pandas DataFrame')
        data.fillna(data.mean(), inplace=True)
        return data
    except Exception as e:
        self.retry(exc=e)

@shared_task(bind=True)
def normalize_data(self, data):
    """
    Normalize the data in the dataset.
    Use min-max scaling to normalize the numerical features.
    
    Parameters:
    data (pd.DataFrame): The DataFrame to normalize.
    
    Returns:
    pd.DataFrame: The normalized DataFrame.
    
    Raises:
    Exception: If data is not a pandas DataFrame.
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise ValueError('Input data must be a pandas DataFrame')
        data_normalized = (data - data.min()) / (data.max() - data.min())
        return data_normalized
    except Exception as e:
        self.retry(exc=e)

@shared_task(bind=True)
def encode_categorical_variables(self, data):
    """
    Encode categorical variables in the dataset.
    Use one-hot encoding for categorical features.
    
    Parameters:
    data (pd.DataFrame): The DataFrame to encode.
    
    Returns:
    pd.DataFrame: The encoded DataFrame.
    
    Raises:
    Exception: If data is not a pandas DataFrame.
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise ValueError('Input data must be a pandas DataFrame')
        data_encoded = pd.get_dummies(data, drop_first=True)
        return data_encoded
    except Exception as e:
        self.retry(exc=e)
