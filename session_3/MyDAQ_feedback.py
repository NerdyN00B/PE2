import nidaqmx as dx
from nidaqmx import stream_readers
import numpy as np

#Set the sample_rate
sample_rate = 10000

#Set the feedback rate
feedback_rate = 5 
#perform feedback 5 times per second; thus we ask the computer to calculate the feedback within 200 ms
time_per_cycle = 1 / feedback_rate
samples_per_buffer = int(sample_rate * time_per_cycle)

#This program will read and write continuously; stops when 'enter' is pressed
#The readtask reads 'samples_per_buffer' amount of samples (buffer size) and stores it in the buffer
#After reading the buffer size, it will change its output, defined by 'feedback'
#feedback is initially just taking the mean of the data in the buffer, and you should change it to
#a proper feedback signal.
#You can also play around with the sample_rate and the buffer size; check how this changes the 
#'response' of our feedback system: how quickly it is able to measure and write a feedback signal

#This function is used to generate a feedback signal. 
#Change this function to implement your own feedback!
def feedbackFunction(data):
	return np.mean(data)

#This function is called every time after the buffer is filled
def reading_task_callback(task_idx, event_type, num_samples, callback_data):	
	#Get the data out of the buffer
	buffer = np.zeros((1, num_samples), dtype=np.float64)
	reader.read_many_sample(buffer, num_samples)
	
	#Read the first channel.
	data = buffer[0]
	
	#Manipulate the data here to get the value for the feedback.
	feedback = feedbackFunction(data)
	
	#Write the feedback to AO0.
	writeTask.write(feedback, auto_start = True)
	writeTask.stop()
	
	#Return 0 to indicate that we did not get an error.
	return 0

with dx.Task('AOTask') as writeTask, dx.Task('AITask') as readTask:
    print("Initializing program")
    #Add the channels to the read and write task
    readTask.ai_channels.add_ai_voltage_chan('myDAQ1/ai0')
    writeTask.ao_channels.add_ao_voltage_chan('myDAQ1/ao0')
    
    readTask.timing.cfg_samp_clk_timing(sample_rate,sample_mode = dx.constants.AcquisitionType.CONTINUOUS)
    reader = stream_readers.AnalogMultiChannelReader(readTask.in_stream)
    
    #Start the task for reading and calling the function after every buffer cycle
    readTask.register_every_n_samples_acquired_into_buffer_event(samples_per_buffer, reading_task_callback)
    readTask.start()
    
    #Condition to stop the feedback
    input('Reading.\nPress enter to stop')