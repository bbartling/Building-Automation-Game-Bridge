import BAC0
import time
import random

from BAC0.core.devices.local.models import (
    analog_output,
    analog_value,
    binary_input,
    analog_input,
    binary_output
)

from BAC0.tasks.RecurringTask import RecurringTask
from bacpypes.primitivedata import Real

import pandas as pd


# should work on Linux or Windows run with
# $ python fake_ahu.py

CSV_FILE_NAME = "./MZVAV-1.csv"
df = pd.read_csv(CSV_FILE_NAME, index_col="Date", parse_dates=True)
print("CSV file length is ",df.shape[1])

# point mapping inside CSV File names
DF_SA_T = "AHU: Supply Air Temperature"
DF_SAT_SP = "AHU: Supply Air Temperature Set Point"
DF_OA_T = "AHU: Outdoor Air Temperature"
DF_MA_T = "AHU: Mixed Air Temperature"
DF_RA_T = "AHU: Return Air Temperature"
DF_SF_S = "AHU: Supply Air Fan Status"
DF_RF_S = "AHU: Return Air Fan Status"
DF_SF_O = "AHU: Supply Air Fan Speed Control Signal"
DF_RF_O = "AHU: Return Air Fan Speed Control Signal"
DF_DPR_O = "AHU: Outdoor Air Damper Control Signal"
DF_CLG_o = "AHU: Cooling Coil Valve Control Signal"
DF_HTG_O = "AHU: Heating Coil Valve Control Signal"
DF_DAP_SP = "AHU: Supply Air Duct Static Pressure Set Point"
DF_DAP_P = "AHU: Supply Air Duct Static Pressure"


# G36 AHU required input points
points = [
    "DAP-SP",
    "DAP-P",
    "SA-T",
    "SAT-SP",
    "MA-T",
    "RA-T",
    "HTG-O",
    "CLG-O",
    "SF-C",
    "SF-S",
    "SF-O",
    "RF-C",
    "RF-S",
    "RF-O",
    "SA-FLOW"
    ]


class ChangeValues(object):
    
    def __init__(self,df):
        self.current_row = 0
        self.df = df
        self.df_length = self.df.shape[1]
        
    def match_df_to_bacnet(self,_object,value):
        point = bacnet.this_application.get_object_name(_object)
        point.presentValue = Real(value)
        bacnet._log.info(f'{_object} is {point.presentValue}')
        
    
    def change_values(self):
        df_row_data = self.df.iloc[self.current_row]
        print(f'df_row_data is {df_row_data}')
        
        for i in range(len(points)):
            
            _object = points[i]
            
            if _object == "DAP-SP":
                value = df_row_data[DF_DAP_SP]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "DAP-P":
                value = df_row_data[DF_DAP_P]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "SA-T":
                value = df_row_data[DF_SA_T]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "SAT-SP":
                value = df_row_data[DF_SAT_SP]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "MA-T":
                value = df_row_data[DF_MA_T]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "RA-T":
                value = df_row_data[DF_RA_T]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "OA-T":
                value = df_row_data[DF_OA_T]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "HTG-O":
                value = df_row_data[DF_HTG_O]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "CLG-O":
                value = df_row_data[DF_CLG_o]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "SF-O":
                value = df_row_data[DF_SF_O]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "SF-C":
                value = df_row_data[DF_SF_S]
                point = bacnet.this_application.get_object_name(_object)
                if value == 1:
                    point.presentValue = "active"
                else:
                    point.presentValue = "inactive"
                bacnet._log.info(f'{_object} is {point.presentValue}')
                
            if points[i] == "SF-S":
                value = df_row_data[DF_SF_S]
                point = bacnet.this_application.get_object_name(_object)
                if value == 1:
                    point.presentValue = "active"
                    bacnet._log.info(f'{_object} is {point.presentValue}')
                    
                    flow_station_value = random.randrange(975, 1025, 1)
                    self.match_df_to_bacnet("SA-FLOW",flow_station_value)
                    
                else:
                    point.presentValue = "inactive"
                    self.match_df_to_bacnet("SA-FLOW",0)
                    bacnet._log.info(f'{_object} is {point.presentValue}')
                
            if points[i] == "RF-O":
                value = df_row_data[DF_RF_O]
                self.match_df_to_bacnet(_object,value)
                
            if points[i] == "RF-C":
                value = df_row_data[DF_RF_S]
                point = bacnet.this_application.get_object_name(_object)
                if value == 1:
                    point.presentValue = "active"
                else:
                    point.presentValue = "inactive"
                bacnet._log.info(f'{_object} is {point.presentValue}')
                
            if points[i] == "RF-S":
                value = df_row_data[DF_RF_S]
                point = bacnet.this_application.get_object_name(_object)
                if value == 1:
                    point.presentValue = "active"
                else:
                    point.presentValue = "inactive"
                bacnet._log.info(f'{_object} is {point.presentValue}')
                
        # if all of the csv file has expired over start over
        if self.current_row == self.df_length:
            self.current_row = 0
        else:     
            self.current_row += 1


