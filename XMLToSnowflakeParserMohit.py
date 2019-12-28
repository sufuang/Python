"""
Module Namer: XMLToSnowflakeParser.py
Author:Mohit Sachdeva 
Date: Dec 2019
"""
import xml.etree.ElementTree as ET
import pandas as pd
from collections import OrderedDict
def parseXML(root,sm):
    sm = sm + "/" + root.tag[root.tag.rfind('}')+1:]
    for child in root:
      parseXML(child,sm)
    if len(list(root)) == 0:
        my_list.append(sm)
def colList():
    """Prepares the list of columns from the XML tags list. This column list will be used for DataFrame creation."""  
    len_max = 0
    for txt in my_list:
        split_tags = txt.split('/')
        len_curr = len(split_tags)
        if len_curr >= len_max:
            len_max = len_curr
        #last3.append(split_tags[-8:])
    print ("max length %d" %len_max)
    for i in range(1, len_max+1):
        col_nm = "column" + str(i)
        cols.append(col_nm)
    print (cols)
    return (len_max)
def splitTags(len_max):
    """Splits the XML path into individual tags and stored in list. This list will be used to populate DataFrame."""
    for txt in my_list:
        split_tags = txt.split('/')
        path_list.append(txt.rsplit('/', 1))
        all_tags.append(split_tags[-len_max:])
        last1.append([split_tags[-1:],len(split_tags)])
        i=1
        strg = '/'
        for s in split_tags[1:len(split_tags)-1]:
            strg = strg + str(i) + "_" + s + "/"
            i = i+1
        sort_path.append(strg)
def renameDupCols(merge_df):
    """Append the pranet XML tag to the duplicate/repeated elements and overcolumn in dataframe"""
    dup_df = merge_df[merge_df.duplicated(['sel_col'],keep=False)]
    i=1
    while not dup_df.empty:
        merge_df = merge_df.join(dup_df['sel_col'],rsuffix='_right')
        for index, row in merge_df.iterrows():
            if row.sel_col == row.sel_col_right:
                cl = "column" + str(row.sel_col_pos - i)
                new_col = row[cl] + "_" + row.sel_col
            else:
                new_col = row.sel_col
            merge_df['sel_col'][index] = new_col
        del merge_df['sel_col_right']
        dup_df = merge_df[merge_df.duplicated(['sel_col'],keep=False)]
        i=i+1
        print(i)
    sel_col_lst = merge_df['sel_col'].tolist()
    for cls in sel_col_lst:
        if cls.count('_') > 1:
            split_cols = cls.split('_')
            col_str = split_cols[0]+"_"+split_cols[-1]
            new_col_lst.append(col_str)
        else:
            new_col_lst.append(cls)
    merge_df['new_sel_col'] = new_col_lst
    return merge_df
def createDDL(merge_df):
    """Prepares DDL statements and writes into the File"""
    ddl = "CREATE OR REPLACE TABLE "+ DB_Nm +"."+ DB_Schema +"."+ Bod_Nm +"_Flat \n(\n  BODNm\t string"
    for index,row in merge_df.iterrows():
        ddl = ddl + "\n  ," + row.new_sel_col + "\t string"
    ddl = ddl + "\n  ,DW_CreateTs\t timestamp\n)\nDATA_RETENTION_TIME_IN_DAYS = "+ str(Rtn_tm) +";"
    with open(Output_Dir+Bod_Nm+"_Flat_DDL.sql", "w") as text_file:
        print("{}".format(ddl), file=text_file)
    text_file.close()
