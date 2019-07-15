#!/usr/bin/python
import pymongo
import json
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft
import sys
import numpy as np

###################################
# read data from database
###################################
def fillData(curveName, arrX, arrY):
  collist = mydb.list_collection_names()
  # check it exists
  if curveName not in collist:
    print(curveName + " does not exists")
    exit()

  # get cursor
  mycol = mydb[curveName]
  cursor = mycol.find()
  count = mycol.count_documents({})
  print(str(count)+" values found for "+ curveName)

  # fill array
  originOfTime = 1563038100008
  for i in range(0,count):
    if(curveName[0:4]=="fake"):
      value = cursor[i]["_id"]
    else:
      value = (cursor[i]["_id"]-originOfTime)/(24*60*60*1000)
    arrX.append(value)
    arrY.append(cursor[i]["value"])

###################################
# Plot
###################################
def cryptoPlot(arrX, arrY):
  plt.plot(arrX, arrY)
  plt.grid()
  plt.show()

###################################
# FFT
###################################
def cryptoFFT(arrX, arrY, *args, **kwargs):
  count = len(arrX)
  yf = fft(arrY)
  xf = np.linspace(arrX[0], arrX[-1], count//2)
  print(xf)
  fig, [ax1, ax2] = plt.subplots(2, 1, sharex=False)

  maxVal = np.amax(yf)
  print(maxVal)

  cap = kwargs.get('cap', None)
  if(cap is None):
    ax1.plot(xf, np.abs(yf[0:count//2] /maxVal), color="red")
  else:
    ax1.plot(xf, np.clip(np.abs(yf[0:count//2] /maxVal), 0, cap))
  ax2.plot(arrX, arrY)
  #plt.plot(arrX,arrY)
  plt.grid()
  plt.show()

###################################
# Correlation
###################################
def cryptoCorrelation(arrX1, arrY1, arrX2, arrY2):
  value = np.corrcoef(arrY1, arrY2)
  print(value[0][1])
  fig, axs = plt.subplots(3, 1, sharex=False)
  axs[0].xcorr(arrY1, arrY2)
  axs[1].plot(arrY1)
  axs[2].plot(arrY2)
  #axs[3].cohere(arrY1, arrY2, 256, 0.1)
  plt.show()

###################################
# Help
###################################
def showHelp():
  print("help")

###################################
# Main
###################################
if len(sys.argv) < 3:
  showHelp()
else:
  # connect to database
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["crypto"]

  if( sys.argv[1] == "fft"):
    x=[]
    y=[]
    fillData(sys.argv[2], x, y)
    if(sys.argv[2][0:4]=="fake"):
      cryptoFFT(x, y)
    else:
      cryptoFFT(x, y)
  elif( sys.argv[1] == "plot"):
    x=[]
    y=[]
    fillData(sys.argv[2], x, y)
    cryptoPlot(x, y)  
  elif( sys.argv[1] == "correl"):
    if len(sys.argv) < 4:
      showHelp()
      exit()
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    fillData(sys.argv[2], x1, y1)
    fillData(sys.argv[3], x2, y2)
    cryptoCorrelation(x1, y1, x2, y2)  





