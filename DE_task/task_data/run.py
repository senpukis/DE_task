import pandas as pd
import numpy as np
import glob
import os
from datetime import date

# paths to folders/files
data_path = r"task_data"
policy_path = r"POLICY_DATA.csv"
result_path = r"results"

# reads all files with.csv extension
filenames = glob.glob(data_path + "\*.csv")
print('File names:', filenames)
df = pd.DataFrame()

# Read policy data
df_b = pd.read_csv(policy_path)

# for loop to iterate and concat csv files
for file in filenames:
    temp = pd.read_csv(file,low_memory=False,index_col=0)
    df = pd.concat([df, temp], axis=0, ignore_index=True)

# Not sure if required but, this block is meant for to reset the index to start from 1 instead 0 
df = df.reset_index()
df = df.rename(columns={"index":"id"})
df['id'] = df.index + 1 

# Joining policy file by policy_id column with inner join
main = pd.merge(df, df_b, how='inner', left_on = 'policy_id', right_on='policy_id')

# Replacing missing values 'car_brand' with a mode
main['car_brand'] = main['car_brand'].fillna(main['car_brand'].mode()[0])

# Creating new column 'car_age' by years 
main['car_age'] = main['car_age'].year = date.today().year - main['car_registration_year']

# Replace missing value of “car_eng_pow” by “-1”. Then group values into "0-100","100-250", "250+" groups
main['car_eng_pow'] = main['car_eng_pow'].fillna(-1)

def group (car_eng_pow):
    if 0.0 <= car_eng_pow <=100 : return "0-100"
    elif 100.1 <= car_eng_pow <= 250 : return "100-250"
    elif car_eng_pow > 250.0 : return "more than 250"

main['car_eng_pow'] = main['car_eng_pow'].apply(group)

# Regroup “marital_status” in a binary way: 1 - Single, 2 - Married. Blank fields should be grouped into a Single group.
main['marital_status'] = main['marital_status'].fillna(1) # Blank fields replaced with value "1"
marital_status = {
                    1 : "Single",
                    2 : "Married"}
main["marital_status"] = main["marital_status"].map(marital_status)

# Replace missing values of “claim_amount” with “0”
main['claim_amount'] = main['claim_amount'].fillna(0) # Blank fields replaced with value "0"


# Output results to an .csv file
main.to_csv(os.path.join(result_path,r'result.csv'))

# Display in terminal results
print(df)
print(df_b)
print(main)




### Replace missing value of “car_eng_pow” by “-1”. Then group values into "0-100","100-250", "250+" groups (Alternate version)
# bins = [-1, 100, 250, np.inf]
# labels=['0-100','100-250','more than 250']
# group=main.groupby(pd.cut(main['car_eng_pow'], bins=bins, labels=labels)).size().reset_index(name='count')
# car_eng_pow = {
#                     range(0,100) : "0-100",
#                     range(100,250) : "100-250",
#                     range(250) : "100-250"}
# main["car_eng_pow"] = main["car_eng_pow"].map(car_eng_pow)