def createDML(merge_df):
    """Prepares DML statements and writes into a File"""
    dml = "INSERT INTO "+ DB_Nm +"."+ DB_Schema +"."+ Bod_Nm +"_Flat \n"+ "SELECT\tBODNm"
    for index,row in merge_df.iterrows():
        dml = dml + "\n\t," + row.new_sel_col
    dml = dml + "\n\t,TO_TIMESTAMP_NTZ(CURRENT_TIMESTAMP) AS DW_CreateTs\nFROM\n\t("
    # Group the dataframe by full XML path for preparing DML
    group_df = merge_df.groupby('sort_path')
    i=1
    m=1
    z=1
    for group_name, df in group_df:
        j=1
        for index, row in df.iterrows():
            cl = "column" + str(row.sel_col_pos - 2)
            if i == 1 and j == 1 and row.column3 == 'DocumentData':
                dml = dml + "\n\t SELECT\t"+ Var_Col +":\"@\"::string AS BODNm"
                dml = dml + "\n\t \t,XMLGET("+ row[cl] +".value,'Abs:"+ row['element'] + "'):\"$\"::string AS " + row.new_sel_col
                m = 0
            elif i == 1 and j == 1:
                dml = dml + "\n\t SELECT\n\t \tXMLGET("+ row[cl] +".value,'Abs:"+ row['element'] + "'):\"$\"::string AS " + row.new_sel_col
            elif j == 1 and row.column3 == 'DocumentData' and m == 1:
                dml = dml + "\nLEFT JOIN\n\t(" + "\n\t SELECT\t" + Var_Col +":\"@\"::string AS BODNm"
                dml = dml + "\n\t \t,XMLGET("+ row[cl] +".value,'Abs:"+ row['element'] + "'):\"$\"::string AS " + row.new_sel_col
                m = 0
            elif j == 1:
                dml = dml + "\nLEFT JOIN\n\t(" + "\n\t SELECT"
                dml = dml + "\n\t \tXMLGET("+ row[cl] +".value,'Abs:"+ row['element'] + "'):\"$\"::string AS " + row.new_sel_col
            else:
                dml = dml + "\n\t \t,XMLGET("+ row[cl] +".value,'Abs:"+ row['element'] + "'):\"$\"::string AS " + row.new_sel_col
            j=j+1
        dml = dml + "\n\t \t," + row['column2'] +".SEQ::integer as SEQ\n\t \t," + row['column2'] + ".index::integer as idx"
        for x in range(1,row.sel_col_pos - 1):
            if x == 1:
                dml = dml + "\n\t FROM\t"+ DB_Nm + "." + DB_Schema + "." + Var_Tbl +" tbl"
            elif x == 2:
                dml = dml + "\n\t \t,LATERAL FLATTEN(tbl." + Var_Col + ":\"$\") "+ row['column2']
            else:
                cl = "column" + str(x)
                cl_prev = "column" + str(x-1)
                dml = dml + "\n\t \t,LATERAL FLATTEN("+ row[cl_prev] + ".value:\"$\") "+ row[cl]
        k=1
        for x in range(1,row.sel_col_pos - 2):
            cl1 = "column" + str(x + 1)
            cl2 = "column" + str(x + 2)
            if k == 1:
                dml = dml + "\n\t WHERE\t"+ row[cl1] +".value like '<"+ row[cl2] +">%'"
            elif k == 2:
                if row.column3 == 'DocumentData':
                    dml = dml + "\n\t AND\t"+ row[cl1] +".value like '<"+ row[cl2] +">%'"
                else:
                    dml = dml + "\n\t AND\t"+ row[cl1] +".value like '<"+ Parent_Tag + row[cl2] +">%'"
            else:
                dml = dml + "\n\t AND\t"+ row[cl1] +".value like '<"+ Child_Tag + row[cl2] +">%'"    
            k=k+1
        cl3 = "column" + str(row.sel_col_pos - 1)
        if i == 1:
            dml = dml + "\n\t) "+ row[cl3]
            join_dict = {row.column3 + str(row.sel_col_pos): row[cl3]
                         ,row.column3 + str(row.sel_col_pos-1): row[cl3]
                        }
            prev_col_pos = row.sel_col_pos
            prev_col3 = row.column3
            first_col_pos = row.sel_col_pos
            first_col3 = row.column3
        else:
            if row.sel_col_pos ==  prev_col_pos and row.column3 == prev_col3:
                dml = dml + "\n\t) "+ row[cl3] + " on " + row[cl3] + ".SEQ = " + join_dict[row.column3 + str(row.sel_col_pos-1)] + ".SEQ AND " + row[cl3] + ".idx = " + join_dict[row.column3 + str(row.sel_col_pos-1)] + ".idx"
            elif row.sel_col_pos ==  prev_col_pos and row.column3 != prev_col3 and z == 1:
                dml = dml + "\n\t) "+ row[cl3] + " on " + row[cl3] + ".SEQ = " + join_dict[first_col3 + str(first_col_pos)] + ".SEQ "
                join_dict[row.column3 + str(row.sel_col_pos)] = row[cl3]
                join_dict[row.column3 + str(row.sel_col_pos-1)] = row[cl3]
                z=0
            elif row.sel_col_pos !=  prev_col_pos and row.column3 != prev_col3 and z == 1:
                dml = dml + "\n\t) "+ row[cl3] + " on " + row[cl3] + ".SEQ = " + join_dict[first_col3 + str(first_col_pos)] + ".SEQ "
                join_dict[row.column3 + str(row.sel_col_pos)] = row[cl3]
                join_dict[row.column3 + str(row.sel_col_pos-1)] = row[cl3]
                z=0
            elif row.sel_col_pos >  prev_col_pos and row.column3 == prev_col3:
                dml = dml + "\n\t) "+ row[cl3] + " on " + row[cl3] + ".SEQ = " + join_dict[row.column3 + str(row.sel_col_pos-1)] + ".SEQ AND " + row[cl3] + ".idx = " + join_dict[row.column3 + str(row.sel_col_pos-1)] + ".idx" + "*** Check Join ***"
                join_dict[row.column3 + str(row.sel_col_pos)] = row[cl3]
            elif row.sel_col_pos <  prev_col_pos and row.column3 == prev_col3:
                dml = dml + "\n\t) "+ row[cl3] + " on " + row[cl3] + ".SEQ = " + join_dict[row.column3 + str(row.sel_col_pos-1)] + ".SEQ AND " + row[cl3] + ".idx = " + join_dict[row.column3 + str(row.sel_col_pos-1)] + ".idx" + "*** Check Join ***"
            prev_col_pos = row.sel_col_pos
            prev_col3 = row.column3
        i=i+1
    with open(Output_Dir+Bod_Nm+"_Flat_DML.sql", "w") as text_file:
        print("{}".format(dml), file=text_file)
    text_file.close()
