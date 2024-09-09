class PG_RH:
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

    def PG_RH(self, DTC, PriceBook, invoice_date):
        DF = DTC.copy()
        DF = DF[["Site_Code", "WFM TT",	"PG_Start_Time", "PG_End_Time",	"Claimed RH", "Claim Type",	"Site Type"]]
        DF["Claimed RH in Decimal"] = "" # 7
        for i in range(len(DF)):
            ''' Check the Claimed RH '''
            SWITCH = 0 
            try:
                RH = len(str(DF.iloc[i, 4]).split(":"))
                SWITCH = 1
            except:
                SWITCH = 0
            '''Generate Claimed RH in Decimal '''
            if(SWITCH == 1):
                RH = str(DF.iloc[i, 4]).split(":")
                DECIMAL_RH = float(RH[0]) + (float(RH[1]) / 60) + (float(RH[2]) / 3600)
                DF.iloc[i, 7] = DECIMAL_RH # Claimed RH in Decimal # 7
        
        # Summary
        SUMMARY = self.pd.DataFrame()
        data = [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""]]
        # Create the pandas DataFrame
        SUMMARY = self.pd.DataFrame(data, columns=["Item", "RH", "Fuel"])

        DF1 = DF[DF["Claim Type"] == "PGRH & Fuel claim"]
        DF2 = DF[DF["Claim Type"] == "PGRH claim"]
        DF3 = DF[DF["Claim Type"] == "Fuel claim"]

        # Total Claimed
        PB1 = PriceBook[PriceBook["Name of the Line Item"] == "Petrol Generator Runhour Claim"]
        PB2 = PriceBook[PriceBook["Name of the Line Item"] == "Petrol Generator Fuel Claim"]
        Total_Claimed_RH = DF1["Claimed RH in Decimal"].sum() + DF2["Claimed RH in Decimal"].sum()
        Total_Claimed_Fuel = (DF1["Claimed RH in Decimal"].sum() + DF3["Claimed RH in Decimal"].sum()) * PB2.iloc[0, 3]

        SUMMARY.iloc[0, 0] = "Total Claim"
        SUMMARY.iloc[0, 1] = Total_Claimed_RH
        SUMMARY.iloc[0, 2] = Total_Claimed_Fuel

        SUMMARY.iloc[1, 0] = "RH Baseline"
        SUMMARY.iloc[1, 1] = PB1.iloc[0, 4]
        SUMMARY.iloc[1, 2] = PB2.iloc[0, 4]

        SUMMARY.iloc[2, 0] = "Billable Claim"
        SUMMARY.iloc[2, 1] = SUMMARY.iloc[0, 1] - SUMMARY.iloc[1, 1]
        SUMMARY.iloc[2, 2] = SUMMARY.iloc[0, 2] - SUMMARY.iloc[1, 2]

        date_format = "%Y-%m-%d"
        a = self.datetime.strptime(str(invoice_date)[0:10], date_format)
        c = self.datetime.strptime(str(PB1.iloc[0, 10])[0:10], date_format)
        delta2 = a - c
        yearGap = self.math.floor(delta2.days / 365)

        SUMMARY.iloc[3, 0] = "Rate"
        SUMMARY.iloc[3, 1] = PB1.iloc[0, 1] * pow(float(PB1.iloc[0, 9]), yearGap)
        SUMMARY.iloc[3, 2] = PB2.iloc[0, 1]

        SUMMARY.iloc[4, 0] = "Passthrough %"
        SUMMARY.iloc[4, 1] = str(PB1.iloc[0, 5] * 100) + "%"
        SUMMARY.iloc[4, 2] = str(PB2.iloc[0, 5] * 100) + "%"

        SUMMARY.iloc[5, 0] = "Bill for the Month"
        SUMMARY.iloc[5, 1] = SUMMARY.iloc[2, 1] * SUMMARY.iloc[3, 1] * PB1.iloc[0, 5]
        SUMMARY.iloc[5, 2] = SUMMARY.iloc[2, 2] * SUMMARY.iloc[3, 2] * PB2.iloc[0, 5]
        return SUMMARY