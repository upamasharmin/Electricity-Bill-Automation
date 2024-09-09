### LIBRARY
import pandas as pd
import os
import time
import datetime
from datetime import date
import math
from datetime import datetime
import warnings
import re
import sys
import calendar
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")
start_time = time.time()

### OBJECTS
from src.DTC_FRACTION_BILLING_AL import DTC_FRACTION_BILLING_AL
OBJ_DTC = DTC_FRACTION_BILLING_AL(pd, time, date, datetime, math, timedelta, calendar)

from src.PG_RH import PG_RH
OBJ_PG_RH = PG_RH(pd, time, date, datetime, math)

from src.ELECTRICITY_BILL import ELECTRICITY_BILL
OBJ_ELECTRICITY_BILL = ELECTRICITY_BILL(pd, time, date, datetime, math)
from src.AVERAGE_E_Bill import AVERAGE_E_Bill
OBJ_AVERAGE_E_Bill = AVERAGE_E_Bill(pd, time, date, datetime, math)
from src.FUEL_BILL import FUEL_BILL
OBJ_FUEL_BILL = FUEL_BILL(pd, time, date, datetime, math)

from src.SECURITY_COST import SECURITY_COST
OBJ_SECURITY_COST = SECURITY_COST(pd, time, date, datetime, math)


### FOLDER PATH
dir_path = os.path.dirname(os.path.realpath(__file__))
input_file_path = "\\input\\"
output_file_path = "\\output\\"
init_file_path = "\\init\\"
eFilePath = "E-Bill\\"


### GET DATE
date_input = input("Enter MNSA KPI Calculation Date: ")
invoice_date = datetime.strptime(date_input, '%b %Y')

### INPUT DATA 
print("- Loading Input...", end="\r")
DTC = pd.read_excel(dir_path + input_file_path + "DTC Data.xlsx")
File_Path = pd.read_excel(dir_path + "\\" + "config.xlsx", sheet_name="File Path")

# Loading the PriceBook file
PriceBook = pd.read_excel('C:\\Users\\' + os.environ.get('USERNAME') + File_Path[File_Path["File Name"] == "Price_Book"].iloc[0, 1])

# Locate the directory path for DC Load files
dc_load_directory = 'C:\\Users\\' + os.environ.get('USERNAME') + File_Path[File_Path["File Name"] == "DC"].iloc[0, 1]

# Function to find the latest DC Load file
def find_latest_dc_load_file(directory):
    pattern = r"DC Load_(\w+)'(\d{2})"
    files = os.listdir(directory)
    latest_file = None
    latest_date = datetime.min

    for file in files:
        match = re.search(pattern, file)
        if match:
            file_date = datetime.strptime(match.group(1) + " " + match.group(2), "%b %y")
            if file_date > latest_date:
                latest_date = file_date
                latest_file = file

    if latest_file:
        return os.path.join(directory, latest_file)
    else:
        raise FileNotFoundError("No valid DC Load files found in the directory")

# Read the latest DC Load file
dc_file_path = find_latest_dc_load_file(dc_load_directory)
DC_DF = pd.read_excel(dc_file_path)


# Other input data
PG_RH_BILL_DF = pd.read_excel(dir_path + input_file_path + "PG RH Robi Claim.xlsx")
SECURITY_BILL_DF = pd.read_excel(dir_path + input_file_path + "Security Bill Info.xlsx")
SECURITY_COST_OF_HIGH_SECURED_SITES = pd.read_excel(dir_path + input_file_path + "Security cost of high secured sites.xlsx")
ELECTRICITY_BILL_DF = pd.read_excel(dir_path + input_file_path + "Security Bill Info.xlsx")
FUEL_PASS_THROUGH_DF = pd.read_excel(dir_path + input_file_path + "Fuel Pass Through.xlsx")


### INPUT DATA - AVERAGE E-BILL
SUBMETER_BILL_DF = pd.read_csv(dir_path + input_file_path + "Submeter Bill.csv")
print("- Loading Input - Completed")


### DEFAULT DATA FRAME
DATA_FRAME = pd.DataFrame()

### OUTPUT INITIALIZATION
Output = pd.ExcelWriter(dir_path + output_file_path + "Service Fee.xlsx", engine="xlsxwriter")

### FRACTION BILLING - DTC
print("- Processing - DTC_FRACTION_BILLING", end="\r")
DataList = OBJ_DTC.PROCESS_DTC(DTC, invoice_date)
DTC_DF = DataList[0]
DIM = DataList[1]
DTC_DF.to_excel(dir_path + output_file_path + "DTC.xlsx", index=None)
print("- Processing - DTC_FRACTION_BILLING - Completed")

