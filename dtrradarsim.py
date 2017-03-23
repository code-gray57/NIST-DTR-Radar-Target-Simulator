# dtrradarsim.py - NIST DTR Radar Target Simulator
#
# By Robert L. Gray III

# Start Date: February 28, 2017
# Completed: March 11, 2017     (update on March 22, 2017)

# This program is used run simulations of vehicles using a graphical user interface (GUI) for testing handheld speed cameras (radar guns) for accuracy readings.
# The program simulates vehicles by creating sine (in reality, cosine) waves using numpy arrays by taking data inputted by the user and other standards built in.
# The program is also built partway like a module, as it can be called in other programs due to object-oriented programming. Most everything is done within objects,
# except for a few functions and one global constant (for the background color of the GUI).

# The original code and implementation created by John Jendzurski in MATLAB (2017).
# This code was implemented for portability (creation of executables and installer for easy distribution). This program also implements an 'advanced' window, allowing
# the user to choose multiple vehicles during the simulation and to specify the amplitude of each (which was not present in the original MATLAB code).

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
# NOTE ON ADVANCED WINDOW: while the default number of vehicles is three for the advanced window, and the only number used in this program, the code is set up to #
#                          allow any number of vehicle simulations with the advanced window. Of course, very high numbers are most definitely improbable and not  #
#                          that useful for this application.                                                                                                      #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

#-----Import needed modules and define global constants------#

#Import numpy and sounddevice for calulating the sine waves and playing them (respectively).
import numpy, sounddevice

#Import the OcempGUI gui modules
from ocempgui.widgets import *                          #For the GUI widgets
from ocempgui.widgets.Constants import *                #For GUI constants

GUI_COLOR = (234, 228, 223) #The background color of the GUI


#----------Start of Class Definitions----------#



#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
# This class is used to create a simple window, which is used to enter input about a single vehicle - its speed, which way it is going relative to the camera, #
# and for how long.                                                                                                                                            #
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

