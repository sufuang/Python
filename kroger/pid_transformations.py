# Databricks notebook source
spark.conf.set("fs.azure.account.auth.type.mxcoredataprodstrg.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.mxcoredataprodstrg.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.mxcoredataprodstrg.dfs.core.windows.net", "18cc7074-141f-48e3-8704-3fbdb42ea7b7")
spark.conf.set("fs.azure.account.oauth2.client.secret.mxcoredataprodstrg.dfs.core.windows.net", dbutils.secrets.get(scope = "MXI-Core-Data-PROD-DBX-SCOPE", key = "merch-mxi-prod-dmp-password"))
spark.conf.set("fs.azure.account.oauth2.client.endpoint.mxcoredataprodstrg.dfs.core.windows.net", "https://login.microsoftonline.com/8331e14a-9134-4288-bf5a-5e2c8412f074/oauth2/token")

# COMMAND ----------

import pyspark.sql.functions as f
from pyspark.sql import Window
from datetime import datetime, timedelta, date
from pyspark.sql.types import *
import unicodedata
import re

def get_data(query):
    '''
    Takes query, a string representing a Spark SQL query, and returns the resulting dataframe
    '''
    df = spark.sql(query)
    return df

def get_gtin(gtin_list, gtin_type):
    '''
    Iterates through list of dictionaries gtin_list with keys "type" and "value"
    Returns the value of "value" when "type" value matches the string gtin_type
    '''
    for gtin in gtin_list:
        if gtin.type == gtin_type:
            return gtin.value
    return None

def get_legacy(legacy_list, attribute_name):
    '''
    Returns None if legacy_list is not iterable
    Iterates through list of dictionaries legacy_list with keys "legacyAttributeName" and "legacyAttributeValue"
    Returns the value of "legacyAttributeValue" when "legacyAttributeType" value matches the string attribute_name
    '''
    if not hasattr(legacy_list, '__iter__'):
        return None
    for attribute in legacy_list:
        if attribute.legacyAttributeName == attribute_name:
            return attribute.legacyAttributeValue
    return None

def normalize(string):
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def clean(string):
    string = string.upper()

    string = normalize(string)

    string = re.sub(r"[^A-Z0-9\s#&/$\.\(\)\-%]", '', string)

    return string

def previous_data(filepath):
    '''
    Reads parquet data from filepath
    '''
    df = spark.read.format('delta').parquet(filepath)
    return df

def cols_to_concat(col_list, spaces_between):
    '''
    Takes a list of strings col_list and an integer spaces_between
    Returns a list alternating between column names and pyspark Columns of literal value ' ' * spaces_between
    Example output: ['upc', f.lit(' '), 'description', f.lit(' '), 'department', f.lit(' '), 'commodity', f.lit(' '), 'subcom', f.lit(' '), 'upc_type']
    '''
    to_concat = []
    for col in col_list:
        to_concat.append(col)
        to_concat.append(f.lit(' ' * spaces_between))
    to_concat.pop()
    return to_concat

def format_text(df, schema, spaces_between):
    '''
    Takes a dataframe df, a dictionary schema in the format {col_name: n_spaces} and an integer spaces_between
    Changes each column to take up n_spaces, padding with spaces on the right if it's too short
    Returns a dataframe with one column 'text' that concatenates each column from the previous dataframe, adding 
    spaces_between spaces between each column's value
    '''
    for col in schema.keys():
        df = df.withColumn(col, f.rpad(f.col(col), schema[col], ' '))

    concat_list = cols_to_concat(schema.keys(), spaces_between)

    df = df.select(f.concat(*concat_list).alias('text'))
    return df

def data_diff(df, path):
    '''
    Finds the difference between the current dataframe df and the previous dataframe that is stored at the filepath path
    '''
    previous = previous_data(path)
    previous_upcs = set(row.__getitem__('markdown_upc') for row in previous.collect())
    diff = df.filter(f.col('markdown_upc').isin(previous_upcs) == False)
    return diff

def delta_data(df,df_path):
    df_Final=spark.read.parquet(df_path)
    df_Final=df_Final.drop("ETL_LOAD_DATE","LOAD_DATETIME")
    df_Final=df.exceptAll(df_Final)
    if df_Final.count()==0:
        print("No New Records as of now")  
    else:
        df_Final=df_Final.withColumn("ETL_LOAD_DATE", f.current_date()).withColumn("LOAD_DATETIME", f.current_timestamp())
        df_Final.write.mode('append').parquet(df_path)
        
        
def write_txt_file(df, path):
    df.coalesce(1).write.mode('overwrite').option('linesep', '\n').format('delta').text(path)
    
    actual_text_file = [file.path for file in dbutils.fs.ls(path) if file.path[-3:] == 'txt'][0]
    
    dbutils.fs.cp(actual_text_file, path + '.txt')
    
def update_data(directory, query, filename, schema, spaces, return_df=False, write=True):
    '''
    directory: (string) Path where the data is stored (string)
    query: (string) Spark SQL query for the relevant data (string)
    filename: (string) Name of parquet file to be written for main df. Text df will write a text file with filename + the current date
    schema: (dictionary) Schema which specifies number of spaces each field should occupy in the text df (e.g. [{field_name}: n_spaces])
    spaces: (integer) Number of spaces between each field in the text df and text file
    return_df: (boolean) If True, returns a df and does not calculate a diff for nielsen (for testing purposes)
    '''
    df_path = directory + f'{filename}/{filename}.parquet'

    df = get_data(query)

    df = transform(df)

    text_df = format_text(df, schema, spaces)

    text_path = directory + f'{filename}/{filename}' + str(date.today())

    if write:
        write_txt_file(text_df, text_path)
        delta_data(df,df_path)

    if return_df:
        return df, text_df

# COMMAND ----------

directory = 'abfss://mx-core-data-prod-pid-container@mxcoredataprodstrg.dfs.core.windows.net/'
