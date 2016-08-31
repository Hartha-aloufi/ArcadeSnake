import RPi.GPIO as GPIO



in1 = 35;
in2 = 36;
in3 = 37;
in4 = 38;


class rasp:

    def __init__(self):
        """
        sets up gpio input

        @param self: 
        @type self: 
        @return: 
        @rtype: 
        """


        GPIO.setmode(GPIO.BOARD);

        

        GPIO.setup(in1, GPIO.IN, pull_up_down=GPIO.PUD_UP);

        GPIO.setup(in2, GPIO.IN, pull_up_down=GPIO.PUD_UP);

        GPIO.setup(in3, GPIO.IN, pull_up_down=GPIO.PUD_UP);

        GPIO.setup(in4, GPIO.IN, pull_up_down=GPIO.PUD_UP);


        self.JUP = in3;
        self.JDOWN = in4;
        self.JRIGHT = in1;
        self.JLEFT = in2;


    def input(raspinput):
        """
        checks whether the pi is getting signals from the input specified,
        the input can be:

        Rasp.JUP,
        Rasp.JDOWN,
        Rasp.JRIGHT,
        Rasp.JLEFT

        @param raspinput: 
        @type raspinput: 
        @return: true if the pi is getting input from raspinput
        @rtype: bool
        """


        return not GPIO.input(raspinput)

    def cleanup():
        """
        has to be called at the end of the program in order to release gpio resources.
        
        @return: 
        @rtype: 
        """
        GPIO.cleanup();
    

Rasp = rasp();
