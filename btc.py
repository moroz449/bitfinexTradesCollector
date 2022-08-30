from time import time,sleep
from json import loads,dumps
import requests
import os


# filesPath="./trades/"
# instrument="tBTCF0:USTF0"

filesPath="./tradesEth/"
instrument="tETHF0:USTF0"

fCnt=0
res=[]
files=os.listdir(filesPath)
if files:
	maxFile=str(max(int(l) for l in files))
	print("max file:",maxFile)
	with open(filesPath+maxFile,"r") as file:
		res=loads(file.read())[-1:]
	fCnt=int(maxFile)+1
startMTS=1608182127943 if not res else res[-1][1]

s=requests.Session()
while True:
	r=s.get("https://api-pub.bitfinex.com/v2/trades/"+instrument+"/hist?sort=1&limit=10000&start="+str(startMTS))
	if r.status_code!=200:
		print("status code not 200")
		print(r.text)
		exit()
	r=loads(r.text)
	i=0
	if res:
		while r[i][0]!=res[-1][0]: i+=1
		i+=1
	print("MTS:", r[-1][1])
	
	res.extend(r[i:])
	if len(r)!=10000: break

	if len(res)>1000000:
		with open(filesPath+str(fCnt),"w") as f: f.write(dumps(res))
		res=[]
		fCnt+=1
	startMTS=r[-1][1]
	sleep(2)

with open(filesPath+str(fCnt),"w") as f: f.write(dumps(res))


