#!/usr/bin/env python
# coding: utf-8


import pandas as pd, numpy as np
import datetime as dt


### Load original attribute labelled with Fuzzy Match (Un-normalized), multiple attributes need to be delimited
attr_path = '/dbfs/FileStore/tables/DATA_SCIENCE/COLOR/'
attributed_df = pd.read_csv(attr_path + 'COLOR_HOUSEWARES_DPT.csv')
attrib_field = 'EXTRACTED_COLOR'
delim = '|'
attributed_df = attributed_df[attributed_df[attrib_field] != 'OTHER']


single_attributes = pd.Series(attributed_df[attrib_field].apply(lambda x: x.split(delim)).sum())


100*single_attributes.value_counts().cumsum()/len(single_attributes)


### Cumulative Percent Prevalence of Single Attributes ranked from top
attrib_cum_counts = pd.DataFrame(100* single_attributes.value_counts().cumsum()/len(single_attributes), columns = ['PERCENT_CUMULATIVE_COUNT'])
cutoff = 100 # Select top attributes that add upto this percentage of all non-other attributed items)
attrib_cum_counts[attrib_cum_counts.PERCENT_CUMULATIVE_COUNT <= cutoff][:100]\
    .reset_index(drop = False).rename(columns = {'index':attrib_field}).to_csv(attr_path+'Normalized_COLOR_HOUSEWARES_Top100.csv', index =None)


### Incorporating PO Feedback
normalized_list = list(attrib_cum_counts.index[:100])
discard = ['DEEP','FISH','BUTTERFLY','SCOOP','LIGHT','UNICORN','OWL','MIRROR MIRROR','ALPHABET','UNIVERSAL','HAPPY BIRTHDAY','LOVELY']
normalized_list = [ i for i in normalized_list if i not in discard] + ['OTHER']
rename = {'ASSORTED':'MULTI COLOR'}
normalized_list += rename.values()

def normalize_colors(attr_string, normalized_list = normalized_list ,delim = '|', rename = rename):
    attr_list = attr_string.split(delim)
    attr_list = [rename[i] if i in rename.keys() else i for i in attr_list]
    attr_list = [i for i in attr_list if i in normalized_list]
    if len(attr_list) > 0:
        return (delim).join(attr_list)
    else: return 'OTHER'


### Write normalized attributes in colon-separated format
attributed_df['NORMALIZED_COLOR'] = attributed_df.EXTRACTED_COLOR.apply(lambda x: ':'.join(normalize_colors(x).split('|')))
display_cols = ['GTIN_NO','COM_DSC','SUBCOM_DSC','VND_ECOM_DSC','NORMALIZED_COLOR']
today = dt.datetime.today().strftime("%m%d%Y")
attributed_df[display_cols].to_csv(attr_path +'COLOR_NORMALIZED_HOUSEWARES_'+today+'.csv', index = None)


