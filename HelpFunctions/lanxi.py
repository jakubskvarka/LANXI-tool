import requests
from.import utility as utility
#
# class LanXI:
#     def __init__(self, ip,sampling_freq,channel_info):
#         self.channel_info=channel_info
#         self.sampling_freq=sampling_freq
#         self.ip = ip
#         self.host = "http://" + self.ip
#
#     def setup_stream(self):
#         """
#         Setup of channel 1 with a microphone
#         """
#         # This setup is indentical to the one found in "Streaming.py", refer to this for more info.
#         # Open recorder application
#         requests.put(self.host + "/rest/rec/open")
#         # Get information about the device and configure
#         self.GetTeds()
#         self.ConfigureStream()
#
#         print(self.channels)
#
#         self.GetFs()
#
#
#
#     def GetTeds(self):
#         # Start TEDS detection, we then check when it is done and read it out as JSON
#         # Detect TEDS
#         self.response = requests.post(self.host + "/rest/rec/channels/input/all/transducers/detect")
#         while requests.get(self.host + "/rest/rec/onchange").json()["transducerDetectionActive"]:
#             pass
#         # Get TEDS information
#         self.response = requests.get(self.host + "/rest/rec/channels/input/all/transducers")
#         self.channels = self.response.json()
#
#
#
#
#
#     def ConfigureStream(self):
#         # To start a stream we first need to set a configuration. In this example we create a configuration by requesting a default channel setup.
#         # We use a tiny utility function to update all values with a given key.
#         # Create a new recording
#         self.response = requests.put(self.host + "/rest/rec/create")
#         # Get Default setup for channels
#         self.response = requests.get(self.host + "/rest/rec/channels/input/default")
#         self.setup = self.response.json()
#         # Replace stream destination from default SD card to socket
#         utility.update_value("destinations", ["socket"], self.setup)
#         # Set enabled to false for all channels
#         utility.update_value("enabled", False, self.setup)
#         #########
#         utility.update_value("bandwidth", self.sampling_freq,self.setup)
#         for i,ch in enumerate(self.setup['channels']):
#             if float(self.channel_info[i]['sensitivity'])>0:
#                 ch['transducer'] = {
#                     "requires200V": 0,
#                     "requiresCcld": 1,
#                     "sensitivity": self.channel_info[i]['sensitivity'],
#                     "unit":self.channel_info[i]['unit']
#                     }
#                 self.setup['channels'][i]['ccld'] = 1
#                 self.setup['channels'][i]['polvolt'] = 0
#                 self.setup['channels'][i]['name']=self.channel_info[i]['name']
#                 self.setup['channels'][i]['enabled'] = True
#             else:
#                 self.setup['channels'][i]['enabled'] = "False"
#                 #################
#         # Enable channels with valid TEDS
#         for channel_nr in range(len(self.channels)):
#             if self.channels[channel_nr] != None:
#                 self.setup["channels"][channel_nr]["transducer"] = self.channels[channel_nr]
#                 self.setup["channels"][channel_nr]["enabled"] = True
#                 self.setup["channels"][channel_nr]["ccld"] = self.channels[channel_nr]["requiresCcld"]
#
#
#         # Remove None channels
#         # self.channels = list(filter(lambda x : x != None, self.channels))
#         # if not any(self.channels):
#         #     print("No channels enabled! Did you connect a microphone?")
#         #     exit()
#         # Next we setup the input channels for streaming. We use the input setup we got previosly.
#         # Create input channels with the setup
#         print(self.setup)
#         self.response = requests.put(self.host + "/rest/rec/channels/input", json = self.setup)
#         # Get streaming socket
#         self.response = requests.get(self.host + "/rest/rec/destination/socket")
#         self.inputport = self.response.json()["tcpPort"]
#         self.response = requests.post(self.host + "/rest/rec/measurements")
#
#
#     def GetFs(self):
#         # Sample rate is found by doubling the channel bandwidth and finding the closest supported sample rate
#         # Channel bandwidth is found in the channel setup, it is in string format, so to get it as a number replace khz with *1000 and evaluate
#
#         bandwidth = self.setup["channels"][0]["bandwidth"]
#         bandwidth = bandwidth.replace('kHz', '*1000')
#         bandwidth = eval(bandwidth)
#         self.response = requests.get(self.host + "/rest/rec/module/info")
#         module_info = self.response.json()
#         supported_sample_rates = module_info["supportedSampleRates"]
#         # Find the sample rate with the minimum difference to bandwidth * 2
#         #Tu by som to mohol mozno upravit manualne na inu hodnotu lebo inak to dava cez 51.2kHz
#         self.sample_rate = min(supported_sample_rates, key = lambda x:abs(x - bandwidth * 2))
#         #print(f"sample rate: {self.sample_rate} hz")
class LanXI:
    def __init__(self, ip,channel_info,sampling_freq= "51.2 kHz"):
        self.ip = ip
        self.host = "http://" + self.ip
        self.channel_info=channel_info
        self.sampling_freq=sampling_freq

    def setup_stream(self):
        """
        Setup of channel 1 with a microphone
        """
        # This setup is indentical to the one found in "Streaming.py", refer to this for more info.
        # Open recorder application
        requests.put(self.host + "/rest/rec/open")
        # Get information about the device and configure
        self.GetTeds()
        self.ConfigureStream()
        #self.GetFs()

    def GetTeds(self):
        # Start TEDS detection, we then check when it is done and read it out as JSON
        # Detect TEDS
        self.response = requests.post(self.host + "/rest/rec/channels/input/all/transducers/detect")
        while requests.get(self.host + "/rest/rec/onchange").json()["transducerDetectionActive"]:
            pass
        # Get TEDS information
        self.response = requests.get(self.host + "/rest/rec/channels/input/all/transducers")
        self.channels = self.response.json()
        #
        # self.channels[0] = {
        #     "direction": "",
        #     "requires200V": 0,
        #     "requiresCcld": 1,
        #     "sensitivity": 0.009755,
        #     "serialNumber": 3036667,
        #     "teds": "EdAFEar9Khcw0HsQ4wUAICAgICAgICAgICAgICAgIA==",
        #     "unit": "m/s2"
        # }
        print(f"Resposnse y GET TEDS{self.response.json()}")  ###########

    def ConfigureStream(self):
        # To start a stream we first need to set a configuration. In this example we create a configuration by requesting a default channel setup.
        # We use a tiny utility function to update all values with a given key.
        # Create a new recording
        self.response = requests.put(self.host + "/rest/rec/create")
        # Get Default setup for channels
        self.response = requests.get(self.host + "/rest/rec/channels/input/default")
        self.setup = self.response.json()
        print(f"Default setup {self.setup}")
        # Replace stream destination from default SD card to socket
        utility.update_value("destinations", ["socket"], self.setup)
        # Set enabled to false for all channels
        utility.update_value("enabled", False, self.setup)
        utility.update_value("bandwidth",self.sampling_freq,self.setup)
        # # Enable channels with valid TEDS ####################################
        # # for channel_nr in range(len(self.channels)):
        # #     if self.channels[channel_nr] != None:
        # self.setup["channels"][0]["transducer"] = {'direction': '', 'requires200V': 0, 'requiresCcld': 1,
        #                                            'sensitivity': 0.009755,
        #                                            'serialNumber': 3036667,
        #
        #                                            'type': {'model': 'A', 'number': '4189', 'prefix': '',
        #                                                     'variant': '021'},
        #                                            'unit': 'Pa'}
        # self.setup["channels"][0]["enabled"] = True
        # self.setup["channels"][0]["ccld"] = self.channels[0]["requiresCcld"]
        # # Tu potrebujem kod zautomatizovat aby si uzivatel zvolil co chce
        # self.setup['channels'][0]['bandwidth'] = '3.2 kHz'

        #Konfiguracia na zaklade uzivatela pre senzory bez TEDS
        for i,ch in enumerate(self.setup['channels']):
            if self.channel_info[i]['enabled']:
                ch['transducer'] = {
                    "requires200V": 0,
                    "requiresCcld": 1,
                    "sensitivity": self.channel_info[i]['sensitivity'],
                    "unit":self.channel_info[i]['unit']
                    }
                self.setup["channels"][i]["enabled"] = True
                self.setup['channels'][i]['ccld'] = True
                self.setup['channels'][i]['polvolt'] = 0
                self.setup['channels'][i]['name']=self.channel_info[i]['name']
                print(f"Channel {i+1} name is {self.channel_info[i]['name']}")

            else:
                self.setup['channels'][i]['enabled'] = False

            # Konfiguracia na zaklade TEDS, ak je pritomny TEDS senzor, je prepisany uzivatelom zadane info
        for idx, t in enumerate(self.channels):
            if t is not None:
                self.setup["channels"][idx]["transducer"] = t
                self.setup["channels"][idx]["ccld"] = t["requiresCcld"]
                self.setup["channels"][idx]["polvolt"] = t["requires200V"]
                print(f'Channel {idx + 1}: {t["type"]["number"] + " s/n " + str(t["serialNumber"])}, '
                      f'CCLD {"On" if t["requiresCcld"] == 1 else "Off"}, '
                      f'Polarization Voltage {"on" if t["requires200V"] == 1 else "off"}')


        # Remove None channels
        # self.channels = list(filter(lambda x : x != None, self.channels))
        # if not any(self.channels):
        #     print("No channels enabled! Did you connect a microphone?")
        #     exit()
        # Next we setup the input channels for streaming. We use the input setup we got previosly.
        # Create input channels with the setup
        print(f"Setup after {self.setup}")
        print(f"Channel info {self.channel_info}")
        self.response = requests.put(self.host + "/rest/rec/channels/input", json=self.setup)
        # Get streaming socket
        self.response = requests.get(self.host + "/rest/rec/destination/socket")
        self.inputport = self.response.json()["tcpPort"]
       # self.response = requests.post(self.host + "/rest/rec/measurements")
        ##POTIALTO sa musim dostat aby to bolo ready a bolo to stale zelene

    # def GetFs(self):
    #     # Sample rate is found by doubling the channel bandwidth and finding the closest supported sample rate
    #     # Channel bandwidth is found in the channel setup, it is in string format, so to get it as a number replace khz with *1000 and evaluate
    #
    #     bandwidth = self.setup["channels"][0]["bandwidth"]
    #     bandwidth = bandwidth.replace('kHz', '*1000')
    #     bandwidth = eval(bandwidth)
    #     self.response = requests.get(self.host + "/rest/rec/module/info")
    #     module_info = self.response.json()
    #     supported_sample_rates = module_info["supportedSampleRates"]
    #     # Find the sample rate with the minimum difference to bandwidth * 2
    #     # Tu by som to mohol mozno upravit manualne na inu hodnotu lebo inak to dava cez 51.2kHz
    #     self.sample_rate = min(supported_sample_rates, key=lambda x: abs(x - bandwidth * 2))
    #     # print(f"sample rate: {self.sample_rate} hz")

    def dicsconnect_from_LANXI(self):
        requests.put(self.host + "/rest/rec/measurements/stop")
        requests.put(self.host + "/rest/rec/finish")
        requests.put(self.host + "/rest/rec/close")