#### Global Variable Declaration ####
Bod_Nm = 'GetRetailStore'        
#Inupt_File = 'C:\\Users\\rkori00\\Documents\\Project\\Data Ingestion Snowflake\\GetRetailStore_XSD_Sample.xml'
#Output_Dir = 'C:\\Users\\rkori00\\Documents\\Project\\Data Ingestion Snowflake\\Output\\'

Inupt_File = 'C:\\SYUE\\XML\\GetRetailStore_XSD_Sample.xml'
Output_Dir = 'C:\\SYUE\\XML\\'

DB_Nm = 'EDM_REFINED_DEV'
DB_Schema = 'SCRATCH'
Rtn_tm = 7
Var_Tbl = 'ESED_RETAILSTORE'
Var_Col = 'SRC_XML'
Parent_Tag = 'Abs:'
Child_Tag = 'Abs:'
my_list = []
split_tags = []
path_list = []
last1 = []
all_tags = []
cols = []
split_cols = []
new_col_lst = []
sort_path = []
####### End variable Declaration ####

tree = ET.parse(Inupt_File)
root = tree.getroot()
parseXML(root,"")
#print (my_list)
my_list = list(OrderedDict.fromkeys(my_list))
#print (my_list)
len_max = colList()
splitTags(len_max)
#creating Dataframe with all tags as columns
all_tags_df = pd.DataFrame(columns=cols, data=all_tags)
#creating Dataframe with last element and its position occurence in the XML tag
col_df = pd.DataFrame(columns=['sel_col','sel_col_pos'], data=last1)
col_df['sel_col'] = col_df['sel_col'].str[0]
# Merging both dataframes to form consolidated data frame
merge_df = all_tags_df.join(col_df)
merge_df = renameDupCols(merge_df)
# Append full the XML path as a column to the existing dataframe
path_df = pd.DataFrame(columns=['path','element'], data=path_list)
sort_df = pd.DataFrame(columns=['sort_path'], data=sort_path)
merge_df = merge_df.join(path_df)
merge_df = merge_df.join(sort_df)
createDDL(merge_df)
createDML(merge_df)