class DTC_FRACTION_BILLING_AL:
    def __init__(self, pd, time, date, datetime, math, timedelta, calendar): 
        self.pd = pd
        self.time = time
        self.math = math
        self.date = date
        self.today = date.today()
        self.now = datetime.now()
        self.today = self.today.strftime("%d_%m_%Y")
        self.dt_string = self.now.strftime("%d/%m/%Y %H:%M:%S")
        self.timedelta = timedelta
        self.calendar = calendar

    # ------------------------------------------------------------------ #

    def PROCESS_DTC(self, DTC, invoice_date):
        # Cut of start date - 16th day of the previous month
        if invoice_date.month == 1:
            Cutoff_start_date = invoice_date.replace(year=invoice_date.year - 1, month=12, day=16)
        else:
            Cutoff_start_date = invoice_date.replace(month=invoice_date.month - 1, day=16)

        # Cut of end date - 15th day of the Invoice month
        Cutoff_end_date = Cutoff_start_date + self.timedelta(days=31)
        if Cutoff_end_date.day <= 15:
            Cutoff_end_date = Cutoff_end_date.replace(day=15)
        else:
            Cutoff_end_date = Cutoff_end_date.replace(month=Cutoff_end_date.month, day=15)

        # Convert the "Commencement Date" column to a datetime data type:
        DTC['Commencement Date'] = self.pd.to_datetime(DTC['Commencement Date'], errors='coerce')
        DTC['Tenant Decom Date'] = self.pd.to_datetime(DTC['Tenant Decom Date'], errors='coerce')

        # Filter the "Commencement Date" based on Cut of start date and end date:
        DTC = DTC[(DTC['Commencement Date'] <= Cutoff_end_date)]
        # DTC = DTC[(DTC['Project Name'] != "Legacy_507-New")]

        # Calculating the number of days in the invoice month, end date of the invoice month
        invoice_month = Cutoff_end_date.month
        days_in_invoice_month = self.calendar.monthrange(Cutoff_end_date.year, invoice_month)[1]
        last_day_of_invoice_month = self.calendar.monthrange(invoice_date.year, invoice_date.month)[1]
        end_date_of_month = invoice_date.replace(day=last_day_of_invoice_month)

        fraction_days_list = []
        for index, row in DTC.iterrows():
            # Rule 1 - OK
            if row['Commencement Date'] < Cutoff_start_date and self.pd.isnull(row['Tenant Decom Date']):
                fraction_days = days_in_invoice_month
            # Rule 2 - OK
            elif Cutoff_start_date < row['Commencement Date'] < invoice_date.replace(day=1) and self.pd.isnull(row['Tenant Decom Date']):
                fraction_days = (end_date_of_month - row['Commencement Date']).days + 1
            # Rule 3 - OK
            elif  row['Commencement Date'] > invoice_date.replace(day=1) and self.pd.isnull(row['Tenant Decom Date']):
                fraction_days = (end_date_of_month - row['Commencement Date']).days
            # Rule 4 - OK
            elif Cutoff_start_date < row['Commencement Date'] and row['Tenant Decom Date'] < Cutoff_end_date:
                fraction_days = (row['Tenant Decom Date'] - row['Commencement Date']).days + 1
            # Rule 5 - OK
            elif row['Commencement Date'] != 0 and self.pd.isnull(row['Tenant Decom Date']):
                fraction_days = days_in_invoice_month
            # Rule 6 - OK
            elif row['Commencement Date'] != 0 and  row['Tenant Decom Date'] < invoice_date.replace(day=1):
                fraction_days =  0
            # Rule 7 - OK
            elif row['Commencement Date'] != 0 and (invoice_date.replace(day=1) < row['Tenant Decom Date']):
                fraction_days = (row['Tenant Decom Date'] - invoice_date.replace(day=1)).days + 1
            fraction_days_list.append(fraction_days)
        DTC['Fraction Days'] = fraction_days_list
        DTC['Commencement Date'] = DTC['Commencement Date'].dt.strftime('%d-%b-%Y')
        DTC['RFAI Customer Acceptance Date'] = DTC['RFAI Customer Acceptance Date'].dt.strftime('%d-%b-%Y')
        DTC['Tenant Decom Date'] = DTC['Tenant Decom Date'].dt.strftime('%d-%b-%Y')
        DataList = [DTC, days_in_invoice_month]
        return DataList