class SimpleWindow(object):
    """ A simple gui window, that allows the user to specify information regarding a single vehicle moving either towards or away from the speed camera. """

    def init(self, is_metric = False):
        """ This function is used to set up the window (initiate the object and instantiate all its attributes). This is used instead of a __init__ method since
it is needed to be called multiple times - every time the window is added again to the main window's frame.

The 'is_metric' optional parameter is used to change between English and Metric units. For the window, this just means switching between miles per hour and
kilometers per hour for the speed unit Label. If 'is_metric' is True, 'kph' is put as the text instead of 'mph'. The actual data conversion is done when creating
the sine wave. """

        self.speed_lbl = Label("Speed") #A label for the speed entry
        self.speed_entry = Entry()      #The entry (text field) where the user inputs the speed of the simulated vehicle
        self.s_unit_lbl = Label("mph")  #A label that details the units of measurement for the speed

        #Now, if 'is_metric' is True, then the units should be metric, so change the text of the unit label to kilometers per hour
        if is_metric:
            self.s_unit_lbl.text = "kph"

        self.dur_lbl = Label("Duration")    #A label for the duration entry
        self.dur_entry = Entry()            #The entry (text field) where the user inputs the duration for the simulated vehicle
        self.d_unit_lbl = Label("sec")      #A label that details the units of measurement for the duration

        #Here the two radio buttons that allow the user to choose whether the simulation is approaching or receding
        self.appro_rad = RadioButton("Approaching")
        self.recede_rad = RadioButton("Receding", self.appro_rad) #Add in the 'appro_rad' radio button to group the two together

        # Set up the tables for holding the widgets
        self.entry_table = Table(2, 3) #This table is to hold the text entries and associated labels

        #Add the associated widgets to the table (those for the text entries)
        self.entry_table.add_child(0, 0, self.speed_lbl)
        self.entry_table.add_child(0, 1, self.speed_entry)
        self.entry_table.add_child(0, 2, self.s_unit_lbl)
        self.entry_table.add_child(1, 0, self.dur_lbl)
        self.entry_table.add_child(1, 1, self.dur_entry)
        self.entry_table.add_child(1, 2, self.d_unit_lbl)

        self.rad_table = Table(2, 1) #This table is to hold the radio buttons

        self.rad_table.add_child(0, 0, self.appro_rad)
        self.rad_table.add_child(1, 0, self.recede_rad)
        

        self.main_table = Table(2, 1) #This is the main table for the window, which holds all the other tables.
        
        self.main_table.add_child(0, 0, self.entry_table) #Add the entry table first
        self.main_table.add_child(1, 0, self.rad_table)

    #--------------------------------------------------------------------------------------------------------#
    # This method is used to switch the text for the speed button from miles per hour to kilometers per hour #
    #--------------------------------------------------------------------------------------------------------#

    def switch_units(self, is_metric):
        """ This method switches the text for the speed button - between English and Metric. The passed parameter 'is_metric' determines which it should
be switched to. """
        if is_metric: #If the units should change to metric, put them in kilometers per hour
            self.s_unit_lbl.text = 'kph'
        else:
            self.s_unit_lbl.text = 'mph'


    #-------------------------------------------------------------------------#
    # Here are the method that return data from widgets (entered by the user) #
    #-------------------------------------------------------------------------#

    def get_speed(self):
        """ This method returns the text within the speed Entry widget. """
        return self.speed_entry.text

    def get_duration(self):
        """ This method returns the text within the duration Entry widget. """
        return self.dur_entry.text

    def get_direct(self):
        """ This method returns the direction that the vehicle is moving. Specifically, it returns True if it is approaching and False if it is receding. If neither
is active, None is returned."""
        if self.appro_rad.active:
            return True #To denote the vehicle is approaching the radar
        elif self.recede_rad.active:
            return False #To denote the vehicle is receding from the radar
        else: #If neither radio button has been selected, return None
            return None
        

    #---------------------------------------------------------------------------------------------------------------------------------------------------#
    # This is the method that returns the reference to the 'main_table' attribute. It is used to add the widgets of the simple window to the interface. #
    #---------------------------------------------------------------------------------------------------------------------------------------------------#
    
    def get_main_table(self):
        """ This method returns a reference to the 'main_table' Table attribute. """
        return self.main_table



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
# This class is used to create an advanced window, where data for multiple vehicles as well as extra data not asked for in the simple window. It takes a specific #
# number that details how many vehicles are to be used during that simulation, and sets up the widgets accordingly. The variating widgets are put into lists for  #
# easy addition - that is, lists are used to hold the widgets that are associated with the vehicle data, since it is easy to add as many as needed no matter      #
# what the passed number is.                                                                                                                                      #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

