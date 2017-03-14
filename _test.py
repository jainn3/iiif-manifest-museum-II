import downloadData
import urllib
#urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "http://www.gunnerkrigg.com//comics/00000001.jpg")
res = downloadData.sparqlQuery()
print len(res)
listOfres = []
for mus in res:
	for artist in mus:
		listOfres.append(artist["image"]["value"] + '\t' + artist["caption"]["value"])
       
print len(listOfres)
'''

while True:
	try:
		x = int(raw_input("Please enter a number: "))
		break
	except ValueError:
		print "Oops!  That was no valid number.  Try again..."


print  "Can you print?"
'''

try:
  doSomething()
except: 
  pass
print  "Can you print?"
