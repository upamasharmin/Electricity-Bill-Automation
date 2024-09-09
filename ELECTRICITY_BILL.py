class ELECTRICITY_BILL:
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

    # def SERVICE_FEE_ELECTRICITY_BILL(self, DTC, PriceBook):
    #     DF = DTC.copy()
    #     DF["Claimed RH in Decimal"] = "" # 5
    #     for i in range(len(DF)):
    #         ''' Check the Claimed RH '''
    #         SWITCH = 0 
    #         try:
    #             RH = len(str(DF.iloc[i, 4]).split(":"))
    #             SWITCH = 1
    #         except:
    #             SWITCH = 0
    #         '''Generate Claimed RH in Decimal '''
    #         if(SWITCH == 1):
    #             RH = len(str(DF.iloc[i, 4]).split(":"))
    #             print(int(RH[0]))
    #             DECIMAL_RH = int(RH[0]) + (int(RH[1]) / 60) + (int(RH[2]) / 3600)
    #             DF.iloc[i, 5] = DECIMAL_RH # Claimed RH in Decimal # 5
    #     return DF
    
    def ACTUAL_E_BILL(self, date_input, dir_path, input_file_path, eFilePath):
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
                  DF1 = self.pd.read_excel(dir_path + input_file_path + eFilePath +str(int(date_input[4:8]) - 1) + "\\"+ "Actual E-Bill " + str(i) + "-" + Month_List[0] + ".xlsx")
                else:
                  DF1 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Actual E-Bill " + str(i) + "-" + date_input[4:8] + ".xlsx")
            elif(n == 1):
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF2 = self.pd.read_excel(dir_path + input_file_path + eFilePath +str(int(date_input[4:8]) - 1) + "\\"+ "Actual E-Bill " + str(i) + "-" + Month_List[0] + ".xlsx")
                else:
                  DF2 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Actual E-Bill " + str(i) + "-" + date_input[4:8] + ".xlsx")
            elif(n == 2):
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF3 = self.pd.read_excel(dir_path + input_file_path + eFilePath +str(int(date_input[4:8]) - 1) + "\\"+ "Actual E-Bill " + str(i) + "-" + Month_List[0] + ".xlsx")
                else:
                  DF3 = self.pd.read_excel(dir_path + input_file_path + eFilePath + date_input[4:8] + "\\" + "Actual E-Bill " + str(i) + "-" + date_input[4:8] + ".xlsx")
            n = n + 1

        frames = [DF1, DF2, DF3]
        DF = self.pd.concat(frames, sort=False)

        

        DF = DF.drop_duplicates(subset='EASI Site Code', keep="first")

        DF = DF[["EASI Site Code", "Meter Owner"]]

        n = 0
        for i in Month_List:
            if(n == 0):
                DF1 = DF1.drop_duplicates(subset='EASI Site Code', keep="first")
                DF = self.pd.merge(DF, DF1[["EASI Site Code", "Amount"]], on="EASI Site Code", how="left")
                DF = self.pd.merge(DF, DF1[["EASI Site Code", "VAT"]], on="EASI Site Code", how="left")
                DF = self.pd.merge(DF, DF1[["EASI Site Code", "Consumption"]], on="EASI Site Code", how="left")
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"Amount":"Amount-" + i + "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"Amount":"Amount-" + i + "-" +date_input[4:8]}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"VAT":"VAT-" + i + "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"VAT":"VAT-" + i + "-" + date_input[4:8]}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"Consumption":"Consumption-" + i+ "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"Consumption":"Consumption-" + i + "-" + date_input[4:8]}, inplace=True)
            elif(n == 1):
                DF2 = DF2.drop_duplicates(subset='EASI Site Code', keep="first")
                DF = self.pd.merge(DF, DF2[["EASI Site Code", "Amount"]], on="EASI Site Code", how="left")
                DF = self.pd.merge(DF, DF2[["EASI Site Code", "VAT"]], on="EASI Site Code", how="left")
                DF = self.pd.merge(DF, DF2[["EASI Site Code", "Consumption"]], on="EASI Site Code", how="left")
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"Amount":"Amount-" + i + "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"Amount":"Amount-" + i + "-" +date_input[4:8]}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"VAT":"VAT-" + i + "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"VAT":"VAT-" + i + "-" + date_input[4:8]}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"Consumption":"Consumption-" + i+ "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"Consumption":"Consumption-" + i + "-" + date_input[4:8]}, inplace=True)
            elif(n == 2):
                DF3 = DF3.drop_duplicates(subset='EASI Site Code', keep="first")
                DF = self.pd.merge(DF, DF3[["EASI Site Code", "Amount"]], on="EASI Site Code", how="left")
                DF = self.pd.merge(DF, DF3[["EASI Site Code", "VAT"]], on="EASI Site Code", how="left")
                DF = self.pd.merge(DF, DF3[["EASI Site Code", "Consumption"]], on="EASI Site Code", how="left")
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"Amount":"Amount-" + i + "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"Amount":"Amount-" + i + "-" +date_input[4:8]}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"VAT":"VAT-" + i + "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"VAT":"VAT-" + i + "-" + date_input[4:8]}, inplace=True)
                if(date_input[0:3] == "Jan" or date_input[0:3] == "Feb"):
                  DF.rename(columns={"Consumption":"Consumption-" + i+ "-" + str(int(date_input[4:8]) - 1)}, inplace=True)
                else:
                  DF.rename(columns={"Consumption":"Consumption-" + i + "-" + date_input[4:8]}, inplace=True)
            n = n + 1
        return DF