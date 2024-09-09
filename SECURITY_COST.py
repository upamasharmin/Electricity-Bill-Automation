class SECURITY_COST:
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

    def SERVICE_FEE_SECURITY_COST(self, SECURITY_BILL_DF, PriceBook):
        SECURITY_BILL_DF["Use Type"] = SECURITY_BILL_DF["Use Type"].str.lower()
        SECURITY_BILL_DF = SECURITY_BILL_DF[SECURITY_BILL_DF["Use Type"] == "pass through site"]
        return SECURITY_BILL_DF