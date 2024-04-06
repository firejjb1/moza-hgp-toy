"""
Script to read Moza HGP shifter input and do stuff
Using pywinusb
"""
from time import sleep
from msvcrt import kbhit

import pywinusb.hid as hid

#from pywinauto.application import Application
import subprocess


unicode = str
raw_input = input

vscodePath = "C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
vsstudioPath = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\IDE\\devenv.exe"
notionPath = "C:\\Users\\user\\AppData\\Local\\Programs\\Notion\\Notion.exe"
edgePath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
discordPath = "C:\\Users\\user\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe"
steamPath = "C:\\Program Files (x86)\\Steam\\steam.exe"
ankiPath = "C:\\Users\\user\\AppData\\Local\\Programs\\Anki\\anki.exe"

gear1Path = vscodePath
gear2Path = vsstudioPath
gear3Path = notionPath
gear4Path = edgePath
gear5Path = ankiPath
gear6Path = steamPath

programPerGear = [gear1Path, gear2Path, gear3Path, gear4Path, gear5Path, gear6Path ]
class MozaMod:
    gearStates = [False] * 7

    def sample_handler(self, data):
        gear = -1
        if data[len(data)-1 - 2] == 32:
            gear = 0
        if data[len(data)-1 - 2] == 64:
            gear = 1
        if data[len(data)-1 - 2] == 128:
            gear = 2
        if data[len(data)-1 - 1] == 1:
            gear = 3
        if data[len(data)-1 - 1] == 2:
            gear = 4
        if data[len(data)-1 - 1] == 4:
            gear = 5
           
        if not self.gearStates[gear]:
            self.gearStates = [False] * 7
            if gear > -1:
                subprocess.Popen([programPerGear[gear]])
                self.gearStates[gear] = True



    def test(self):
        all_hids = hid.HidDeviceFilter(vendor_id = 0x346e).get_devices()

        print(all_hids)
        if not all_hids:
            print("No HID class devices attached.")
        else:
            while True:
                print("Choose a device to monitor raw input reports:\n")
                print("0 => Exit")
                for index, device in enumerate(all_hids):
                    device_name = unicode("{0.vendor_name} {0.product_name}" \
                            "(vID=0x{1:04x}, pID=0x{2:04x})"\
                            "".format(device, device.vendor_id, device.product_id))
                    print("{0} => {1}".format(index+1, device_name))
                print("\n\tDevice ('0' to '%d', '0' to exit?) " \
                        "[press enter after number]:" % len(all_hids))
                index_option = raw_input()
                if index_option.isdigit() and int(index_option) <= len(all_hids):
                    # invalid
                    break
            int_option = int(index_option)
            if int_option:
                device = all_hids[int_option-1]
                try:
                    device.open()

                    #set custom raw data handler
                    device.set_raw_data_handler(self.sample_handler)

                    print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
                    while not kbhit() and device.is_plugged():
                        #just keep the device opened to receive events
                        sleep(0.5)
                    return
                finally:
                    device.close()
 
    #
if __name__ == '__main__':
    mozamod = MozaMod()
    mozamod.test()
