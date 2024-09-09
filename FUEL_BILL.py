class FUEL_BILL:
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

    def FUEL_BILL(self, FUEL_PASS_THROUGH_DF, DTC_DF, PriceBook, date_input):
        DF = DTC_DF.copy()
        # Fuel Passthorugh File
        FUEL_PASS_THROUGH_DF = FUEL_PASS_THROUGH_DF[["Robi Site Code", "Edotco Site Code", str(date_input)[0:3] + "'" + str(date_input)[6:8]]]
        DTC_DF.rename(columns={"EASI Site Code":"Edotco Site Code"}, inplace=True)
        FUEL_PASS_THROUGH_DF = self.pd.merge(FUEL_PASS_THROUGH_DF, DTC_DF[["Edotco Site Code", "Colo Count for Fuel Discount"]], on="Edotco Site Code", how="left")
        FUEL_PASS_THROUGH_DF = FUEL_PASS_THROUGH_DF[["Robi Site Code", "Edotco Site Code", "Colo Count for Fuel Discount",str(date_input)[0:3] + "'" + str(date_input)[6:8]]]
        FUEL_PASS_THROUGH_DF["Robi will share (without VAT rebate)"] = ""
        for i in range(len(FUEL_PASS_THROUGH_DF)):
            # if(FUEL_PASS_THROUGH_DF.iloc[i, 3]):
            if(str(FUEL_PASS_THROUGH_DF.iloc[i, 2]) != "nan"):
                if(FUEL_PASS_THROUGH_DF.iloc[i, 2] == 0):
                    FUEL_PASS_THROUGH_DF.iloc[i, 4] = 0
                else:
                    if(str(FUEL_PASS_THROUGH_DF.iloc[i, 3]) != "nan"):
                        FUEL_PASS_THROUGH_DF.iloc[i, 4] = FUEL_PASS_THROUGH_DF.iloc[i, 3] / FUEL_PASS_THROUGH_DF.iloc[i, 2]

        return FUEL_PASS_THROUGH_DF
    
    def FUEL_BILL_RECON(self, DTC_DF, date_input, dir_path, input_file_path, FUEL_PASS_THROUGH_DF, eFilePath):
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

        DF1 = self.pd.DataFrame()
        DF2 = self.pd.DataFrame()
        DF3 = self.pd.DataFrame()

        n = 0
        for i in Month_List:
            if(n == 0):
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                    DF1 = self.pd.read_excel(dir_path + input_file_path + eFilePath + str(int(date_input[4:8]) - 1)  + "\\" + "Monthly Advance Fuel Bill_" + Month_List[0] + ".xlsx")
                else:
                    DF1 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Monthly Advance Fuel Bill_" + str(i) + " " + date_input[4:8] + ".xlsx")
            elif(n == 1):
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                    DF2 = self.pd.read_excel(dir_path + input_file_path + eFilePath + str(int(date_input[4:8]) - 1)  + "\\" + "Monthly Advance Fuel Bill_" + Month_List[0] + ".xlsx")
                else:
                    DF2 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Monthly Advance Fuel Bill_" + str(i) + " " + date_input[4:8] + ".xlsx")
            elif(n == 2):
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                    DF3 = self.pd.read_excel(dir_path + input_file_path + eFilePath + str(int(date_input[4:8]) - 1)  + "\\" + "Monthly Advance Fuel Bill_" + Month_List[0] + ".xlsx")
                else:
                    DF3 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Monthly Advance Fuel Bill_" + str(i) + " " + date_input[4:8] + ".xlsx")
            n = n + 1

        
        frames = [DF1, DF2, DF3]
        DF = self.pd.concat(frames, sort=False)

        DF = DF.drop_duplicates(subset='Edotco Site Code', keep="first")

        DF = DF[["Robi Site Code", "Edotco Site Code"]]

        DF1 = DF1.drop_duplicates(subset='Edotco Site Code', keep="first")
        DF2 = DF2.drop_duplicates(subset='Edotco Site Code', keep="first")
        DF3 = DF3.drop_duplicates(subset='Edotco Site Code', keep="first")
        # FUEL_PASS_THROUGH_DF.rename(columns={"Edotco Site Code":"Edotco Site Code"}, inplace=True)
        FUEL_PASS_THROUGH_DF = FUEL_PASS_THROUGH_DF.drop_duplicates(subset='Edotco Site Code', keep="first")

        n = 0
        for i in Month_List:
            if(n == 0):
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Consumables from other operator-"]], on="Edotco Site Code", how="left")
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Total cost (5% VAT included)"]], on="Edotco Site Code", how="left")
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Robi will share (without VAT rebate)"]], on="Edotco Site Code", how="left")
                DF.rename(columns={"Consumables from other operator-":"Consumables from other operator-" + i}, inplace=True)
                DF.rename(columns={"Total cost (5% VAT included)":"Total cost (5% VAT included)" + i}, inplace=True)
                DF.rename(columns={"Robi will share (without VAT rebate)":"Robi will share (without VAT rebate)" + i}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                 DF = self.pd.merge(DF, FUEL_PASS_THROUGH_DF[["Edotco Site Code", str(i) + "'" + str(int(date_input[6:8]) - 1)]], on="Edotco Site Code", how="left")	  
                else:
                 DF = self.pd.merge(DF, FUEL_PASS_THROUGH_DF[["Edotco Site Code", str(i) + "'" + date_input[6:8]]], on="Edotco Site Code", how="left")
                DF["Robi will pay - " + i] = ""
                DF["Need to adjust - " + i] = ""

                v1 = 2
                v2 = 3
                v3 = 5
                v4 = 6
                v5 = 7
                v6 = 4
                for i in range(len(DF)):
                    if(str(DF.iloc[i, v1]) != "nan"):
                        if(DF.iloc[i, v1] == 0):
                            DF.iloc[i, v4] = 0
                        else:
                            if(str(DF.iloc[i, v3]) != "nan"):
                                DF.iloc[i, v4] = DF.iloc[i, v3] / DF.iloc[i, v1]
                            else:
                                DF.iloc[i, v4] = 0
                    if(str(DF.iloc[i, v4]) != "nan" and str(DF.iloc[i, v4]) != ""):
                        if(DF.iloc[i, v6] == "nan" or str(DF.iloc[i, v6]) == ""):
                            DF.iloc[i, v5] = 0
                        else:
                            DF.iloc[i, v5] = DF.iloc[i, v4] - DF.iloc[i, v6]
                    else:
                        if(str(DF.iloc[i, v6]) == "nan" or str(DF.iloc[i, v6]) == ""):
                            DF.iloc[i, v5] = 0
                        else:
                            DF.iloc[i, v5] = DF.iloc[i, v6]
            elif(n == 1):
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Consumables from other operator-"]], on="Edotco Site Code", how="left")
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Total cost (5% VAT included)"]], on="Edotco Site Code", how="left")
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Robi will share (without VAT rebate)"]], on="Edotco Site Code", how="left")
                DF.rename(columns={"Consumables from other operator-":"Consumables from other operator-" + i}, inplace=True)
                DF.rename(columns={"Total cost (5% VAT included)":"Total cost (5% VAT included)" + i}, inplace=True)
                DF.rename(columns={"Robi will share (without VAT rebate)":"Robi will share (without VAT rebate)" + i}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                 DF = self.pd.merge(DF, FUEL_PASS_THROUGH_DF[["Edotco Site Code", str(i) + "'" + str(int(date_input[6:8]) - 1)]], on="Edotco Site Code", how="left")
                else:
                 DF = self.pd.merge(DF, FUEL_PASS_THROUGH_DF[["Edotco Site Code", str(i) + "'" + date_input[6:8]]], on="Edotco Site Code", how="left")
                DF["Robi will pay - " + i] = ""
                DF["Need to adjust - " + i] = ""
                v1 = 2 + 6
                v2 = 3 + 6
                v3 = 5 + 6
                v4 = 6 + 6
                v5 = 7 + 6
                for i in range(len(DF)):
                    if(str(DF.iloc[i, v1]) != "nan"):
                        if(DF.iloc[i, v1] == 0):
                            DF.iloc[i, v4] = 0
                        else:
                            if(str(DF.iloc[i, v3]) != "nan"):
                                DF.iloc[i, v4] = DF.iloc[i, v3] / DF.iloc[i, v1]
                    if(str(DF.iloc[i, v4]) != "nan" and str(DF.iloc[i, v4]) != ""):
                        if(DF.iloc[i, v6] == "nan" or str(DF.iloc[i, v6]) == ""):
                            DF.iloc[i, v5] = 0
                        else:
                            DF.iloc[i, v5] = DF.iloc[i, v4] - DF.iloc[i, v6]
                    else:
                        if(str(DF.iloc[i, v6]) == "nan" or str(DF.iloc[i, v6]) == ""):
                            DF.iloc[i, v5] = 0
                        else:
                            DF.iloc[i, v5] = DF.iloc[i, v6]
            elif(n == 2):
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Consumables from other operator-"]], on="Edotco Site Code", how="left")
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Total cost (5% VAT included)"]], on="Edotco Site Code", how="left")
                DF = self.pd.merge(DF, DF1[["Edotco Site Code", "Robi will share (without VAT rebate)"]], on="Edotco Site Code", how="left")
                DF.rename(columns={"Consumables from other operator-":"Consumables from other operator-" + i}, inplace=True)
                DF.rename(columns={"Total cost (5% VAT included)":"Total cost (5% VAT included)" + i}, inplace=True)
                DF.rename(columns={"Robi will share (without VAT rebate)":"Robi will share (without VAT rebate)" + i}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                 DF = self.pd.merge(DF, FUEL_PASS_THROUGH_DF[["Edotco Site Code", str(i) + "'" + str(int(date_input[6:8]) - 1)]], on="Edotco Site Code", how="left")
                else:
                 DF = self.pd.merge(DF, FUEL_PASS_THROUGH_DF[["Edotco Site Code", str(i) + "'" + date_input[6:8]]], on="Edotco Site Code", how="left")
             
                    
                    
                DF["Robi will pay - " + i] = ""
                DF["Need to adjust - " + i] = ""
                v1 = 2 + 6 + 6
                v2 = 3 + 6 + 6
                v3 = 5 + 6 + 6
                v4 = 6 + 6 + 6
                v5 = 7 + 6 + 6
                for i in range(len(DF)):
                    if(str(DF.iloc[i, v1]) != "nan"):
                        if(DF.iloc[i, v1] == 0):
                            DF.iloc[i, v4] = 0
                        else:
                            if(str(DF.iloc[i, v3]) != "nan"):
                                DF.iloc[i, v4] = DF.iloc[i, v3] / DF.iloc[i, v1]
                    if(str(DF.iloc[i, v4]) != "nan" and str(DF.iloc[i, v4]) != ""):
                        if(DF.iloc[i, v6] == "nan" or str(DF.iloc[i, v6]) == ""):
                            DF.iloc[i, v5] = 0
                        else:
                            DF.iloc[i, v5] = DF.iloc[i, v4] - DF.iloc[i, v6]
                    else:
                        if(str(DF.iloc[i, v6]) == "nan" or str(DF.iloc[i, v6]) == ""):
                            DF.iloc[i, v5] = 0
                        else:
                            DF.iloc[i, v5] = DF.iloc[i, v6]
            n = n + 1

        DF["TA"] = 0
        for i in range(len(DF)):
            if str(DF.iloc[i, 7]) == "nan":
                DF.iloc[i, 7] = 0
            if str(DF.iloc[i, 13]) == "nan":
                DF.iloc[i, 13] = 0
            if str(DF.iloc[i, 19]) == "nan":
                DF.iloc[i, 19] = 0
            DF.iloc[i, 20] = DF.iloc[i, 7] + DF.iloc[i, 13] + DF.iloc[i, 19]
        DF["Total Adjustment"] = ""
        DF.iloc[0, 21] = DF["TA"].sum()
        DF = DF.drop('TA', axis=1)
        return DF