class AdvancedWindow(object):
    """ A more advanced gui window, which allows the user to select multiple simulated vehicles and can input the amplitude. """

    def init(self, num_vehicles = 3, is_metric = False):
        """ This function is used to set up the window (initiate the object and instantiate all its attributes). This is used instead of a __init__ method since
it is needed to be called multiple times - every time the window is added again to the main window's frame.

The 'num_vehicles' optional parameter is used to detail how many vehicles (and thusly how many widgets) are in the simulation. For this application, the number will
always at most be three.

The 'is_metric' optional parameter is used to change between English and Metric units. For the window, this just means switching between miles per hour and
kilometers per hour for the speed unit Label. If 'is_metric' is True, 'kph' is put as the text instead of 'mph'. The actual data conversion is done when creating
the sine wave. """

        self.dur_lbl = Label("Duration")    #A label for the duration entry
        self.dur_entry = Entry()            #The entry (text field) where the user inputs the duration for the simulated vehicle
        self.d_unit_lbl = Label("sec")      #A label that details the units of measurement for the duration


        #Set up the table for hold the widgets dealing with the duration. 
        self.dur_table = Table(1, 3)

        self.dur_table.add_child(0, 0, self.dur_lbl)
        self.dur_table.add_child(0, 1, self.dur_entry)
        self.dur_table.add_child(0, 2, self.d_unit_lbl)

        #Set up the labels for the different information that needs to be added for each vehicle in the simulation
        self.speed_lbl = Label("Speed (mph)")
        self.appr_lbl = Label("Receding") #Default is approaching, so the check buttons should be checked when the vehicle is receding
        self.amp_lbl = Label("Amplitude")

        #Now, if 'is_metric' is True, then the units should be metric, so change the text of the speed label to mention kilometers per hour
        if is_metric:
            self.speed_lbl.text = "Speed (kph)"

        #Set up the lists that will hold the different widgets for all the specified vehicles.
        self.speed_entries = [] #Used to hold the Entry widgets to enter each vehicle's speed
        self.appr_buttons = []  #Used to hold the Checkbutton widgets to determine if the vehicles are approaching or receding
        self.amp_entries = []   #Used to hold the Entry widgets for entering the amplitude of each vehicle's sine wave
        
        for i in range(num_vehicles):
            self.speed_entries.append(Entry())      #Add a new Entry (text field) object for each vehicle in the simulation.
            self.appr_buttons.append(CheckButton()) #Add a new Checkbutton object for each vehicle in the simulation
            self.amp_entries.append(Entry())        #Add a new Entry (text field) object for each vehicle in the simulation.


        #Set up the table for holding all these widgets
        self.list_table = Table(num_vehicles + 1, 3) #The table should be big enough for each group of widgets

        self.list_table.add_child(0, 0, self.speed_lbl) #Add the speed label first
        self.list_table.add_child(0, 1, self.appr_lbl)  #Add the approaching label second
        self.list_table.add_child(0, 2, self.amp_lbl)   #Add the amplitude label last

        for i in range(num_vehicles): #For as many vehicles there are, add each group of associated widgets (speed, appr/reced, ampl) to the table
            self.list_table.add_child(i + 1, 0, self.speed_entries[i])
            self.list_table.add_child(i + 1, 1, self.appr_buttons[i])
            self.list_table.add_child(i + 1, 2, self.amp_entries[i])

        #Set up an HFrame for the list table
        self.list_frame = HFrame()
        self.list_frame.add_child(self.list_table) #Add the list table to the frame

            
        self.main_table = Table(2, 1) #This is the main table for the window, which holds all the other tables.
        
        self.main_table.add_child(0, 0, self.dur_table)  #Add the duration table first
        self.main_table.add_child(1, 0, self.list_frame) #Then the list frame


    #---------------------------------------------------------------------------------------------------------#
    # This method is used to switch the text for the speed entries from miles per hour to kilometers per hour #
    #---------------------------------------------------------------------------------------------------------#

    def switch_units(self, is_metric):
        """ This method switches the text for the speed button - between English and Metric. The passed parameter 'is_metric' determines which it should
be switched to. """
        if is_metric: #If the units should change to metric, put them in kilometers per hour
            self.speed_lbl.text = 'Speed (kph)'
        else:
            self.speed_lbl.text = 'Speed (mph)'


    def get_speed(self):
        """ This method returns a list containing the text within the Entry widgets in 'speed_entries' """
        text = []

        #Go through each entry in the list and add the text to the text list
        for entry in self.speed_entries:
            text.append(entry.text)

        return text #Return the list containing all the text


    def get_direction(self):
        """ This method returns a list containing booleans that determine which direction each vehicle is heading, if any. """
        direct = []

        #Go through each check button in the list, and for each that is checked (active), append true to the direction list. For those that are not, append False
        for cb in self.appr_buttons:
            if cb.active:
                direct.append(False) #If the button was checked, then the vehicle should be receding
            else:
                direct.append(True)

        return direct #Return the list containing the direction booleans


    def get_duration(self):
        """ This method returns the duration of the simulation - how long the sine waves should be played for. """
        return self.dur_entry.text


    def get_amplitude(self):
        """ This method returns a list containing the amplitudes of each vehicle's sine wave. """
        amp = []

        #Go through each entry in the list and add the text to the amplitude list
        for entry in self.amp_entries:
            amp.append(entry.text)

        return amp #Return the list containing the amplitudes




    #-----------------------------------------------------------------------------------------------------------------------------------------------------#
    # This is the method that returns the reference to the 'main_table' attribute. It is used to add the widgets of the advanced window to the interface. #
    #-----------------------------------------------------------------------------------------------------------------------------------------------------#

    def get_main_table(self):
        """ This method returns a reference to the 'main_table' Table attribute. """
        return self.main_table


