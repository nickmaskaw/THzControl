import tkinter as tk
from tkinter import ttk
import time as tm
import sys
import clr
from System import String
from System import Decimal
from System.Collections import *

if not r'C:\Program Files\Thorlabs\Kinesis' in sys.path:
    sys.path.append(r'C:\Program Files\Thorlabs\Kinesis')
    
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI

clr.AddReference("Thorlabs.MotionControl.KCube.BrushlessMotorCLI")
from Thorlabs.MotionControl.KCube.BrushlessMotorCLI import KCubeBrushlessMotor


class KBD101:
    def __init__(self, default_serial):
        self._default_serial = default_serial
        self._device         = None
        self._motor_config   = None
        self._widget         = False
        self._connected      = False
        
    @property
    def is_connected(self): return self._connected
        
    def create_widget(self, frame, row):
        if not self._widget:
            self._widget = True
            default_serial = self._default_serial
            options = {'sticky': tk.W, 'padx': 5, 'pady': 5}

            self._label   = ttk.Label(frame, text="Delay line:", width=10)
            self._serial  = tk.StringVar(value=default_serial)
            self._entry   = ttk.Entry(frame, textvariable=self._serial, width=40)
            self._button  = ttk.Button(frame, text="Connect", command=self._button_clicked)
            self._value   = tk.StringVar(value="")
            self._visual  = ttk.Entry(frame, textvariable=self._value, width=20, state='disabled')
            self._get_btn = ttk.Button(frame, text="Get", command=self._button_get, state='disabled')
            self._set_btn = ttk.Button(frame, text="Set", command=self._button_set, state='disabled')

            self._label.grid(row=row, column=0, **options)
            self._entry.grid(row=row, column=1, **options)
            self._button.grid(row=row, column=2, **options)
            self._visual.grid(row=row, column=3, **options)
            self._get_btn.grid(row=row, column=4, **options)
            self._set_btn.grid(row=row, column=5, **options)
            
            print("Delay line widget successfully created")
        else:
            print("Delay line widget already exists")
        
    def _button_clicked(self):
        if self._button['text'] == "Connect":
            self.connect()
        elif self._button['text'] == "Disconnect":
            self.disconnect()
            
    def _button_get(self):
        self.request_pos()
        self._value.set(self.get_pos())
    
    def _button_set(self):
        self.return_to(self._value.get())
        
    def widget_enable(self):
        if self._widget and self._connected:
            self._button['state']  = 'normal'
            self._visual['state']  = 'normal'
            self._get_btn['state'] = 'normal'
            self._set_btn['state'] = 'normal'
        print("Delay line widget enabled")
            
    def widget_disable(self):
        if self._widget and self._connected:
            self._button['state']  = 'disabled'
            self._visual['state']  = 'disabled'
            self._get_btn['state'] = 'disabled'
            self._set_btn['state'] = 'disabled'
        print("Delay line widget disabled")
            
    def connect(self, manual_serial=None):
        serial = self._serial.get() if not manual_serial else manual_serial
        try:
            self._device = self._build_device(serial)
            self._device.Connect(serial)
            tm.sleep(.2)
            self._motor_config = self._load_motor_config(serial)
            self._connected = True
            if self._widget:
                self._button['text']   = "Disconnect"
                self._entry['state']   = 'disabled'
                self._visual['state']  = 'normal'
                self._get_btn['state'] = 'normal'
                self._set_btn['state'] = 'normal'
                self._button_get()
            info = self.get_info()
            print("Connected delay line: {} (serial no. {}) | Stage: {} (serial no. {})".format(*tuple(info.values())))
        except:
            print("Failed to connect the delay line")
            
    def disconnect(self):
        try:
            self._device.Disconnect()
            self._connected = False
            if self._widget:
                self._button['text']   = "Connect"
                self._entry['state']   = 'normal'
                self._visual['state']  = 'disabled'
                self._get_btn['state'] = 'disabled'
                self._set_btn['state'] = 'disabled'
            print("Disconnected the delay line")
        except:
            print("Failed to disconnect the delay line")        
    
    def _build_device(self, serial):
        if isinstance(serial, str) and serial[:2] == '28':
            DeviceManagerCLI.BuildDeviceList()
            device_list = DeviceManagerCLI.GetDeviceList()
            
            if serial in device_list:
                device = KCubeBrushlessMotor.CreateKCubeBrushlessMotor(serial)
                return device
            else:
                print('Check if the intended serial number is listed below:')
                print(device_list)
                return None
        else:
            print('Check if the intended serial number is a string that begins with "28".')
            return None
        
    def _load_motor_config(self, serial):
        motor_config = self._device.LoadMotorConfiguration(serial)
        return motor_config
    
    def get_info(self):
        device_info = self._device.GetDeviceInfo()
        stage_info  = self._device.GetStageDefinition()
        useful_info = {'deviceName'   : device_info.Name,
                       'deviceSerial' : device_info.SerialNumber,
                       'stageName'    : stage_info.PartNumber,
                       'stageSerial'  : stage_info.SerialNumber}
        return useful_info
    
    def enable(self):
        self._device.EnableDevice()
        tm.sleep(2)
        
    def disable(self):
        self._device.DisableDevice()
    
    def start_polling(self, rate=50):
        self._device.StartPolling(rate)
        
    def stop_polling(self):
        self._device.StopPolling()
        
    def get_polling_rate(self):
        return self._device.PollingDuration()
        
    def home(self, polling_rate=50, timeout=60000):
        poll = False if self.get_polling_rate() else True
        
        if poll: self.start_polling()
        self._device.Home(timeout)
        if poll: self.stop_polling()
            
    def move_to(self, pos, timeout=60000):
        self._device.MoveTo(Decimal(float(pos)), timeout)
        
    def return_to(self, pos, timeout=60000):
        self.set_vel(100)
        self.move_to(pos, timeout)
        
    def request_pos(self):
        self._device.RequestPosition()
        
    def get_pos(self):
        pos = str(self._device.Position).replace(',', '.')
        return float(pos)
    
    def get_vel(self):
        vel = str(self._device.GetVelocityParams().MaxVelocity).replace(',', '.')
        return float(vel)
    
    def set_vel(self, vel, acceleration=999):
        self._device.SetVelocityParams(Decimal(vel), Decimal(acceleration))