# create AHU duct pressure setpoint point
_new_objects = analog_value(
    name="DAP-SP",
    properties={"units": "inchesOfWater"},
    description="AHU Duct Pressure Setpoint",
    presentValue=1, is_commandable=True
)

# create AHU duct pressure
_new_objects = analog_input(
    name="DAP-P",
    properties={"units": "inchesOfWater"},
    description="AHU Duct Pressure",
    presentValue=1, is_commandable=False
)

# create AHU supply temp
_new_objects = analog_input(
    name="SA-T",
    properties={"units": "degreesFahrenheit"},
    description="AHU Duct Supply Temp",
    presentValue=75, is_commandable=False
)

# create AHU supply temp setpoint
_new_objects = analog_value(
    name="SAT-SP",
    properties={"units": "degreesFahrenheit"},
    description="AHU Duct Supply Setpoint",
    presentValue=75, is_commandable=True
)

# create AHU mix temp
_new_objects = analog_input(
    name="MA-T",
    properties={"units": "degreesFahrenheit"},
    description="AHU Duct Mix Temp",
    presentValue=75, is_commandable=False
)

# create AHU return temp
_new_objects = analog_input(
    name="RA-T",
    properties={"units": "degreesFahrenheit"},
    description="AHU Duct Return Temp",
    presentValue=75, is_commandable=False
)

# create AHU out temp
_new_objects = analog_input(
    name="OA-T",
    properties={"units": "degreesFahrenheit"},
    description="AHU Outside Air Temp",
    presentValue=75, is_commandable=False
)

# create AHU heating valve
_new_objects = analog_output(
    name="HTG-O",
    properties={"units": "percent"},
    description="AHU Heating Valve Command",
    presentValue=0, is_commandable=True
)

# create AHU cooling valve
_new_objects = analog_output(
    name="CLG-O",
    properties={"units": "percent"},
    description="AHU Cooling Valve Command",
    presentValue=0, is_commandable=True
)

# create AHU supply fan VFD speed
_new_objects = analog_output(
    name="SF-O",
    properties={"units": "percent"},
    description="AHU Supply Fan VFD Speed",
    presentValue=75, is_commandable=True
)

# create AHU fan VFD run command
_new_objects = binary_output(
    name="SF-C",
    description="AHU Supply Fan Command",
    presentValue=True, is_commandable=True
)

# create AHU fan status input
_new_objects = binary_input(
    name="SF-S",
    description="AHU Supply Fan Status",
    presentValue=True, is_commandable=False,
)

# create AHU return fan VFD speed
_new_objects = analog_output(
    name="RF-O",
    properties={"units": "percent"},
    description="AHU Return Fan VFD Speed",
    presentValue=60, is_commandable=True
)

# create AHU return fan VFD run command
_new_objects = binary_output(
    name="RF-C",
    description="AHU Return Fan Command",
    presentValue=True, is_commandable=True
)

# create AHU return fan status input
_new_objects = binary_input(
    name="RF-S",
    description="AHU Return Fan Status",
    presentValue=True, is_commandable=False,
)

# create AHU supply fan flow station
# OR can be totalized VAV box air flows
_new_objects = analog_input(
    name="SA-FLOW",
    properties={"units": "cubicFeetPerMinute"},
    description="AHU Supply Fan Air Flow",
    presentValue=75, is_commandable=False
)


# create app
#bacnet = BAC0.lite(ip='10.0.2.20/24',deviceId='2021')
bacnet = BAC0.lite()

_new_objects.add_objects_to_application(bacnet)
bacnet._log.info("APP Created Success!")

cv = ChangeValues(df)
cv.change_values()

def main():
    task1 = RecurringTask(cv.change_values, delay=60)
    task1.start()

    while True:

        time.sleep(10)


if __name__ == "__main__":
    main()

