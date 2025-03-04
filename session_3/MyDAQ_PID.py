import nidaqmx as dx
from nidaqmx import stream_readers
import numpy as np
import time

class MyDAQ_PID():
    def __init__(self,
                 setpoint,
                 min_output,
                 max_output,
                 samplerate:int=200_000,
                 name:str='myDAQ3',
                 feedback_rate:int=20,
                 feedback_cycles:int=100,
                 kp=0, ki=0, kd=0,
                 ):
        self.__setpoint = setpoint
        self.min = min_output
        self.max = max_output
        
        self.samplerate = samplerate
        self.name = name
        self.feedback_rate = feedback_rate
        self.feedback_cycles = feedback_cycles
        
        self.__kp = kp
        self.__ki = ki
        self.__kd = kd
        
        self.continuous = dx.constants.AcquisitionType.CONTINUOUS
        
    @property
    def kp(self):
        return self.__kp
    
    @kp.setter
    def kp(self, value):
        assert isinstance(value, (int, float)), "kp must be a number"
        self.__kp = value
    
    @property
    def ki(self):
        return self.__ki
    
    @ki.setter
    def ki(self, value):
        assert isinstance(value, (int, float)), "ki must be a number"
        self.__ki = value
    
    @property
    def kd(self):
        return self.__kd
    
    @kd.setter
    def kd(self, value):
        assert isinstance(value, (int, float)), "kd must be a number"
        self.__kd = value
    
    @property
    def setpoint(self):
        return self.__setpoint
    
    @setpoint.setter
    def setpoint(self, value):
        assert isinstance(value, (int, float)), "setpoint must be a number"
        self.__setpoint = value
    
    
    def feedback_function(self):
        data = np.concatenate(self.data)
        # data = self.data[-1]
        
        error = self.setpoint - data
        
        timelength = data.size / self.samplerate
        time = np.linspace(0, timelength, data.size)
        integral = np.trapz(error, time)
        derivative = np.gradient(error, time)[-1]
        
        feedback = self.kp * error[-1]
        feedback += self.ki * integral
        feedback += self.kd * derivative
        
        if feedback < self.min:
            feedback = self.min
        elif feedback > self.max:
            feedback = self.max
        
        return feedback
    
    def reading_task_callback(self,
                              task_idx,
                              event_type,
                              num_samples,
                              callback_data,
                              ):
        self.__repeats += 1
        buffer = np.zeros((1, num_samples), dtype=np.float64)
        self.reader.read_many_sample(buffer, num_samples)
        
        self.data.append(buffer[0])
        # print(len(self.data))
        
        feedback = self.feedback_function()
        
        print(f"Writing {feedback:.2f} Volts to AO0".rjust(50))
        self.writeTask.write(feedback, auto_start=True)
        self.writeTask.stop()
        
        return 0

    
    def measure(self):
        print("Starting feedback loop")
        self.__repeats = 0
        self.data = []
        
        samples_per_buffer = int(self.samplerate / self.feedback_rate)
        
        with dx.Task('AOTask') as self.writeTask, dx.Task('AITask') as self.readTask:
            self.readTask.ai_channels.add_ai_voltage_chan(f'{self.name}/ai0')
            self.writeTask.ao_channels.add_ao_voltage_chan(f'{self.name}/ao0')
            
            self.readTask.timing.cfg_samp_clk_timing(self.samplerate, sample_mode=self.continuous)
            self.reader = stream_readers.AnalogMultiChannelReader(self.readTask.in_stream)
            
            self.readTask.register_every_n_samples_acquired_into_buffer_event(samples_per_buffer, self.reading_task_callback)
            self.readTask.start()
            
            time.sleep(5)
            self.readTask.stop()
            self.writeTask.write(0, auto_start=True)
            self.writeTask.stop()
        
        # return np.concatenate(self.data)
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, value):
        self.__data = value