#------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# This class is used to set up and create the graphical user interface. It takes the simple and advanced windows as objects and uses their main tables for getting #
# input from the user. The tables can be switched out - and the number of vehicles for the advanced table specified - using widgets (such as radio buttons).       #
#                                                                                                                                                                  #
# This class also takes care of starting the simulation.                                                                                                           #
#------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class MainWindow(object):
    """ This class represents the main window / gui of the module. It contains the simple and advanced windows as objects and using them to create sine waves for
vehicle simulations. It also allows the user to specify the transmit frequency (in K-, Ka-, or X-band) for the calculations needed to create the sine waves as well as
switching between the simple and advanced windows."""

    FREQUENCY_SAMPLE = 44.1e3       #This is the (default) frequency sample for creating sine waves
    MAPPING = numpy.array([1, 2])   #This is the (default) mapping used to specify the channels used for each sine wave when creating them using sounddevice

    def __init__(self, simple_obj = SimpleWindow(), advanced_obj = AdvancedWindow()):

        self.gui = None             #The 'renderer' for the interface. It is basically the gui - holds the window screen, all the widgets, and manages all the events.
        self.main_frame = HFrame()  #The main frame of the gui. This will hold the other components of the gui - including the simple and advanced windows

        self.switch_frame = HFrame() #This frame holds the 'switching' buttons - the Button to switch between windows and the CheckButton to switch between speed units

        self.band_frame = HFrame(Label("Transmit Frequency")) #This frame holds the radio buttons for choosing the band

        self.simple_win = simple_obj        #This holds the simple window object used to create / display the simple window
        self.advanced_win = advanced_obj    #This holds the advanced window object used to create / display the advanced window

        
        #Set up the button used to switch back and force between the simple and advanced window tables.
        self.switch_button = Button("#Switch to Advanced Sim")
        self.switch_button.connect_signal(SIG_CLICKED, self.switch_windows)

        #Set up a CheckButton object to switch to metric units
        self.metric_button = CheckButton("Metric")
        self.metric_button.connect_signal(SIG_CLICKED, self.switch_units) #If the button is clicked, changed the units based on its activity (checked or unchecked)

        #Add the two buttons to the switch frame
        self.switch_frame.add_child(self.switch_button)
        self.switch_frame.add_child(self.metric_button)
        

        #Here are the radio buttons for choosing the band for the transmit frequency
        self.kband_rad = RadioButton("K-Band")
        self.kaband_rad = RadioButton("Ka-Band", self.kband_rad)
        self.xband_rad = RadioButton("X-Band", self.kband_rad)

        self.kband_rad.active = True #Set the K-Band frequency to active by default, since it is the most used/common frequency

        #Add the radio buttons to the band frame
        self.band_frame.add_child(self.kband_rad)
        self.band_frame.add_child(self.kaband_rad)
        self.band_frame.add_child(self.xband_rad)

        #Create and set up the run button for starting the simulation
        self.run_button = Button("#Run")
        self.run_button.connect_signal(SIG_CLICKED, self.run)


    #----------------------------------------------------------------------------------------------------------------------------------------------------#
    # This method is used to switch between using the simple sine wave creation (with only one vehicle and default amplitude) and the advanced sine wave #
    # creation (up to three vehicles specified and allowing the user to input the amplitude).                                                            #
    #----------------------------------------------------------------------------------------------------------------------------------------------------#
    
    def switch_windows(self):
        """ This method switches between the simple and advanced windows. """
        #First, determine which window is currently active.
        if self.simple_win.get_main_table() == self.main_frame.children[0]: #If the current window is the simple window, it should be switched to the advanced window
            next_win = 'A' #Use A to denote that the advanced window should be switched to.

        else: #Otherwise, the advanced window is currently displayed, so switch to the simple one
            next_win = 'S' #Use S to denote that the simple window should be switched to
            
        #Next, remove any 'child' (table that holds the window widgets) from the main frame, and then add the appropriate window table to the mainframe.
        for child in self.main_frame.children:
            self.main_frame.remove_child(child) #Remove the child from the main frame
            child.destroy()

        #Finally, add the appropriate window to the GUI
        if next_win == 'S':      #If the radio button for the simple window is active, then add its main table to the frame
            self.simple_win.init(self.metric_button.active) #Re-initiate the object and make sure the units for speed correspond to the current choice of the user
            self.main_frame.add_child(self.simple_win.get_main_table()) #Add the main table of the window to the GUI

            self.switch_button.set_text("#Switch to Advanced Sim") #Switch the button's text to indicate which window will be switched to next

    
        else: #Otherwise, add the advanced window's main table to the frame

            self.advanced_win.init(is_metric = self.metric_button.active) #Re-initate the object and make sure the units for the speed correspont to the current choice of the user
            self.main_frame.add_child(self.advanced_win.get_main_table()) #Add the main table of the window to the GUI

            self.switch_button.set_text("#Switch to Simple Sim") #Switch the button's text to indicate which window will be switched to next


    #----------------------------------------------------------------------------------#
    # This method switches between English and Metric measurements for the simulation. #
    #----------------------------------------------------------------------------------#
    
    def switch_units(self):
        """ This method changes between English and Metric units for the speed data. It simply calls the each window's 'switch_units()' method to change the unit
label to the current units the user wants to use. """
        if self.simple_win.get_main_table() == self.main_frame.children[0]: #Check if the simple window is the current one
            if self.metric_button.active: #If the metric button is active, then the units should be English
                #print "Switch to English..." #DEBUG
                self.simple_win.switch_units(False) #Pass False to indicate it should be English
            
            else:
                #print "Switch to metric..." #DEBUG
                self.simple_win.switch_units(True) #Pass True to indicate it should be metric
                
        else: #Otherwise, it's the advanced window
            if self.metric_button.active: #If the metric button is active, then the units should be English
                #print "Switch to English..." #DEBUG
                self.advanced_win.switch_units(False) #Pass False to indicate it should be English
            
            else:
                #print "Switch to metric..." #DEBUG
                self.advanced_win.switch_units(True) #Pass True to indicate it should be metric



    #----------------------------------------------------------------------------------------------------------------------------------------------------------#
    # This method calculates the frequency of a sine wave based upon the passed velocity (in meters per second) and the transmit frequency chosen by the user. #
    #----------------------------------------------------------------------------------------------------------------------------------------------------------#

    def calc_frequency(self, velocity):
        """ This method calculates the frequency of the sine wave based on the transmit frequency and velocity (in meters per second) selected by the user.
The frequency is calculated using the Doppler Equation:

    frequency = (2 * transmit_frequency * velocity) / c
    """
        c = 299792458 #The speed of light in meters per second

        #Dermine the transmit frequency using the band radio buttons
        if self.kband_rad.active:
            trans_freq = 24.150e9 #For K-band (in Hz)
            
        elif self.kaband_rad.active:
            trans_freq = 34.7e9   #For Ka-Band (in Hz)
            
        elif self.xband_rad.active:
            trans_freq = 10.525e9 #For X-Band (in Hz)

        else: #Otherwise, return None to indicate an error occurred (since no transmit frequency was chosen)
            return None
            
        #Calculate and return the frequency using the Doppler Equation
        return (2 * trans_freq * velocity) / c


    #----------------------------------#
    # This method runs the simulation. #
    #----------------------------------#

    def run(self):
        """ This method runs the simulation: it creates sine waves based upon which window is active and what data was entered in by the user and then plays
the sound waves. If any error occurs, the simulation stops and a dialog window with an error message is created. """

        #First, determine which window is currently active.
        if self.simple_win.get_main_table() == self.main_frame.children[0]:

            #Get the speed, duration, and direction from the simple window's widgets
            speed = self.simple_win.get_speed()
            duration = self.simple_win.get_duration()
            direction = self.simple_win.get_direct()

            #Call the 'create_sine' function to create and return the data needed to play the sine wave
            channels = self.create_sine(speed, direction, duration)

            #Check if an error message was returned - if so, 'channels' will not be a numpy array but a string
            if type(channels) == str:
                
                #If an error message was returned, create a dialog window to display the error message using the 'create_error_window' method
                create_error_window(self.gui, channels)
                
            else: #Otherwise, no error message was returned, the creation of the sine wave data was success; thusly, play the sine wave using the returned data
                #Play the sine wave data within the numpy array 'channels'

                #print "sb_mapping: ", MainWindow.MAPPING #DEBUG
                #print "sb_f_sample: ", MainWindow.FREQUENCY_SAMPLE #DEBUG

                #Now, since the main channel has been found, find the maximum value in the numpy array and scale the whole array down by that value (to keep within range)
                maximum = numpy.amax(numpy.abs(channels))
                channels = channels/maximum

                #Finally, play the sine wave
                sounddevice.play(channels, MainWindow.FREQUENCY_SAMPLE, MainWindow.MAPPING.copy()) #Copy the mapping to make sure that sounddevice doesn't change it

                #print "sa_mapping: ", MainWindow.MAPPING #DEBUG
                #print "sa_f_sample: ", MainWindow.FREQUENCY_SAMPLE #DEBUG


        else: #Otherwise, it was the advanced window, and so get the data from the advanced window's widgets

            #Get the speed, direction, and amplitude lists from the advanced window's widgets
            speed_list = self.advanced_win.get_speed()
            direct_list = self.advanced_win.get_direction()
            amp_list = self.advanced_win.get_amplitude()

            #Get the duration for the simulation
            duration = self.advanced_win.get_duration()

            #Couple all the vehicle data into one list, with each individual vehicle data in a list of its own (within the overarching list). Exclude any
            #vehicle data that has not been specified (each data value is None or empty string
            vehicle_data = []

            for i in range(len(speed_list)):
                #If all the data for the vehicle is specified, add the data to the main data list
                if (speed_list[i] != None and speed_list[i] != "") and (direct_list[i] != None) and (amp_list[i] != None and amp_list[i] != ""):
                    vehicle_data.append([speed_list[i], direct_list[i], amp_list[i]])

            #Now, for the vehicle data that is specified, create sine wave data for the vehicle using the 'create_sine()' method and store all this data
            #within a list. If any error pops up for any vehicle, display the error and stop the simulation
            sine_wave_data = []
            error = False  #Used to indicate if an error occured while creating the sine waves

            for vehicle in vehicle_data:
                channels = self.create_sine(vehicle[0], vehicle[1], duration, vehicle[2]) #Pass the vehicle data into the 'create_sine()' method

                #Check if an error message was returned - if so, 'channels' will not be a numpy array but a string
                if type(channels) == str:
                    
                    #If an error message was returned, create a dialog window to display the error message using the 'create_error_window' method
                    create_error_window(self.gui, channels)
                    
                    error = True  #Change to True to designate an error has occured.
                    break #Exit the loop

                else: #Otherwise, add the data into the 'sine_wave'data' list
                    sine_wave_data.append(channels)


            #Now, if an error did not occur, all the sine wave data was created and saved into 'sine_wave_data', so the sine waves can be created and played
            if not error:

                #First, check if there is any data within the 'sine_wave_data' - since the user could have not specified any data and hit 'run'
                if sine_wave_data == []:

                    #If there was no data, then create a dialog window displaying that no vehicle data was specifed
                    create_error_window(self.gui, "DATA ERROR")
                    
                else: #Otherwise, there is data, and so add all of the numpy arrays together into one numpy array and play that as the combined sine waves
                    main_channel = sine_wave_data[0] #Get the first vehicle in the sine wave data for the main channel

                    for i in range(1, len(sine_wave_data)): #Go through each sine wave data and add it to the main channel
                        main_channel += sine_wave_data[i]

                    #print "ab_mapping: ", MainWindow.MAPPING #DEBUG
                    #print "ab_f_sample: ", MainWindow.FREQUENCY_SAMPLE #DEBUG

                    #Now, since the main channel has been found, find the maximum value in the numpy array and scale the whole array down by that value (to keep within range)
                    maximum = numpy.amax(numpy.abs(main_channel))
                    main_channel = main_channel/maximum

                    #Finally, play the sine waves
                    sounddevice.play(main_channel, MainWindow.FREQUENCY_SAMPLE, MainWindow.MAPPING.copy()) #Copy the mapping to make sure that sounddevice doesn't change it

                    #print "aa_mapping: ", MainWindow.MAPPING #DEBUG
                    #print "aa_f_sample: ", MainWindow.FREQUENCY_SAMPLE #DEBUG


                
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # Here is the basic method to create a sine wave to simulate a vehicle passing using given information about the speed, direction, length of time, and amplitude. #
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    def create_sine(self, speed_units, direction, duration, amplitude = 1):
        """ This method creates a sine wave using basic data passed into it - the speed of the vehicle, the direction of the vehicle (either True for approaching the
radar gun or False for receding), how long the sine wave should last for, and the amplitude of the sine waves (which correlates to the distance the vehicle is from
the radar gun.

NOTE: The sine wave, after creation, is scaled by the amplitude, but no checks are made to see if the waves are out of bounds and need to be scaled down. This is
taken care of in the 'run()' method (where the sine waves are always scaled down by the maximum value in the numpy array to keep the uppermost value as 1). """
        
        #First determine the phase angle using the direction
        if direction:                       #If the direction is towards the radar
            phase_angle = numpy.pi/2
        elif direction == False:            #If the direction is away from the radar
            phase_angle = -1 * numpy.pi/2
        else:                               #Otherwise, the user did not choose a direction, so return 'ERROR' since the sine wave cannot be created
            return 'DIR ERROR'

        #Convert the passed string data into floating point numbers, if possible
        try:
            speed_units = float(speed_units)
            duration = float(duration)
            amplitude = float(amplitude)
            
        except ValueError:
            return 'CONVERT ERROR' #Return an error message that the speed and/or the duration could not be converted (

        frequency_sample = MainWindow.FREQUENCY_SAMPLE #Set the frequency sample to the standard sample stored in FREQUENCY_SAMPLE of the 

        #Turn the speed value in the specified units (either mph or kph) into meters per second and then calculate the frequency using the Doppler Equation

        if self.metric_button.active: #If the metric button is active (checked), then the units are in kilometers per hour
            #print "--in run, using metric units..." #DEBUG
            meters_per_sec = speed_units * (1000.0 / 60**2) #Convert to meters per second (make 1000 a floating point number to avoid integer division)

        else: #Otherwise, the units are in miles per hour
            #print "--in run, using English units..." #DEBUG
            meters_per_sec = speed_units * (1609.34 / 60**2) #Convert to meters per second
        
        frequency = self.calc_frequency(meters_per_sec) #Calculate and get the frequency (in Hz)

        #print frequency #DEBUG

        #If the frequency is None, then an error occurred (transmit frequency not specified) and exit the function with an error string
        if frequency == None:
            return 'TRANSMIT FREQ ERROR' #No transmit frequency was specified

        #Create a numpy array that contains the numbers from 1 to the frequency sample multiplied by the duration. This is used to both create the sine wave and to
        #determine its length of time to play
        n_list = numpy.arange(1, int(round(duration * frequency_sample) + 1))

        #Now, calculate the arrays/lists of cosine function values for creating the sound wave
        ch_1_data = numpy.cos(2 * numpy.pi * frequency * n_list / frequency_sample)                         #The data for the first (left) channel of the sound
        ch_2_data = 1.9 * numpy.cos((2 * numpy.pi * frequency * n_list / frequency_sample) - phase_angle)   #The data for the second (right) channel of the sound
        
        #Combine the two numpy arrays into one - needed for sending into sounddevice : will play multiple channels, but have to be in one multi-dimensional array
        channels = numpy.array([ch_1_data, ch_2_data])

        #Getting the transpose because sounddevice interprets COLUMNS as channels, NOT ROWS - using numpy.array([ch_1_data, ch_2_data]) returns
        #the channel 1 and 2 arrays as ROWS of the new array. Thusly, to fit the specifications of sounddevice, the transpose must be used.
        channels = channels.T

        #Finally, multiply both channels by the passed amplitude.
        channels = channels * amplitude

        #Return the channels for the sine wave from the method
        return channels
            
            

    #-----------------------------------------------------------------------#
    # Here is the 'start()' method, which instantiates the gui and runs it. #
    #-----------------------------------------------------------------------#
    
    def start(self, title, win_width, win_height):
        """ This is the main method for this class, which sets up everything for the user interface and starts the main loop. """

        #Initialize the GUI
        self.gui = Renderer()
        self.gui.create_screen(win_width, win_height) #Create the screen for the gui
        self.gui.title = title     #Set up the title of the window
        self.gui.color = GUI_COLOR #Set up the color (background) of the GUI

        #Create a main table to hold and format all the frames of the object
        main_table = Table(4, 1)


        #Add each frame to the table
        main_table.add_child(0, 0, self.switch_frame)
        main_table.add_child(1, 0, self.main_frame)
        main_table.add_child(2, 0, self.band_frame)
        main_table.add_child(3, 0, self.run_button)

        #Add the table to the gui
        self.gui.add_widget(main_table)

        #Initiate and add the main table of the SimpleWindow, since it will be the default window to open to
        self.simple_win.init() #Initiate the object
        self.main_frame.add_child(self.simple_win.get_main_table()) #Add it to the main frame of the GUI
        
        #Start the main loop.
        self.gui.start()



