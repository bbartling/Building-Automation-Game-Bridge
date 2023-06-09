## This script is to replicate a fake air handling unit BACnet points to test/debug on a test bench IoT applications and/or edge device FDD algorithms. The code uses the LBNL dataset for testing fault detection algorithms (See PDF lbnldatasynthesisinventory) where data is read (from the CSV file `MZVAV-1.csv`) and then expressed as a discoverable BACnet point that updates every 60 seconds for each row in the CSV file. When every row is read in the CSV file the data being represented in BACnet starts over at row 0 in a continous loop. Note the supply fan flow BACnet is a random value between 975 and 1025 to represent a fan operating around 10000 CFM. Pip install BAC0, pandas, and run app with `$ python fake_ahu.py.` Should work on Windows or Linux, tested with Python 3.10.6

### JCI point naming convention
* `"DAP-SP"` (discharge air pressure setpoint) 
* `"DAP-P"` (discharge air pressure) 
* `"SA-T"` (discharge air temperature sensor) 
* `"SAT-SP"` (discharge air temperature setpoint) 
* `"MA-T"` (mix air temperature sensor) 
* `"RA-T"` (return air temperature sensor) 
* `"HTG-O"` (heat valve command) 
* `"CLG-O"` (cooling valve command) 
* `"SF-C"` (discharge fan vfd command) 
* `"SF-S"` (discharge fan vfd status) 
* `"SF-O"` (discharge fan vfd speed) 
* `"RF-C"` (return fan vfd command) 
* `"RF-S"` (return fan vfd status) 
* `"RF-O"` (return fan vfd speed) 
* `"SA-FLOW"` (disharge fan air flow station) 






