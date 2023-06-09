# building-automation-helper
This is an unfinished concept idea for a (non-AI) chat interface to assist building operators in day-to-day tasks of operating the building technology systems.
![Alt text](/images/BAS_chat.PNG)

### Remote action via the chat interface
* "check ahu"
* "check zones"
* "check chiller plant"
* "check boiler plant"
* "check power"
* "check energy"
* "check overrides"
* "check all"
* "check faults"
* "adjust setpoint *"
* "command * off"
* "command * on"
* "demand response start"

### Chat interface
![Alt text](/images/interface.PNG)

### Architecture concept
* server communicates actions and recieves responses to client inside building with MQTT secure (MQTTs)
* chat interface is hosted by web server over HTTPS
![Alt text](/images/schematic.jpg)

### fake_bacnet_device
* For testing purposes on client based actions
* This app uses one of LBNLs FDD datasets to represent as a fake discoverable BACnet device. The sensor I/O data in JCI point naming convention dates every every 60 seconds read row by row in the LBNL CSV file. 
See LBNL PDF in subfolder.


## FUTURE ENDEAVORS

### Use LLM like chat GPT for chat dialog and logic:
* Cloud server to use back end API with chat GPT to manage chat dialogs
* Use an IoT service to communicate from building to cloud such as "things board" or the VOLTTRON framework

### Server hosting chat interface: 
* Develop a secure remote server that controls the bots actions which is operating autonomously behind the building's firewall. This server would enable efficient monitoring and control of the bot, including the ability to implement a kill switch if necessary. By ensuring the bot's operations can be managed remotely, it enhances the overall security and control of the system. Server to incorporate an OpenADR client feature to incorporate demand response control signals to the bot.

### Building Electrical Usage Optimization: 
* Expand the capabilities of the bot to optimize electrical usage within the building. This includes implementing strategies such as electrical load shedding, load shifting, and continuous load management. The bot will autonomously analyze energy consumption patterns and make adjustments based on predefined optimization algorithms. Integration with the remote server allows for real-time monitoring and fine-tuning of the electrical system.

### System-Level HVAC Optimization: 
* Extend the bot's capabilities to optimize the HVAC system at a system-level. This involves focusing on areas such as trim respond AHU (Air Handling Unit) fan duct pressure control, leaving temperature setpoint optimization, as well as chiller and boiler plant management. By utilizing advanced algorithms and real-time data analysis, the bot can optimize the HVAC system's performance, energy efficiency, and occupant comfort.

### Integration of Other Building Systems: 
* Expand the scope of the bot to integrate and manage other building systems beyond HVAC. This includes adjustable electrical loads such as lighting systems, battery storage systems, and ice storage systems. By incorporating these systems into the bot's control and optimization algorithms, it can create a holistic approach to energy management, maximizing efficiency, and reducing overall energy consumption.