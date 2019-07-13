#!/usr/bin/python
import pymongo
import json
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["crypto"]

collist = mydb.list_collection_names()
if "fake_BTC" in collist:
  print("exists")
  mycol = mydb["fake_BTC"]
  cursor = mycol.find()
  count = mycol.count_documents({})
  x=[]
  y=[]
  # fill array
  for i in range(0,count):
    x.append(cursor[i]["_id"])
    y.append(cursor[i]["value"])

  yf = fft(y)
  plt.plot(x,y)
  #while cursor.hasNext():
  #  value = cursor.next()
  #  print(value["value"])
