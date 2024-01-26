"""
 purpose: Common used functions
          - no m
 Module name:  C:\\users\\iny2819\\kroger\\Code\\com_code.py
 Author: Sophia Yue
 Date:   10-13-23
 function name:
  f_get_hh_mm_ss  
  elapse_time 
  f_read
 Instruction: 
   - No need to define the common function codes in the invoking code
   - to invoke the functions, include the following code in the invoking code    

    path_code = 'C:\\users\\iny2819\\kroger\\Code\\'  
    f_com_code = path_code + "com_code.py"
    exec(compile(open(f_com_code , "rb").read(), f_com_code, 'exec' ))
"""
from datetime import datetime

def f_get_hh_mm_ss(tot_second):
    """
      module name : f_get_hh_mm_ss
      purpose     : Convert total seconds into hours, minutes, and seconds 
      parameter
         tot_second   : total seconds; any numeric value, integer or floating
      note            : Will convert the floating number to integer and drop the values after the decimal point
      Example         : f_get_hh_mm_ss(3618.52)  # return (1, 0, 18)which is 1 hour and 18 seconds      
    """   
    tot_second = int(tot_second)
    min  = 60
    hour = 60 * 60
    day  = 60 * 60 * 24     
    hh =  tot_second // hour
    mm = (tot_second - (hh * hour)) // min
    ss =  tot_second  - ((hh * hour) + (mm * min))
    return  hh, mm, ss


def elapse_time (start_time, end_time, dsc):
    """
     module name  : elapse_time
     purpose      : Get elapse time and print it as hh:mm:yy 
     parameter    : 
       start_time : Start time in second;  any numeric value, integer or floating e.g. time.time()
       end_time   : End Time in second  ;  any numeric value; integer or floating e.g. time.time()
       desc       : Description 
     notes        :
                   - The calling function is required to "import time
                   - Will convert the start_time and end_time to integers
                   - will call function "f_get_hh_mm_ss" to convert the elapse_time to hours, minutes, and seconds
                   - Will call strftime function from time module to display the timestamp for start time and end time 
     example1    :
                   elapse_time(0, 2400.17, "Test completed.")
                   - The result would be
                     Test completed. It took 3701.170000 seconds - 1hh:1mm:41ss.
                     start time: Dec 31 1969 17:00:00  end time:  Dec 31 1969 18:01:41
     example2   :              
                   cty_start_time = time.time()  # type : floating
                   time.sleep(5)
                   cty_end_time = time.time()
                   elapse_time (  cty_start_time, cty_end_time, "Test completed.")
                   - The result would be
                     Test completed. It took 5.001574 seconds - 0hh:0mm:5ss.
                     start time: Jan 19 2019 20:20:14  end time:  Jan 19 2019 20:20:19                 
    """    
    elapsed =  end_time -  start_time
    hh, mm, ss = f_get_hh_mm_ss(elapsed)
    print (" %s It took %3f seconds - %uhh:%umm:%uss." %(dsc,elapsed, hh, mm, ss)) 
    print (" start time:", time.strftime("%b %d %Y %H:%M:%S", time.localtime(start_time)), " end time: ",  time.strftime("%b %d %Y %H:%M:%S", time.localtime(end_time)))
    return hh, mm, ss


def f_read(path, file, sheet_name = '', encoding = False, sep = ','):
    exe = file.split('.')[-1]
    if exe == 'zip':
       if  ('parquet' in file):
           print("Data" in my_string) 
           df = pd.read_parquet(path + file)
       else: df = pd.read_csv(path + file, compression="zip")
    elif exe == 'csv': 
       #df = pd.read_csv( path + file, dtype='unicode',  engine='python', error_bad_lines=False)
       if encoding != False:  df = pd.read_csv( path + file, dtype='unicode',  engine='python', encoding= encoding, sep = sep)
       else:  df = pd.read_csv( path + file, dtype='unicode',  engine='python', sep = sep) 
    elif exe == 'xlsx': 
       if  sheet_name == '':  df = pd.read_excel( path + file  )
       else:  df = pd.read_excel( path + file, sheet_name = sheet_name)     
    else: pass
    print (f'file {file} shape {df.shape} \n columns: {df.columns}')
    print (f'dtypes: \n {df.dtypes}')
    print (f'head: \n {df.head()}')
    return df    


