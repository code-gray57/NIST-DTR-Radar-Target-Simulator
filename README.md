# NIST-DTR-Radar-Target-Simulator
Introduction
---

__NIST DTR Radar Target Simulator__ is an application that simulates moving vehicles on roads using sine waves for the purpose of testing the accuracy of radar guns.

The application allows input of variable data about the vehicle - such as the speed and direction (coming to or going away from the radar) - and creates sine waves based off this information that can be read by a radar gun as a simulation of a vehicle. 

There are two simulation types that are available in the application: _Simple_, for simulating one vehicle only, and _Advanced_, for simulating up to three vehicles.

* The __*Simple*__ simulation allows the user to specify the speed of the vehicle, the direction it is going in respect to the radar gun (either away or towards), how long the created sine wave should play, and the transmit frequency band (K, Ka, or X) of the radar gun.


* The __*Advanced*__ simulation allows the user to specify the data mentioned in the Simple simulation on up to three vehicles and also allows the user to specify the amplitude for each sine wave (which is used to determine the distance of the vehicle away from the radar gun).

##### NOTE:
While this application is stand-alone in terms of execution and creates sine waves for simulating vehicles, the created sine waves cannot be used as simulations unless specific hardware is used in conjuction with this application. 


Installation
---

**_The installer can run on the following computer versions:_**  
Windows 7  
Windows 10   

(Windows Vista and 8 may potentially work, but this has not been confirmed).

_Steps:_

- Download the installer
- Run the installer (double-click the file)
- Follow the installation instructions. Most or all of the time you will simply hit Next
- The software is now on your computer. To run it, double click the shortcuts on either the desktop or start menu.

###### Installer created using *Inno Setup (v. 5.5.9)*


Overview
---

_A brief overview on how to use the DTR Radar Simulator application_

__Simple Simulation:__

![simple_window](http://imgur.com/Hcojw9b.png)

Entries:

* Speed  
    Input the speed the vehicle simulation will be moving at (in either miles per hour or kilometers per hour)
    
    
* Duration  
	Input how long the simulation should last for (in seconds)
    
Check Buttons:

* Metric  
	Switches between English units for speed (miles per hour) and metric (kilometers per hour). Checking the box will have the simulation use metric, and unchecked English. The label of each window that tells the units will change to reflect the units used (mph or kph).


Radio Buttons:

* Approaching / Receding  
	Select whether the vehicle simulation will be approaching (moving towards) or receding from (moving away) from the radar gun
    
    
* Transmit Frequency  
	Select the transmit frequency used by the radar gun (default is K-Band)

Buttons:

* Switch – Switch to Advanced Sim  
	Switches to the advanced simulation
* Run  
	Runs the simulation using the inputted data.

__Advanced Simulation:__

![advanced_window](http://imgur.com/sftvRdv.png)

Entries:

* Duration
	Input how long the entire simulation should last for (in seconds)
* Speed  
	Input the speed for each vehicle (in either miles per hour or kilometers per hour) – one vehicle for each entry
* Amplitude  
	Input the amplitude of the simulation sine wave – one vehicle for each entry (used to detail the distance of the vehicle from the radar gun)

Check Buttons:

* Metric  
	Switches between English units for speed (miles per hour) and metric (kilometers per hour). Checking the box will have the simulation use metric, and unchecked English. The label of each window that tells the units will change to reflect the units used (mph or kph).
    

* Receding  
	Box is checked if the vehicle is receding from the radar gun, unchecked it if is approaching the vehicle – one for each vehicle (default is approaching)

Radio Buttons:

* Transmit Frequency  
	Select the transmit frequency used by the radar gun (default is K-Band)

Buttons:

* Switch – Switch to Simple Sim  
	Switches to the simple simulation
* Run  
	Runs the simulation using the inputted data.

Authors
---
- Source Code by Robert L. Gray III
- original MATLAB source code and calculations by John Jendzurski

Packages
---

Software created with Python (v. 2.7)

Packages included:

- Ocempgui    - For GUI creation
- Pygame      - coupled with and required for Ocempgui for GUI creation
- NumPy       - For computation of sine waves and required for Ocempgui functionality
- Sounddevice - For playing created sine waves


License
---
Pygame - distributed under LGPL version 2.1

OcempGUI - Copyright © 2005-2007 Marcus von Appen

Numpy - Copyright © 2005, NumPy Developers. All rights reserved.

Sounddevice - Copyright © 2015-2017 Matthias Geier

- See [LICENSE.txt](https://github.com/code-gray57/NIST-DTR-Radar-Target-Simulator/blob/master/LICENSE.txt) for the terms of use for the application
- See [PKG-LICENSE.txt](https://github.com/code-gray57/NIST-DTR-Radar-Target-Simulator/blob/master/PKG-LICENSE.txt) for the complete license notice for the packages

