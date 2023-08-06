***************
CTid-programmer
***************

A graphical-user interface for programming CTid®
information into a CTid-enabled sensor.  The program relies on avrdude
to do the physical programming of ATtiny microcontrollers.

This program depends on PyQt4 which cannot be installed by pip.
On Ubuntu, make sure you have the python3-qt4 package installed:

    sudo apt install python3-pyqt4

The program also depends on an enhanced version of avrdude, which is
available here:

    https://bitbucket.org/egauge/avrdude/src/upstream/

The enhancements in this repository enable programming of ATtiny
microcontrollers with a standard FTDI serial cable.
