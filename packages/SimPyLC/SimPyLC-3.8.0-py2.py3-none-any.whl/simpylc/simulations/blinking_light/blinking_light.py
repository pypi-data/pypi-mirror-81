# ====== Legal notices
#
# Copyright (C) 2013 - 2020 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.qquick.org/license.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

import simpylc as sp

class BlinkingLight (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)
        self.blinkingTimer = sp.Timer ()
        self.blinkingLight = sp.Marker ()
        self.pulse = sp.Oneshot ()
        self.counter = sp.Register ()
        self.run = sp.Runner ()
        
    def input (self):   
        pass
    
    def sweep (self):
        self.blinkingTimer.reset (self.blinkingTimer > 8)
        self.blinkingLight.mark (not self.blinkingLight, not self.blinkingTimer)
        self.pulse.trigger (self.blinkingTimer > 3)
        self.counter.set (self.counter + 1, self.pulse)
        
