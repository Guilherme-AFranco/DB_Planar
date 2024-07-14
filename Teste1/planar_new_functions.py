from nptdms import TdmsFile
import concurrent.futures
from IPython.display import display
import pandas as pd
#import numpy as np # Precisa apenas para a func mean_3 # versão atualizada não precisa
import os

from planar_functions import *

def media_calibrations_tdsm(path_calib_tdsm_list): #Retorna e plota a média de um conjuto de arquivos tdsm
  mean_list = []
  for elements in path_calib_tdsm_list:
    if elements.endswith("tdms"):
      conv = 2/(2**16-1)
      calib_tdsm = TdmsFile.read(elements).as_dataframe().multiply(-1).multiply(conv)
      abc, cdf = mean_3(calib_tdsm)
      mean_list.append(abc)
  #display(mean_list)
  mean_list = pd.concat(mean_list).groupby(level=0).mean()
  #display(mean_list)
  #plot_color_map(mean_list)
  return mean_list

#def calibrations_tdsm(calib_tdsm_file): #Retorna e plota a média de um conjuto de arquivos tdsm
#  mean_list = []
#  for elements in calib_tdsm_file:
#    if elements.endswith("tdms"):
#      #conv = 2/(2**16-1)
#      calib_tdsm = TdmsFile.read(elements).as_dataframe()#.multiply(-1).multiply(conv)
#      #abc, cdf = mean_3(calib_tdsm)
#      #mean_list.append(abc)
#      mean_list.append(calib_tdsm)
#  #display(mean_list)
#  #mean_list = pd.concat(mean_list).groupby(level=0).mean()
#  #display(mean_list)
#  #plot_color_map(mean_list)
#  return mean_list


def process_file(file):
    if file.endswith("tdms"):
        return TdmsFile.read(file).as_dataframe()

def calibrations_tdsm(calib_tdsm_file): 
    mean_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_file, calib_tdsm_file)
        for result in results:
            if result is not None:
                mean_list.append(result)
    return mean_list