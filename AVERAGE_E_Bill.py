class AVERAGE_E_Bill:
    def __init__(self, pd, time, date, datetime, math): 
        self.pd = pd
        self.time = time
        self.math = math
        self.date = date
        self.datetime = datetime
        self.today = date.today()
        self.now = datetime.now()
        self.today = self.today.strftime("%d_%m_%Y")
        self.dt_string = self.now.strftime("%d/%m/%Y %H:%M:%S")

    # ------------------------------------------------------------------ #

    def AVERAGE_E_Bill(self, DTC_DF, PriceBook, E_BILL_3_MONTH_DF, SUBMETER_BILL_DF,DC_DF,date_input, DIM):
        E_BILL_3_MONTH = E_BILL_3_MONTH_DF.copy()
        Month_List = []
        if(date_input[0:3] == "Jan"):
            Month_List = ["Nov-" + (str(int(date_input[4:8]) - 1)), "Dec-" + (str(int(date_input[4:8]) - 1)), "Jan-" + (str(int(date_input[4:8])))]
        elif(date_input[0:3] == "Feb"):
            Month_List = ["Dec-" + (str(int(date_input[4:8]) - 1)), "Jan-" + (str(int(date_input[4:8])), "Feb-" + (str(int(date_input[4:8]))))]
 
        elif(date_input[0:3] == "Mar"):
             Month_List = ["Jan", "Feb", "Mar"]
        elif(date_input[0:3] == "Apr"):
            Month_List = ["Feb", "Mar", "Apr"]
        elif(date_input[0:3] == "May"):
            Month_List = ["Mar","Apr",  "May"]
        elif(date_input[0:3] == "Jun"):
            Month_List = ["Apr", "May", "Jun"]
        elif(date_input[0:3] == "Jul"):
            Month_List = ["May", "Jun", "Jul"]
        elif(date_input[0:3] == "Aug"):
             Month_List = ["Jun", "Jul", "Aug"]
        elif(date_input[0:3] == "Sep"):
             Month_List = ["Jul", "Aug", "Sep"]
        elif(date_input[0:3] == "Oct"):
             Month_List = ["Aug", "Sep", "Oct"]
        elif(date_input[0:3] == "Nov"):
             Month_List = ["Sep", "Oct", "Nov"]
        elif(date_input[0:3] == "Dec"):
             Month_List = ["Oct", "Nov", "Dec"]
            
        else:
            Month_List = []
        DTC = DTC_DF.copy()
        DF = DTC[["SiteRef", "Indoor/Outdoor", "Colo MNO Count for Discount", "Indoor_Other Customer Count", "Outdoor_Other Customer Count"]]
        # TODO::As per the Date
        E_BILL_3_MONTH_DF = E_BILL_3_MONTH_DF[["EASI Site Code", "Amount-" + Month_List[0] + "-" + date_input[4:8],	"VAT-" + Month_List[0] + "-" + date_input[4:8], "Amount-" + Month_List[1] + "-" + date_input[4:8], "VAT-" + Month_List[1] + "-" + date_input[4:8], "Amount-" + Month_List[2] + "-" + date_input[4:8], "VAT-" + Month_List[2] + "-" + date_input[4:8], "Consumption-" + Month_List[0] + "-" + date_input[4:8], "Consumption-" + Month_List[1] + "-" + date_input[4:8], "Consumption-" + Month_List[2] + "-" + date_input[4:8]]]

        DC_DF = DC_DF.rename(columns={"EASI Site Ref.": "EASI Site Code"})
       
        
        for i in range(len(E_BILL_3_MONTH_DF)):
            try:
                E_BILL_3_MONTH_DF.iloc[i, 1] = float(E_BILL_3_MONTH_DF.iloc[i, 1])
            except:
                E_BILL_3_MONTH_DF.iloc[i, 1] = 0
            try:
                E_BILL_3_MONTH_DF.iloc[i, 2] = float(E_BILL_3_MONTH_DF.iloc[i, 2])
            except:
                E_BILL_3_MONTH_DF.iloc[i, 2] = 0
            try:
                E_BILL_3_MONTH_DF.iloc[i, 3] = float(E_BILL_3_MONTH_DF.iloc[i, 3])
            except:
                E_BILL_3_MONTH_DF.iloc[i, 3] = 0
            try:
                E_BILL_3_MONTH_DF.iloc[i, 4] = float(E_BILL_3_MONTH_DF.iloc[i, 4])
            except:
                E_BILL_3_MONTH_DF.iloc[i, 4] = 0
            try:
                E_BILL_3_MONTH_DF.iloc[i, 5] = float(E_BILL_3_MONTH_DF.iloc[i, 5])
            except:
                E_BILL_3_MONTH_DF.iloc[i, 5] = 0
            try:
                E_BILL_3_MONTH_DF.iloc[i, 6] = float(E_BILL_3_MONTH_DF.iloc[i, 6])
            except:
                E_BILL_3_MONTH_DF.iloc[i, 6] = 0
             
        TEMP_DF = E_BILL_3_MONTH_DF.copy()
        TEMP_DF = TEMP_DF.drop_duplicates(subset=['EASI Site Code'], keep='first')
        TEMP_DF = TEMP_DF.reset_index()
        del TEMP_DF['index']
        TEMP_DF["Total-" + Month_List[0]] = 0 # 10
        TEMP_DF["Total-" + Month_List[1]] = 0 # 11
        TEMP_DF["Total-" + Month_List[2]] = 0 # 12
        TEMP_DF["Electricity Bill (3 month average/preceeding month or 0)"] = 0 # 13
        TEMP_DF["Average Usage Consumption"] = 0 # 14
        TEMP_DF["Per Hour Consumption"] = 0 # 15
        for i in range(len(TEMP_DF)): # Sum Up Duplicate Values
            DF0 = E_BILL_3_MONTH_DF[E_BILL_3_MONTH_DF["EASI Site Code"] == str(TEMP_DF.iloc[i, 0])]
            DF1 = 0
            DF2 = 0
            DF3 = 0
            DF4 = 0
            DF5 = 0
            DF6 = 0
            DF7 = 0
            DF8 = 0
            DF9 = 0
            for j in range(len(DF0)):
                # Month 1
                try: 
                    DF0.iloc[j, 1] = float(DF0.iloc[j, 1])
                    if(str(DF0.iloc[j, 1]) == "nan"):
                        DF1 = DF1 + 0
                    else:
                        DF1 = DF1 + DF0.iloc[j, 1]
                except:
                    DF1 = DF1 + 0
                try:
                    DF0.iloc[j, 2] = float(DF0.iloc[j, 2]) 
                    if(str(DF0.iloc[j, 2]) == "nan"):
                        DF2 = DF2 + 0
                    else:
                        DF2 = DF2 + DF0.iloc[j, 2]
                except:
                    DF2 = DF2 + 0
                # Month 2
                try:
                    DF0.iloc[j, 3] = float(DF0.iloc[j, 3])
                    if(str(DF0.iloc[j, 3]) == "nan"):
                        DF3 = DF3 + 0
                    else:
                        DF3 = DF3 + DF0.iloc[j, 3]
                except:
                    DF3 = DF3 + 0
                try: 
                    DF0.iloc[j, 4] = float(DF0.iloc[j, 4])
                    if(str(DF0.iloc[j, 4]) == "nan"):
                        DF4 = DF4 + 0
                    else:
                        DF4 = DF4 + DF0.iloc[j, 4]
                except:
                    DF4 = DF4 + 0
                # Month 3
                try:
                    DF0.iloc[j, 5] = float(DF0.iloc[j, 5])
                    if(str(DF0.iloc[j, 5]) == "nan"):
                        DF5 = DF5 + 0
                    else:
                        DF5 = DF5 + DF0.iloc[j, 5]
                except:
                    DF5 = DF5 + 0 
                try:
                    DF0.iloc[j, 6] = float(DF0.iloc[j, 6])
                    if(str(DF0.iloc[j, 6]) == "nan"):
                        DF6 = DF6 + 0
                    else:
                        DF6 = DF6 + DF0.iloc[j, 6]
                except:
                    DF6 = DF6 + 0

                try: # Consumption # Month 1
                    DF0.iloc[j, 7] = float(DF0.iloc[j, 7])
                    if(str(DF0.iloc[j, 7]) == "nan"):
                        DF7 = DF7 + 0
                    else:
                        DF7 = DF7 + DF0.iloc[j, 7]
                except:
                    DF7 = DF7 + 0
                try: # Consumption # Month 2
                    DF0.iloc[j, 8] = float(DF0.iloc[j, 8])
                    if(str(DF0.iloc[j, 8]) == "nan"):
                        DF8 = DF8 + 0
                    else:
                        DF8 = DF8 + DF0.iloc[j, 8]
                except:
                    DF8 = DF8 + 0
                try: # Consumption # Month 3
                    DF0.iloc[j, 9] = float(DF0.iloc[j, 9])
                    if(str(DF0.iloc[j, 9]) == "nan"):
                        DF9 = DF9 + 0
                    else:
                        DF9 = DF9 + DF0.iloc[j, 9]
                except:
                    DF9 = DF9 + 0

            TEMP_DF.iloc[i, 1] = DF1
            TEMP_DF.iloc[i, 2] = DF2
            TEMP_DF.iloc[i, 3] = DF3
            TEMP_DF.iloc[i, 4] = DF4
            TEMP_DF.iloc[i, 5] = DF5
            TEMP_DF.iloc[i, 6] = DF6
            TEMP_DF.iloc[i, 7] = DF7
            TEMP_DF.iloc[i, 8] = DF8
            TEMP_DF.iloc[i, 9] = DF9

            TEMP_DF.iloc[i, 10] = TEMP_DF.iloc[i, 1] + TEMP_DF.iloc[i, 2] # Month 1
            TEMP_DF.iloc[i, 11] = TEMP_DF.iloc[i, 3] + TEMP_DF.iloc[i, 4] # Month 2
            TEMP_DF.iloc[i, 12] = TEMP_DF.iloc[i, 5] + TEMP_DF.iloc[i, 6] # Month 3

            x = 0
            if(TEMP_DF.iloc[i, 10] > 0):
                x = x + 1
            if(TEMP_DF.iloc[i, 11] > 0):
                x = x + 1
            if(TEMP_DF.iloc[i, 12] > 0):
                x = x + 1

            y = 0
            if(TEMP_DF.iloc[i, 7] > 0):
                y = y + 1
            if(TEMP_DF.iloc[i, 8] > 0):
                y = y + 1
            if(TEMP_DF.iloc[i, 9] > 0):
                y = y + 1
            
            TEMP_DF.iloc[i, 13] = (TEMP_DF.iloc[i, 10] + TEMP_DF.iloc[i, 11] + TEMP_DF.iloc[i, 12]) / x # Average Electricity Bill
            TEMP_DF.iloc[i, 14] = (TEMP_DF.iloc[i, 7] + TEMP_DF.iloc[i, 8] + TEMP_DF.iloc[i, 9]) / 3 # Average Consumption
            TEMP_DF.iloc[i, 15] = (TEMP_DF.iloc[i, 14] / 24) / DIM # Per Hour Consumption

        DTC_DF.rename(columns={"SiteRef":"EASI Site Code"}, inplace=True)
        TEMP_DF = self.pd.merge(TEMP_DF, DTC_DF[["EASI Site Code", "Customer Site Ref"]], on="EASI Site Code", how="left")
        TEMP_DF = self.pd.merge(TEMP_DF, DTC_DF[["EASI Site Code", "Indoor/Outdoor"]], on="EASI Site Code", how="left")
        TEMP_DF = self.pd.merge(TEMP_DF, DTC_DF[["EASI Site Code", "Colo MNO Count for Discount"]], on="EASI Site Code", how="left") #18
        TEMP_DF = self.pd.merge(TEMP_DF, DTC_DF[["EASI Site Code", "Indoor_Other Customer Count"]], on="EASI Site Code", how="left")
        TEMP_DF = self.pd.merge(TEMP_DF, DTC_DF[["EASI Site Code", "Outdoor_Other Customer Count"]], on="EASI Site Code", how="left")
       
    
        TEMP_DF["Passthrough %"] = 0 #21
        TEMP_DF["Robi Electricity (considering MSA)"] = "" #22
        TEMP_DF = self.pd.merge(TEMP_DF, DC_DF[["EASI Site Code", "Total DC Load_Robi data"]], on="EASI Site Code", how="left")#23
        TEMP_DF[TEMP_DF.columns[23]] = TEMP_DF["Total DC Load_Robi data"]#23
        
        # Passthrough %
        for i in range(len(TEMP_DF)):
            if(str(TEMP_DF.iloc[i, 18]) == "nan" or str(TEMP_DF.iloc[i, 18]) == "" or str(TEMP_DF.iloc[i, 18]) == "NaT"):
                TEMP_DF.iloc[i, 18] = "0.0"
            else:
                TEMP_DF.iloc[i, 18] = str(float(TEMP_DF.iloc[i, 18]))
            if(str(TEMP_DF.iloc[i, 19]) == "nan" or str(TEMP_DF.iloc[i, 19]) == "" or str(TEMP_DF.iloc[i, 19]) == "NaT"):
                TEMP_DF.iloc[i, 19] = "0.0"
            else:
                TEMP_DF.iloc[i, 19] = str(float(TEMP_DF.iloc[i, 19]))
            if(str(TEMP_DF.iloc[i, 20]) == "nan" or str(TEMP_DF.iloc[i, 20]) == "" or str(TEMP_DF.iloc[i, 20]) == "NaT"):
                TEMP_DF.iloc[i, 20] = "0.0"
            else:
                TEMP_DF.iloc[i, 20] = str(float(TEMP_DF.iloc[i, 20]))
            # FILTER PRICE BOOK - "Name of the Line Item"
            PB = PriceBook[PriceBook["Name of the Line Item"] == "E-Bill Discount for Other Customer Consumtion"]
            PB = PB[PB["Indoor/Outdoor"] == TEMP_DF.iloc[i].loc["Indoor/Outdoor"]]
            for item in range(len(PB)):
                if(str(PB.iloc[item].loc["Colo MNO Count for Discount"]) == str(TEMP_DF.iloc[i, 18]) and str(PB.iloc[item].loc["Indoor (Other Customer Count)"]) == str(TEMP_DF.iloc[i, 19]) and str(PB.iloc[item].loc["Outdoor (Other Customer Count)"]) == str(TEMP_DF.iloc[i, 20])):
                    TEMP_DF.iloc[i, 21] = PB.iloc[item, 5]

            TEMP_DF.iloc[i, 22] = TEMP_DF.iloc[i, 13] * TEMP_DF.iloc[i, 21] # Robi Electricity (considering MSA)
            

        TEMP_DF = self.pd.merge(TEMP_DF, DTC_DF[["EASI Site Code", "Total Non-MNO Count"]], on="EASI Site Code", how="left") # 24
        TEMP_DF = self.pd.merge(TEMP_DF, DTC_DF[["EASI Site Code", "Non-MNO DC Load"]], on="EASI Site Code", how="left") # 25


        TEMP_DF["Discount for non-MNO"] = "" # 26
        TEMP_DF["E-bill PT amount after Colo discount"] = "" # 27
        TEMP_DF["Calculated VAT Rebate"] = "" # 28

        for i in range(len(TEMP_DF)):
            if(str(TEMP_DF.iloc[i, 25]) == "nan"): # Non-MNO DC Load
                TEMP_DF.iloc[i, 25] = 0
            
            if(str(TEMP_DF[TEMP_DF.columns[23]]) == "nan"): # Robi DC Load
                TEMP_DF[TEMP_DF.columns[23]] = 0
            

            if(str(TEMP_DF.iloc[i, 22]) == "nan"): # Robi Electricity (considering MSA)
                TEMP_DF.iloc[i, 22] = 0

            TEMP_DF.iloc[i, 26] = (TEMP_DF.iloc[i, 25]/TEMP_DF.iloc[i, 23]) *  TEMP_DF.iloc[i, 22] #Discount for MNO

            TEMP_DF.iloc[i, 27] = TEMP_DF.iloc[i, 22] - TEMP_DF.iloc[i, 26] # E-bill PT amount after Colo discount

            TEMP_DF.iloc[i, 28] = TEMP_DF.iloc[i, 27] - (TEMP_DF.iloc[i, 27] * (100/105)) #Calculated VAT Rebate

        E_BILL_3_MONTH = E_BILL_3_MONTH.drop_duplicates(subset=['EASI Site Code'], keep='first')
        TEMP_DF = self.pd.merge(TEMP_DF, E_BILL_3_MONTH[["EASI Site Code", "Meter Owner"]], on="EASI Site Code", how="left") # 29
        
        SUBMETER_BILL_DF.rename(columns={"Edotco ID":"EASI Site Code"}, inplace=True)
        SUBMETER_BILL_DF = SUBMETER_BILL_DF.drop_duplicates(subset=['EASI Site Code'], keep='first')
        TEMP_DF = self.pd.merge(TEMP_DF, SUBMETER_BILL_DF[["EASI Site Code", "Customer ID"]], on="EASI Site Code", how="left") # 30

        TEMP_DF["Electricity Authority"] = "" # 31
        TEMP_DF["Applicable VAT rebate (e.co)"] = "" # 32
        TEMP_DF["Net amount (3m avg)"] = "" # 33
        for i in range(len(TEMP_DF)):
            # if(str(TEMP_DF.iloc[i, 25]) == "nan"):
            #     TEMP_DF.iloc[i, 25] = 0
            if(str(TEMP_DF.iloc[i, 30]) != "nan"): # Electricity Authority
                TEMP_DF.iloc[i, 31] = "Submeter"
            else:
                TEMP_DF.iloc[i, 31] = TEMP_DF.iloc[i, 29]

            if(str(TEMP_DF.iloc[i, 31]) == "e.co"): # Applicable VAT rebate (e.co)
                TEMP_DF.iloc[i, 32] = TEMP_DF.iloc[i, 28]

            if(str(TEMP_DF.iloc[i, 32]) == ""): # Electricity Authority
                TEMP_DF.iloc[i, 33] = TEMP_DF.iloc[i, 27]
            else:
                TEMP_DF.iloc[i, 33] = TEMP_DF.iloc[i, 27] - TEMP_DF.iloc[i, 32] # Net amount (3m avg)

        TEMP_DF = self.pd.merge(TEMP_DF, SUBMETER_BILL_DF[["EASI Site Code", "Total bill amount with PF charge{(e+f+g)}"]], on="EASI Site Code", how="left")
        TEMP_DF.rename(columns={"Total bill amount with PF charge{(e+f+g)}":"Sub-meter billing"}, inplace=True) # 34

        TEMP_DF["Submeter Bill (Robi to Share)"] = "" # 35
        TEMP_DF["Net Passthrough amount"] = "" # 36
        for i in range(len(TEMP_DF)):
            if(str(TEMP_DF.iloc[i, 18]) != "nan"):
                TEMP_DF.iloc[i, 35] = TEMP_DF.iloc[i, 34] / float(TEMP_DF.iloc[i, 18])
            else:
                TEMP_DF.iloc[i, 35] = TEMP_DF.iloc[i, 34]

            if(str(TEMP_DF.iloc[i, 34]) != "nan"):
                TEMP_DF.iloc[i, 36] = TEMP_DF.iloc[i, 34]
            else:
                TEMP_DF.iloc[i, 36] = TEMP_DF.iloc[i, 33]
        return TEMP_DF
    
    def AVERAGE_E_Bill_RECON(self, Output_AVERAGE_E_Bill, date_input, dir_path, input_file_path, SUBMETER_BILL_DF, eFilePath):
        Output_AVERAGE_E_Bill_DF = Output_AVERAGE_E_Bill.copy()
        if(date_input[0:3] == "Jan"):
            Month_List = ["Nov-" + (str(int(date_input[4:8]) - 1)), "Dec-" + (str(int(date_input[4:8]) - 1)), "Jan-" + (str(int(date_input[4:8])))]
        elif(date_input[0:3] == "Feb"):
            Month_List = ["Dec-" + (str(int(date_input[4:8]) - 1)), "Jan-" + (str(int(date_input[4:8])), "Feb-" + (str(int(date_input[4:8]))))]
 
        elif(date_input[0:3] == "Mar"):
             Month_List = ["Jan", "Feb", "Mar"]
        elif(date_input[0:3] == "Apr"):
            Month_List = ["Feb", "Mar", "Apr"]
        elif(date_input[0:3] == "May"):
            Month_List = ["Mar","Apr",  "May"]
        elif(date_input[0:3] == "Jun"):
            Month_List = ["Apr", "May", "Jun"]
        elif(date_input[0:3] == "Jul"):
            Month_List = ["May", "Jun", "Jul"]
        elif(date_input[0:3] == "Aug"):
             Month_List = ["Jun", "Jul", "Aug"]
        elif(date_input[0:3] == "Sep"):
             Month_List = ["Jul", "Aug", "Sep"]
        elif(date_input[0:3] == "Oct"):
             Month_List = ["Aug", "Sep", "Oct"]
        elif(date_input[0:3] == "Nov"):
             Month_List = ["Sep", "Oct", "Nov"]
        elif(date_input[0:3] == "Dec"):
             Month_List = ["Oct", "Nov", "Dec"]
            
        else:
            Month_List = []

        PT1 = self.pd.DataFrame()
        PT2 = self.pd.DataFrame()
        PT3 = self.pd.DataFrame()
        n = 0
        for i in Month_List:
            if n == 0:
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  PT1 = self.pd.read_excel(dir_path + input_file_path + eFilePath +str(int(date_input[4:8]) - 1) + "\\" + "Energy PT " + i + "-" + Month_List[0] + ".xlsx")
                else:
                  PT1 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Energy PT " + i + "-" + date_input[4:8] + ".xlsx")
            elif n == 1:
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  PT2 = self.pd.read_excel(dir_path + input_file_path + eFilePath +str(int(date_input[4:8]) - 1) + "\\" + "Energy PT " + i + "-" + Month_List[0] + ".xlsx")
                else:
                  PT2 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Energy PT " + i + "-" + date_input[4:8] + ".xlsx")
            elif n == 2:
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  PT3 = self.pd.read_excel(dir_path + input_file_path + eFilePath +str(int(date_input[4:8]) - 1) + "\\" + "Energy PT " + i + "-" + Month_List[0] + ".xlsx")
                else:
                  PT3 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Energy PT " + i + "-" + date_input[4:8] + ".xlsx")
            n = n + 1

        frames = [PT1, PT2, PT3]
        PT = self.pd.concat(frames, sort=False)

        PT = PT.drop_duplicates(subset=['EASI Site Code'])

        PT = PT[["EASI Site Code"]]
        Output_AVERAGE_E_Bill_DF = Output_AVERAGE_E_Bill_DF[["EASI Site Code"]]

        frames = [PT, Output_AVERAGE_E_Bill_DF]
        PT = self.pd.concat(frames, sort=False)

        PT = PT.drop_duplicates(subset='EASI Site Code')
            
        n = 0
        for i in Month_List:
            if n == 0:
                PT1 = PT1.drop_duplicates(subset='EASI Site Code')
                PT = self.pd.merge(PT, PT1[["EASI Site Code", "Total Amount"]], on="EASI Site Code", how="left")
                PT.rename(columns={"Total Amount":"Advanced " + i}, inplace=True)
            elif n == 1:
                PT2 = PT2.drop_duplicates(subset='EASI Site Code')
                PT = self.pd.merge(PT, PT2[["EASI Site Code", "Total Amount"]], on="EASI Site Code", how="left")
                PT.rename(columns={"Total Amount":"Advanced " + i}, inplace=True)
            elif n == 2:
                PT3 = PT3.drop_duplicates(subset='EASI Site Code')
                PT = self.pd.merge(PT, PT3[["EASI Site Code", "Total Amount"]], on="EASI Site Code", how="left")
                PT.rename(columns={"Total Amount":"Advanced " + i}, inplace=True)
            n = n + 1


        for i in Month_List:
            Output_AVERAGE_E_Bill = Output_AVERAGE_E_Bill.drop_duplicates(subset='EASI Site Code')
            PT = self.pd.merge(PT, Output_AVERAGE_E_Bill[["EASI Site Code", "Total-" + i]], on="EASI Site Code", how="left")
            PT.rename(columns={"Total-" + i: "Actual " + i}, inplace=True)
            
        PT["Total Actual Bill"] = ""
        PT["Total Advanced Bill"] = ""
        PT["Credit/Debit"] = ""
        for i in range(len(PT)):
            if(str(PT.iloc[i, 1]) == "nan"):
                PT.iloc[i, 1] = 0
            if(str(PT.iloc[i, 2]) == "nan"):
                PT.iloc[i, 2] = 0
            if(str(PT.iloc[i, 3]) == "nan"):
                PT.iloc[i, 3] = 0
            if(str(PT.iloc[i, 4]) == "nan"):
                PT.iloc[i, 4] = 0
            if(str(PT.iloc[i, 5]) == "nan"):
                PT.iloc[i, 5] = 0
            if(str(PT.iloc[i, 6]) == "nan"):
                PT.iloc[i, 6] = 0
            PT.iloc[i, 7] = PT.iloc[i, 1] + PT.iloc[i, 2] + PT.iloc[i, 3]
            PT.iloc[i, 8] = PT.iloc[i, 4] + PT.iloc[i, 5] + PT.iloc[i, 6]
            PT.iloc[i, 9] = PT.iloc[i, 7] - PT.iloc[i, 8]
        
        PT = PT[["EASI Site Code", "Advanced "+ str(Month_List[0]), "Advanced "+str(Month_List[1]), "Advanced "+str(Month_List[2]), "Total Advanced Bill", "Actual "+str(Month_List[0]), "Actual "+str(Month_List[1]), "Actual "+str(Month_List[2]), "Total Actual Bill", "Credit/Debit"]]
        print(PT.head(10))
        # Except Submeter Bill
        SUBMETER_BILL_DF.rename(columns={"Edotco ID":"EASI Site Code"}, inplace=True)
        SUBMETER_BILL_DF = SUBMETER_BILL_DF.drop_duplicates(subset='EASI Site Code')
        PT = self.pd.merge(PT, SUBMETER_BILL_DF[["EASI Site Code", "Total bill amount with PF charge{(e+f+g)}"]], on="EASI Site Code", how="left") # 10

        PT["Status"] = ""
        for i in range(len(PT)):
            if(PT.iloc[i, 10] > 0):
                PT.iloc[i, 11] = "OK"

        PT = PT[PT["Status"] != "OK"]
        PT.drop(['Status', 'Total bill amount with PF charge{(e+f+g)}'], axis=1, inplace=True)
        return PT