#----------End of Class Definitions----------#






#----------Start of Function Definitions----------#


#--------------------------------------------------------------------------------------------------------------------#
# This function is used to create a dialog window to display messages about errors that occur during the simulation. #
#--------------------------------------------------------------------------------------------------------------------#

def create_error_window(gui, error_string):
    """ This method creates a dialog window to display an error message to the user when an error occurs when running the simulation. """

    #Create the buttons and the results for the buttons for the dialog window
    buttons = [Button("#Close")]
    signals = [DLGRESULT_OK]

    #Create the dialog window
    dialog_win = GenericDialog("Error Message", buttons, signals)

    error = error_string + ": " #The type of error that was created

    #Set up the widgets needed for the message
    e_label = Label(error)      #Create a Label widget to display the kind of error that occured
    frame = VFrame()            #Create a VFrame to hold the Label widget

    frame.add_child(e_label) #Add the error string label to the frame
    
    #Determine what error string was passed into the function and get the appropriate error message to display
    if error_string == "DIR ERROR": #An error happened with the direction of the vehicle - no direction specified

        #Create a Label object to display the error message
        msg_label = Label("Direction for vehicle not specified")

        #Add the error message to the frame
        frame.add_child(msg_label)

    elif error_string == "CONVERT ERROR": #An error happened with the conversion of the speed, duration, and/or amplitude - no data or invalid data specified

        #Create Label objects to display the error message
        msg_label = Label("Invalid data for speed, duration,")
        msg_label2 = Label("and/or amplitude")

        #Add the error message to the frame
        frame.add_child(msg_label)
        frame.add_child(msg_label2)

    elif error_string == "TRANSMIT FREQ ERROR": #An error happened with the transmit frequency for the vehicle - none was specified

        #Create a Label object to display the error message
        msg_label = Label("No transmit frequency was specified")

        #Add the error message to the frame
        frame.add_child(msg_label)

    elif error_string == "DATA ERROR": #No data was specified at all (for advanced window)

        #Create Label objects to display the error message
        msg_label = Label("Invalid and/or no data was specifed")
        msg_label2 = Label("for the vehicles")

        #Add the error message to the frame
        frame.add_child(msg_label)
        frame.add_child(msg_label2)

    else: #This shouldn't be come to, since any error will be one of the above, but for the impossible case, just say an error occured

        #Create a Label object to display the error message
        msg_label = Label("An error occured")

        #Add the error message to the frame
        frame.add_child(msg_label)
        

    dialog_win.content.add_child(frame) # Add the frame to the dialog window's content
    
    dialog_win.connect_signal(SIG_DIALOGRESPONSE, close_dialog, dialog_win)
    dialog_win.depth = 2 #Put the dialog window on top of the other widgets

    gui.add_widget(dialog_win) #Add the dialog window to the GUI


#-----------------------------------------------------------------------------------------------------------------#
# This function simply destroys the passed GenericDialog window (or technically any dialog window passed into it) #
#-----------------------------------------------------------------------------------------------------------------#

def close_dialog(result, dialog):
    """ This method destroys the passed dialog window when called. """
    if result == DLGRESULT_OK: #If the OK result was signaled (which should be the only signal), destroy the dialog window
        dialog.destroy() #Destroy the dialog window


#----------End of Function Definitions----------#




#If run by itself without being imported, simply create the GUI window and start it
if __name__ == "__main__":
    main = MainWindow()
    main.start("NIST DTR Radar Target Simulator", 290, 325)
        
