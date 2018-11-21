#  -*- coding: utf-8 -*-

"""Class implementing communication with NDI (Northern Digital) trackers"""

#there is some cut and paste from Doshkun's wherepy and from NifTKNDICapiTracker.*

#we can import generic tracker code from scikit-tracker, which isn't written yet.

from ndicapy import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                     ndiOpenNetwork, ndiCloseNetwork,
                     ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                     ndiGetGXTransform, NDI_XFORMS_AND_STATUS,
                     NDI_115200, NDI_8N1, NDI_NOHANDSHAKE)

#where should we set things like this?
VIRTUAL_SROM_SIZE=1024 
#THIS isn't necessary if we use ndicapy read from file function as that 
#will pad it out to 1024 anyway
#so current niftk library
#reads sroms at contructor, then calls internal connect
#which calls enabletoolports

if sys.version_info[0] >= 3:
    def c_str(value):
        """Convert passed value to a Python3-compatible
        C-style string for use in NDI API functions.
        """
        return bytes(str(value), 'utf-8')
else:
    def c_str(value):
        """Convert passed value to a Python2-compatible
        C-style string for use in NDI API functions.
        """
        return str(value)

class ndiTracker:
    """For NDI trackers, hopefully will support Polaris, Aurora, 
    and Vega, currently only tested with wireless tools on Vega
    """
     def __init__(self):
        """Create an instance ready for connecting."""
        super(Tracker, self).__init__()
        self.device = None

    def Connect ( ip , port ):
        self.device = ndiOpenNetwork(ip, port)
        if not self.device:
            raise IOError(
            'Could not connect to NDI device found on '
            '{}'.format(name))

        reply = ndiCommand(device, 'INIT:')
        error = ndiGetError(device)
        if  error != NDI_OKAY:
            raise IOError(
            'Error when sending command: '
            '{}'.format(ndiErrorString(error)))   


    def ReadSROMsFromFile ( sromFilenames ):
        #basically want to implement NDICapitracker::EnableToolPorts
        # // stop tracking
        #if (this->IsDeviceTracking) //this is an integer flag maintaned my m_Tracker. We can do that I guess.
        #let's not bother with it for now, see what sort of errors we get if we call TSTOP when not in tracking mode?
        #check whether there's a call to ndi.
        #other wise just do this
        ndiCommand(self.device,'TSTOP:')
        errnum = ndiGetError(self.device)
        if errnum != NDI_OKAY:
            ndiClose(self.device)
            raise IOError('Error when sending TSTOP to tracker. The error'
                              ' was: {}'.format(ndiErrorString(errnum)))
    
        #free ports that are waiting to be freed
        ndiCommand(self.device,'PHSR:01')
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        for toolIndex in range (numberOfTools):
            portHandle = ndiGetPHSRHandle(self.device,toolIndex)
            ndiCommand(self.device,"PHF:%02X",portHandle)

            errnum = ndiGetError(self.device)
            if errnum != NDI_OKAY:
            ndiClose(self.device)
            raise IOError('Error when freeing port handle {}. The error'
                              ' was: {}'.format(toolIndex,ndiErrorString(errnum)))

        # Set port handles and send SROM files to tracker
        # We need to do this before initializing and enabling
        # the ports waiting to be initialized.
        # at this stage we're going to need a list of srom file names. 

        for sromfilename in sromFilenames:
            #no wired tools
            #get a port handle, there's a lot of wildcards in the 
            #next PHRQ command?
            ndiCommand(this->Device, 'PHRQ:*********1****')
            #not sure this is the python module
            portHandle = ndiGetPHRQHandle(this->Device);
            errnum = ndigeterror(self.device)
            if errnum != ndi_okay:
                ndiclose(self.device)
                raise ioerror('error when freeing port handle {}. the error'
                              ' was: {}'.format(toolindex,ndierrorstring(errnum)))

            #this returns some sortof ndibit field? What do we do with it
            ndiPVWRFromFile(self.device, portHandle, sromfilename)
            errnum = ndigeterror(self.device)
            if errnum != ndi_okay:
                ndiclose(self.device)
                raise ioerror('error when setting rom file port handle {}. the error'
                              ' was: {}'.format(toolindex,ndierrorstring(errnum)))






#two ways of implementing this, one we read into a binary object
#then pass using ndiPVWR, alternatively we use ndicapymodules ...
PyObject* Py_ndiPVWRFromFile(PyObject* module, PyObject* args)  
#this wants port and file name, what is the port for vega?
