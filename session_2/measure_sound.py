import sys
import os
import inspect

parentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from mydaq_long import MyDAQ_Long
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

daq = MyDAQ_Long()
