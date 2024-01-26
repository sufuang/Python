# Databricks notebook source
dbutils.widgets.text(name='filepath',defaultValue='',label='Enter file path')
filepath=dbutils.widgets.get("filepath")
dbutils.widgets.dropdown("mode","append",["append","overwrite"])
mode=dbutils.widgets.get("mode")
dbutils.widgets.dropdown("bol_value","true",["true","false"])
bol_value=dbutils.widgets.get("bol_value")


# COMMAND ----------

# MAGIC %md
# MAGIC ######Below utility commands is used for writing custom logs in /tmp/ folder,as the purpose of writing the logs in tmp folder is ,we can append to the existing logs file,for a particular session,so until the cluster is shutdown we can write the logs to the same filename.

# COMMAND ----------

import logging
import time
import datetime
file_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

NOTEBOOK_NAME=dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get().split("/")

p_dir = '/tmp/'

p_filename = 'custom_log'+file_date+'.log'
p_logfile = p_dir + p_filename 

print(p_logfile)
my_logger = logging.getLogger(f"{file_date}")
my_logger.setLevel(logging.INFO) 

fh = logging.FileHandler(p_logfile,mode='a+')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
if (my_logger.hasHandlers()):
     my_logger.handlers.clear()
my_logger.addHandler(fh)

def sLog(level,message):
    if level == 0:
        my_logger.debug(f'Message: {message}')
    elif level == 1:
        my_logger.info(f'Message: {message}')
    elif level == 2:
        my_logger.warn(f'Message: {message}')
    elif level == 3:
        my_logger.error(f'Message: {message}')
    elif level == 4:
        my_logger.fatal(f'Message: {message}')
    else:
        my_logger.debug(f'Message: {message}')

# COMMAND ----------

# MAGIC %md
# MAGIC #to have connection to dev storage

# COMMAND ----------

# MAGIC %md
# MAGIC ######Below Utility commands is used to read a dataframe as a parquet file,and also write the dataframe as a parquet file in mxcoredataprodstrg storage account

# COMMAND ----------

def read_parquet(file):
   df1 = spark.read.option("header", bol_value).option('inferschema',bol_value).parquet(file)

#Display(df1)
   print('spark Dataframe is created:df1')
   return df1
def write_parquet(df,file):
    df.write.mode(mode).parquet(file)
    print('spark Dataframe is Written:df')

# COMMAND ----------

# MAGIC %md
# MAGIC ##Databricks Utilities
# MAGIC  .File System <br>
# MAGIC  .Workflow<br>
# MAGIC  .Widget<br>
# MAGIC  .Secrets<br>
# MAGIC  .Library

# COMMAND ----------

# MAGIC %md 
# MAGIC ### File System

# COMMAND ----------

dbutils.fs.help()

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.fs.mkdirs("/Test")
# MAGIC This command is used to create a new directory Test in dbfs.

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.fs.ls("/Test")
# MAGIC This command is used to list all the files in Test directory.

# COMMAND ----------

# MAGIC %md
# MAGIC ######display(dbutils.fs.ls("/Test"))
# MAGIC This command is used to display all the files in the Test directory in tabular format..

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.fs.mkdirs("/Test/new")
# MAGIC This commands is used to create a new directory new in the parent directory Test,or create both if not exist.

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.fs.put("/Test/new.txt","Demo txt")
# MAGIC This Command is used to write the text to the file new.txt<br>

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.fs.head("/Test/new.txt")
# MAGIC This Command is used to read the content of the file new.txt

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ######dbutils.fs.mv("/Test/new.txt","/Test/new")
# MAGIC This command is used to move the files from new.txt from /test/ to /test/new.<br>

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ######dbutils.fs.cp("/Test/new.txt","/Test/new")
# MAGIC This command is used to copy the files from new.txt from /test/ to /test/new.

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.fs.rm("/Test/new/new.txt")<br>
# MAGIC This Command is used to remove the file new.txt from the Test directory