### EDIT PRICE BOOK
PriceBook = PriceBook[["Name of the Line Item", "Rate", "Discount", "PG Fuel Factor", "PG Baseline RH", "Passthrough %", "Colo MNO Count for Discount", "Indoor (Other Customer Count)", "Outdoor (Other Customer Count)", "Escalation Factor", "Escalation Start Date", "Indoor/Outdoor"]]

# PG RH
print("- Processing - PG RH", end="\r")
Output_PG_RH = OBJ_PG_RH.PG_RH(PG_RH_BILL_DF, PriceBook, invoice_date)
Output_PG_RH.to_excel(Output, index=None, sheet_name="PG RH BILL")
print("- Processing - PG RH - Completed")

### ELECTRICITY BILL
print("- Processing - ELECTRICITY BILL", end="\r")
E_BILL_3_MONTH_DF = OBJ_ELECTRICITY_BILL.ACTUAL_E_BILL(date_input, dir_path, input_file_path, eFilePath)
E_BILL_3_MONTH_DF.to_excel(dir_path + output_file_path + "Bill.xlsx", index=None)
print("- Processing - ELECTRICITY BILL - Completed")

### AVERAGE_E_Bill
print("- Processing - AVERAGE_E_Bill", end="\r")
Output_AVERAGE_E_Bill = OBJ_AVERAGE_E_Bill.AVERAGE_E_Bill(DTC_DF, PriceBook, E_BILL_3_MONTH_DF, SUBMETER_BILL_DF,DC_DF,date_input, DIM)
Output_AVERAGE_E_Bill.to_excel(Output, index=None, sheet_name="AVERAGE_E_Bill")
print("- Processing - AVERAGE_E_Bill - Completed")

### AVERAGE_E_Bill RECON
print("- Processing - AVERAGE_E_Bill RECON", end="\r")
Output_AVERAGE_E_Bill_RECON = OBJ_AVERAGE_E_Bill.AVERAGE_E_Bill_RECON(Output_AVERAGE_E_Bill, date_input, dir_path, input_file_path, SUBMETER_BILL_DF, eFilePath)
Output_AVERAGE_E_Bill_RECON.to_excel(Output, index=None, sheet_name="AVERAGE_E_Bill_RECON")
print("- Processing - AVERAGE_E_Bill RECON - Completed")

### FUEL BILL
print("- Processing - FUEL_BILL", end="\r")
Output_FUEL_BILL = OBJ_FUEL_BILL.FUEL_BILL(FUEL_PASS_THROUGH_DF, DTC_DF, PriceBook, date_input)
Output_FUEL_BILL.to_excel(Output, index=None, sheet_name="FUEL_BILL")
print("- Processing - FUEL_BILL - Completed")

print("- Processing - FUEL_BILL RECON", end="\r")
Output_FUEL_BILL_RECON = OBJ_FUEL_BILL.FUEL_BILL_RECON(DTC_DF, date_input, dir_path, input_file_path, FUEL_PASS_THROUGH_DF, eFilePath)
Output_FUEL_BILL_RECON.to_excel(Output, index=None, sheet_name="FUEL_BILL_RECON")
print("- Processing - FUEL_BILL RECON - Completed")

## SECURITY COST
print("- Processing - SECURITY COST", end="\r")
Output_SECURITY_COST = OBJ_SECURITY_COST.SERVICE_FEE_SECURITY_COST(SECURITY_BILL_DF, PriceBook)
Output_SECURITY_COST.to_excel(Output, index=None, sheet_name="Continuous Security Cost")
SECURITY_COST_OF_HIGH_SECURED_SITES.to_excel(Output, index=None, sheet_name="High Secured Site")
print("- Processing - SECURITY COST - Completed")

### FINAL OUTPUT
DTC.to_excel(Output, index=None, sheet_name="DTC")
PriceBook.to_excel(Output, index=None, sheet_name="PriceBook")
Output._save()

### END PROCESS
elapsed_time = time.time() - start_time
elapsed_time_hr = round(math.floor((elapsed_time) / 3600))
elapsed_time = (elapsed_time) % 3600
elapsed_time_min = round(math.floor((elapsed_time) / 60))
elapsed_time = elapsed_time % 60
elapsed_time_sec = round(math.floor((elapsed_time) % 60))
print("- Processing Time: {0} Hour {1} Minute {2} Second".format(elapsed_time_hr,elapsed_time_min,elapsed_time_sec) + "")