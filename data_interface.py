
import time
import numpy as np
import pandas as pd
from datetime import datetime

def create_sample_data():
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    #define empty dataframe
    df = pd.DataFrame(columns=['Frame', 'Element', 'Type', 'Timestamp', 'Length', 'Value'])
    
    #add rows to dataframe
    for i in range(10):
        df.loc[len(df)] = [f"Long_Test_Frame_1", f"Element_{i}", "double", dt_string, 1, np.random.rand(1)]
    df.loc[len(df)] = [f"Long_Test_Frame_1", f"Element_Array", "double", dt_string, 5, "[0.1, 0.2, 0.3, 0.4, 0.5]"]
    
    return df

def __update_value(df):
    #update element and timestamps
    for i in range(11):
        #if length is 1, update value
        if df.loc[i, 'Length'] == 1:
            df.loc[i, 'Value'] = np.random.rand(1)
            df.loc[i, 'Timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #if length is 5, update value
        elif df.loc[i, 'Length'] == 5:
            df.loc[i, 'Value'] = "[0.1, 0.2, 0.3, 0.4, 0.5]"
            df.loc[i, 'Timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
    return df

async def update_data(df):
    #wait 0.5 seconds
    time.sleep(0.5)
    return __update_value(df)