# COMMAND ----------

# MAGIC %md 
# MAGIC ###Notebook Widgets

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.widgets.text(name='filepath',defaultValue='',label='Enter file path')
# MAGIC This command is used to create a widget text with name filepath and defaultvalue empty,and with label as given.

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.widgets.get("filepath")
# MAGIC This command is used to get the value of widget with name filepath.

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.widgets.removeAll()
# MAGIC This command is used to remove all the widgets from the notebook.

# COMMAND ----------

dbutils.widgets.help()

# COMMAND ----------

# MAGIC %md
# MAGIC ##Notebook Workflow

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.notebook.run('/Users/adarsh.singh@kroger.com/bcg_utils',timeout_seconds=50)
# MAGIC This command is used to run the Notebook bcg_utils with a timeout of 50 seconds.

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.notebook.run('/Users/adarsh.singh@kroger.com/Utility',120,{'filepath':''})
# MAGIC This command is used to run the notebook Utility from other notebook,and also pass the value to the parameter to the widget name filename.

# COMMAND ----------

dbutils.notebook.help()

# COMMAND ----------

# MAGIC %md
# MAGIC ###Library

# COMMAND ----------

# MAGIC %md
# MAGIC ######dbutils.library.installPyPI("sympy")<br>
# MAGIC This command is used to instal the module sympy.Then we can import the module and use it in the program.

# COMMAND ----------

#dbutils.library.help()
#not working

# COMMAND ----------

# MAGIC %md
# MAGIC ###Secrets

# COMMAND ----------

# MAGIC %md
# MAGIC ######Below commands is used to list all the available scope.

# COMMAND ----------

dbutils.secrets.listScopes()

# COMMAND ----------

# MAGIC %md
# MAGIC ######Below command is used to get all the keys associated with the given scope.

# COMMAND ----------

dbutils.secrets.list("MXI-Core-Data-DEV-DBX-SCOPE")

# COMMAND ----------

# MAGIC %md
# MAGIC ######Below command is used to get the secrets value of the given key by using the given scope.

# COMMAND ----------

value=dbutils.secrets.get(scope="MXI-Core-Data-DEV-DBX-SCOPE",key="STORAGE-GEN2-PRIMARY-DFS-ENDPOINT")
for char in value:
    print(char,end=" ")

# COMMAND ----------

dbutils.secrets.help()

# COMMAND ----------

# MAGIC %md
# MAGIC Below is the function defined for flatenning array of structs  and structs also if StructType then convert all sub element to columns, if ArrayType then add the Array Elements as Rows using the explode function

# COMMAND ----------

from datetime import date
from pyspark.sql.types import *
from pyspark.sql.functions import *
#Flatten array of structs and structs
def flatten(df):
   # compute Complex Fields (Lists and Structs) in Schema   
   complex_fields = dict([(field.name, field.dataType)
                             for field in df.schema.fields
                             if type(field.dataType) == ArrayType or  type(field.dataType) == StructType])
   while len(complex_fields)!=0:
      col_name=list(complex_fields.keys())[0]
      print ("Processing :"+col_name+" Type : "+str(type(complex_fields[col_name])))
    
      # if StructType then convert all sub element to columns.
      # i.e. flatten structs
      if (type(complex_fields[col_name]) == StructType):
         expanded = [col(col_name+'.'+k).alias(col_name+'_'+k) for k in [ n.name for n in  complex_fields[col_name]]]
         df=df.select("*", *expanded).drop(col_name)
    
      # if ArrayType then add the Array Elements as Rows using the explode function
      # i.e. explode Arrays
      elif (type(complex_fields[col_name]) == ArrayType):    
         df=df.withColumn(col_name,explode_outer(col_name))
    
      # recompute remaining Complex Fields in Schema       
      complex_fields = dict([(field.name, field.dataType)
                             for field in df.schema.fields
                             if type(field.dataType) == ArrayType or  type(field.dataType) == StructType])
   return df

