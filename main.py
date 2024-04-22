from PyQt6.QtWidgets import QMainWindow,QApplication, QPushButton,QComboBox,QLabel,QCheckBox,QFileDialog,QLineEdit,QVBoxLayout, QWidget, QSplitter
from PyQt6 import uic
import sys
import os
import interpretation

import recorder
from process_hdf5 import process_data
from offline import Analyser
from  RealTimePyQt import FigHandler, StreamThread

from HelpFunctions.lanxi import LanXI



class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        #Load USER INTERFACE .ui
        self.graphwindow = None
        self.dataset=None
        uic.loadUi('UserInt.ui',self)
        #Define QWidgets
        #BUTTONS

        self.button=self.findChild(QPushButton,"pushButton")
        self.button2 = self.findChild(QPushButton, "pushButton_2")
        self.button3 = self.findChild(QPushButton, "pushButton_3")
        self.button4 = self.findChild(QPushButton, "pushButton_4")
        self.button5 = self.findChild(QPushButton, "pushButton_5")
        self.button6 = self.findChild(QPushButton, "pushButton_6")
        self.button7 = self.findChild(QPushButton, "pushButton_7")
        self.button8 = self.findChild(QPushButton, "pushButton_8")
        self.button9 = self.findChild(QPushButton, "pushButton_9")
        #LABELS
        self.label=self.findChild(QLabel,'label')
        self.label2 = self.findChild(QLabel, 'label2')
        self.label3= self.findChild(QLabel,'label3')
        #COMOBOBOX
        self.combobox=self.findChild(QComboBox,'comboBox')
        self.combobox2 = self.findChild(QComboBox, 'comboBox_2')
        self.combobox3 = self.findChild(QComboBox, 'comboBox_3')
        self.combobox4 = self.findChild(QComboBox, 'comboBox_4')

        # LINE EDIT
        self.line = self.findChild(QLineEdit, "lineEdit")
        self.line2 = self.findChild(QLineEdit, "lineEdit_2")
        self.line3 = self.findChild(QLineEdit, "lineEdit_3")
        self.line4 = self.findChild(QLineEdit, "lineEdit_4")
        self.line5 = self.findChild(QLineEdit, "lineEdit_5")
        self.line6 = self.findChild(QLineEdit, "lineEdit_6")
        self.line7 = self.findChild(QLineEdit, "lineEdit_7")
        self.line8 = self.findChild(QLineEdit, "lineEdit_8")
        self.line9 = self.findChild(QLineEdit, "lineEdit_9")
        self.line10 = self.findChild(QLineEdit, "lineEdit_10")
        self.line11 = self.findChild(QLineEdit, "lineEdit_11")
        self.line12 = self.findChild(QLineEdit, "lineEdit_12")
        self.line13 = self.findChild(QLineEdit, "lineEdit_13")
        self.line14 = self.findChild(QLineEdit, "lineEdit_14")
        self.line15 = self.findChild(QLineEdit, "lineEdit_15")
        self.line16 = self.findChild(QLineEdit, "lineEdit_16")
        self.line17 = self.findChild(QLineEdit, "lineEdit_17")
        self.line18 = self.findChild(QLineEdit, "lineEdit_18")
        self.line19 = self.findChild(QLineEdit, "lineEdit_19")
        self.line20 = self.findChild(QLineEdit, "lineEdit_20")
        self.line21 = self.findChild(QLineEdit, "lineEdit_21")
        self.line22 = self.findChild(QLineEdit, "lineEdit_22")



        self.checkbox=self.findChild(QCheckBox, 'checkBox')
        self.checkbox2 = self.findChild(QCheckBox, 'checkBox_2')
        self.checkbox3 = self.findChild(QCheckBox, 'checkBox_3')
        self.checkbox4 = self.findChild(QCheckBox, 'checkBox_4')
        self.checkbox5 = self.findChild(QCheckBox, 'checkBox_5')
        self.checkbox6 = self.findChild(QCheckBox, 'checkBox_6')
        self.checkbox7 = self.findChild(QCheckBox, 'checkBox_7')
        self.checkbox8 = self.findChild(QCheckBox, 'checkBox_8')

        self.button.clicked.connect(self.select_file_and_combobox) #
        #self.button2.clicked.connect(self.apply_channel)#
        self.button3.clicked.connect(self.start_analyser) # plot
        self.button4.clicked.connect(self.dostanem_list_s_funkciami_ciar)
        self.button5.clicked.connect(self.liveFFT)
        self.button6.clicked.connect(self.startRecorder)
        self.button7.clicked.connect(self.disconnect_from_LANXI)
        self.button8.clicked.connect(self.remove_freq)
        self.button9.clicked.connect(self.connect_to_LANXI)


        self.ip_adress = self.line7.text()



    def select_file_and_combobox(self):
        # open file dialog
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', "HDF5 (*.h5)")
        print(self.filename)
        self.path = self.filename
        self.combobox.clear()
        # output
        if self.filename:
            self.filename = os.path.basename(self.filename)
            self.label.setText(f"Selected file: {str(self.filename)}")
            self.dataset = process_data(self.path)
            self.list_of_data = self.dataset.get_group_keys()
            self.combobox.addItems(self.list_of_data)
        return self.path

    def get_time_channel(self):
        self.list_of_data = self.dataset.get_group_keys()
        for i in self.list_of_data:
            if 'time' in i.lower():
                TimeChannel= i
        return TimeChannel

    def apply_channel(self):
        self.currentText = self.combobox.currentText()
        self.label2.setText(f"Selected channel:{self.currentText}")

        return self.currentText

    def dostanem_dict_s_freq(self):

        self.list_of_values = []
        self.d1=int(self.line.text())
        self.d2=int(self.line2.text())
        self.z1 = int(self.line3.text())
        self.z2 = int(self.line4.text())
        self.beta=int(self.line5.text())
        self.n = int(self.line6.text())
        #self.list_of_values.extend([self.d1,self.d2,self.z1,self.z2,self.beta,self.n] )
        #print(self.list_of_values)
        self.freq=self.dataset.get_fault_freq(self.d1,self.d2,self.z1,self.z2,self.n,self.beta)
        accuracy=int(self.line22.text())
        dict1 = self.graphwindow.filter_freq(accuracy=accuracy)
        self.freq.update(dict1)
        print(self.freq)

        return self.freq


    def dostanem_list_s_funkciami_ciar(self):
        self.graphwindow.handle_lines(self.dostanem_dict_s_freq())


    def start_analyser(self):
        self.currentText = self.combobox.currentText()
        self.label2.setText(f"Selected channel:{self.currentText}")
        self.graphwindow=Analyser(self.path,self.currentText,cmap=self.combobox4.currentText(),
                                  resolution=float(self.combobox3.currentText()),Time=self.checkbox.isChecked(),
                                  FFT=self.checkbox2.isChecked(),Spectrogram=self.checkbox3.isChecked(),logScale=self.checkbox4.isChecked(),
                                  timeChannel=self.get_time_channel())
        self.graphwindow.show()

    def remove_freq(self):
        self.graphwindow.clear_lines()
        print("Cleared")

    def liveFFT(self):
        self.IP=self.line7.text()
        sampling_freq = self.combobox2.currentText()
        self.channel_info = self.dostanem_channel_info()

        lanxi = LanXI(self.IP,sampling_freq=sampling_freq,channel_info=self.channel_info)
        lanxi.setup_stream()
        streamer = StreamThread(lanxi)
        streamer.start()

        self.live = FigHandler(lanxi, streamer)
        self.live.show()


    def dostanem_channel_info(self):

        self.channels= [
            {
            'enabled':self.checkbox5.isChecked(),
            'name':self.line10.text(),
            'sensitivity':float(self.line14.text()),
            'unit': self.line18.text()
            },
            {
            'enabled': self.checkbox6.isChecked(),
            'name':self.line11.text(),
            'sensitivity':float(self.line15.text()),
            'unit': self.line19.text()
            },
            {
            'enabled': self.checkbox7.isChecked(),
            'name':self.line12.text(),
            'sensitivity':float(self.line16.text()),
            'unit': self.line20.text()
            },
            {
            'enabled': self.checkbox8.isChecked(),
            'name': self.line13.text(),
            'sensitivity': float(self.line17.text()),
            'unit': self.line21.text()
            }
        ]

        return self.channels
    ###Nepotrebne
    def slovnik(self):
        chan=self.dostanem_channel_info()
        for i,ch in enumerate(chan):
            if float(chan[i]['sensitivity']) > 0:
                print(chan[i]['sensitivity'])
                print(chan[i]['enabled'])
                chan[i]['enabled']='True'
        print(chan)


    def startRecorder(self):
        self.name_of_file=self.line8.text()
        self.record_time = int(self.line9.text())
        self.sampling_freq = self.combobox2.currentText()

        self.channel_info=self.dostanem_channel_info()
        recorder.Recorder(name_of_file=self.name_of_file,record_time=self.record_time,sampling_freq=self.sampling_freq,ip_adress=self.ip_adress,channel=self.channel_info)
        interpretation.Parser(name_of_file=f"{self.name_of_file}{self.sampling_freq}.stream",channel_info=self.channel_info)

    def disconnect_from_LANXI(self):
        self.channel_info = self.dostanem_channel_info()
        Lanxi = LanXI(self.ip_adress,self.channel_info)
        Lanxi.dicsconnect_from_LANXI()

    def connect_to_LANXI(self):
        self.channel_info = self.dostanem_channel_info()
        self.sampling_freq = self.combobox2.currentText()
        Lanxi = LanXI(self.ip_adress,self.channel_info,sampling_freq=self.sampling_freq)
        Lanxi.setup_stream()



app=QApplication(sys.argv)
window=UI()
window.show()
app.exec()