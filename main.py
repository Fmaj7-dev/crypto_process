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
    if(curveName == "fake_BTC"):
      value = cursor[i]["_id"]
    else:
      value = (cursor[i]["_id"]-originOfTime)/(2*15*60*1000)
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

  cap = kwargs.get('cap', None)
  if(cap is None):
    plt.plot(xf, np.abs(yf[0:count//2] /count))
  else:
    plt.plot(xf, np.clip(np.abs(yf[0:count//2] /count), 0, cap))
  #plt.plot(arrX,arrY)
  plt.grid()
  plt.show()

###################################
# Correlation
###################################
def cryptoCorrelation(curveNameA, curveNameB):
  print ("correl "+curveNameA + " "+curveNameB)

###################################
# Help
###################################
def showHelp():
  print("help")

if len(sys.argv) < 3:
  showHelp()
  collection = sys.argv[1]
else:
  # connect to database
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["crypto"]

  if( sys.argv[1] == "fft"):
    x=[]
    y=[]
    fillData(sys.argv[2], x, y)
    cryptoFFT(x, y)
  if( sys.argv[1] == "correl"):
    if len(sys.argv) < 4:
      showHelp()
      exit()
    cryptoCorrelation(sys.argv[2], sys.argv[3])  

exit()





