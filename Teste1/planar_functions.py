from nptdms import TdmsFile
from IPython.display import display
import pandas as pd
#import numpy as np # Precisa apenas para a func mean_3 # versão atualizada não precisa
import os

#from matplotlib import colormaps
#cmap = 
#list(colormaps)
import matplotlib.pyplot as plt
#from matplotlib import cm
#cmap = cm.get_cmap('Spectral')

#Desconcatena e Realiza a média da matriz na terceira dimensão
def mean_3(dataframe): #Versão atualizada no mean_3
  x_axis_atual = dataframe.shape[0]
  x_axis_original = 32 ## Número no tdms original // x = rows
  z_axis_original = x_axis_atual/x_axis_original

  not_concatened_df = []
  for i in range(int(z_axis_original)):
    not_concatened_df.append(dataframe.iloc[32*(i):32*(i+1)].copy().reset_index().drop(columns=['index']))

  df = not_concatened_df[0].copy()
  for elements in not_concatened_df[1:]:
    df += elements.values
  df = df/len(not_concatened_df)

  return df, not_concatened_df

#Lê todos os arquivos em uma pasta e retorna o full path
def absoluteFilePaths(directory):
    all_files = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            all_files.append(os.path.abspath(os.path.join(dirpath, f)))
    return all_files

#Plota individualmente um colormap dando um path de um arquivo tdms ou a partir dataframe
def plot_color_map(path_calib_tdsm):
  if isinstance(path_calib_tdsm, pd.DataFrame):
    fig, axs = plt.subplots(1, 1)
    graf = axs.matshow(path_calib_tdsm, cmap='Blues', aspect='auto')
    plt.colorbar(graf)
    return
  conv = 2/(2**16-1)
  calib_tdsm = TdmsFile.read(path_calib_tdsm).as_dataframe().multiply(-1).multiply(conv) # leer VH y negarlo
  abc, cdf = mean_3(calib_tdsm)

  name_file = path_calib_tdsm.split("\\")[-1]
  fig, axs = plt.subplots(1, 1)
  fig.suptitle('Média Temporal: '+name_file)
  graf = axs.matshow(abc.to_numpy(), cmap='Blues', aspect='auto') # aparentemente posso retirar o to_numpy()
  #print(abc.to_numpy())
  #plt.colorbar(graf)
  #plt.savefig("") #Ajustar path do folder

def plot_color_map_duo(path_calib_tdsm,media_total_calibrations,current_directory, save_path=""):
  name_file = path_calib_tdsm.split("\\")[-1]
  fig, axs = plt.subplots(1, 2)
  fig.suptitle('Média Temporal e Diferença da média: '+name_file)

  conv = 2/(2**16-1)
  calib_tdsm = TdmsFile.read(path_calib_tdsm).as_dataframe().multiply(-1).multiply(conv)
  abc, cdf = mean_3(calib_tdsm)
  #colormap 1
  graf = axs[0].matshow(abc, cmap='Blues', aspect='auto')
  #colormap 2
  graf = axs[1].matshow(abc-media_total_calibrations, cmap='Blues', aspect='auto')

  #plt.colorbar(graf)
  if not os.path.exists(current_directory+"\\Resultados"):
    os.makedirs(current_directory+"\\Resultados")

  if save_path == "":
    plt.savefig(current_directory+"\\Resultados\\"+name_file+".png")
  else:
    if not os.path.exists(current_directory+"\\Resultados\\"+save_path):
      os.makedirs(current_directory+"\\Resultados\\"+save_path)
    plt.savefig(current_directory+"\\Resultados\\"+save_path+"\\"+name_file+".png")

#Plota 3 colormaps (média temporal e diferença da média das calibrações) dando um path de um arquivo tdms
#alt 1: printar junto a média total
#alt 2: dividir pela média total ao invés de subtrair
#alt 3: dividir pelo vhmax
def plot_color_map_trio(path_calib_tdsm,media_total_calibrations,current_directory, save_path=""):
  name_file = path_calib_tdsm.split("\\")[-1]
  fig, axs = plt.subplots(1, 3)
  fig.suptitle('Média Temporal, V-MED ou V-Max, Div da média: '+name_file)

  conv = 2/(2**16-1)
  calib_tdsm = TdmsFile.read(path_calib_tdsm).as_dataframe().multiply(-1).multiply(conv)
  abc, cdf = mean_3(calib_tdsm)
  #colormap 1
  graf = axs[0].matshow(abc, cmap='Blues', aspect='auto')
  #colormap 2
  graf = axs[1].matshow(media_total_calibrations, cmap='Blues', aspect='auto')
  #colormap 3
  graf = axs[2].matshow(abc.div(media_total_calibrations), cmap='Blues', aspect='auto')
  
  #print("abc")
  #display(abc)
  #print("v-med")
  #display(media_total_calibrations)
  #https://stackoverflow.com/questions/13784201/how-to-have-one-colorbar-for-all-subplots
  fig.subplots_adjust(right=0.8)
  cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
  fig.colorbar(graf, cax=cbar_ax)
  
  if not os.path.exists(current_directory+"\\Resultados"):
    os.makedirs(current_directory+"\\Resultados")

  if save_path == "":
    plt.savefig(current_directory+"\\Resultados\\"+name_file+".png")
  else:
    if not os.path.exists(current_directory+"\\Resultados\\"+save_path):
      os.makedirs(current_directory+"\\Resultados\\"+save_path)
    plt.savefig(current_directory+"\\Resultados\\"+save_path+"\\"+name_file+".png")

#inserir a lista de paths tdms e retorna um dict apenas com os necessários
def dict_por_espessura(lista_tdms):
    calibrations_dict_path = {}
    #print(lista_tdms)
    for elements in lista_tdms: #Cria um dict com key = espessura do filme, e os valores os paths
        if elements.endswith(".tdms"):
            elements_name = elements.split("\\")[-1]
            if "_" in elements_name:
                elements_size = elements_name.split("_")[1]
                #elements_numb = elements_name.split("_")[2].split(".")[0]
            elif "-" in elements_name:
                elements_size = elements_name.split("-")[0]
                #elements_numb = elements_name.split("-")[1].split(".")[0]

            if not elements_size in calibrations_dict_path:
                calibrations_dict_path[elements_size] = [elements]
            else:
                calibrations_dict_path[elements_size].append(elements)
        
    for elements in calibrations_dict_path: # Sort especial para deixar em ordem pois o sort normal não funciona (testar caso tenha mais de 20)
        for i in range(len(calibrations_dict_path[elements])-9):
            calibrations_dict_path[elements] += [calibrations_dict_path[elements].pop(1)]

    #display(calibrations_dict_path)
    for elements in calibrations_dict_path: # remove os elementos repetidos no caso 1,2... quando maior que 16 // agora pode ser simplificado já que crie o sort, mas contua rápido e elaborado caso mude no futuro
        if len(calibrations_dict_path[elements]) > 16:
            for i in range(len(calibrations_dict_path[elements])-16):
                contador = 0
                for j in calibrations_dict_path[elements]:
                    if "-"+str(i+1)+"." in j:
                        calibrations_dict_path[elements].pop(contador)
                    elif "_"+str(i+1)+"." in j:
                        calibrations_dict_path[elements].pop(contador)
                    contador+=1
    #display(calibrations_dict_path)
    return calibrations_dict_path