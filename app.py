import time
from BBWebFw import webApp
from BBWebFw.FileRenderer import Template
import os
import random
import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('hthshacks.json')
config = {
	"apiKey": "AIzaSyBaN3_U2CM-FcaP9mm_CUJ6_qjMj7PVkKA",
	"authDomain": "hthshacks-2021.firebaseapp.com",
	"databaseURL": "https://hthshacks-2021-default-rtdb.firebaseio.com/",
	"storageBucket": "hthshacks-2021.appspot.com"
}
fb = firebase_admin.initialize_app(cred_obj,config)

app = webApp("app", "gunicorn", os.path.dirname(os.path.abspath(__file__)))
app.staticCache = 60 * 60 * 24 * 365

template = Template()

@app.catchURL("/")
def root(req,res):
	res.text = template("index.html")

@app.catchURL("/get")
def getHelp(req,res):
	res.text = template("get.html")

@app.catchURL("/raise")
def getHelp(req,res):
	res.text = template("raise.html")

@app.catchURL("/startfund")
def startf(req,res):
	res.text = template("success.html", {"alert": "Your CrowdFunding Was Started"})
	ref = db.reference('/fundraisers').push({"Name": req.POST["Name"],
											 "Disease": req.POST["Disease"],
											 "Severity": req.POST["Disease"],
											 "FundingTarget": req.POST["FundingTarget"],
											 "FundingDone": 0
											 })

@app.catchURL("/sheduleappointment")
def giveHelp(req,res):
	print(req.POST)
	if 'emergency' in req.POST:
		res.text = template("success.html", {"alert": "Your Appointment Request Was Registered. Our Doctors Will Reach Out Within An Hour."})
		ref = db.reference('/appointments-emergency')
	elif not 'emergency' in req.POST:
		res.text = template("success.html", {"alert": "Your Appointment Request Was Registered. Our Doctors Will Reach Out In A Few Hours."})
		ref = db.reference('/appointments/')

	ref.push({"Name": req.POST["Name"],
			  "Phone Number": req.POST["PPhNum"],
			  "Patient's Name": req.POST["PName"],
			  "Patient's DOB": req.POST["PDOB"],
			  "Symptoms": req.POST["symp"]})

@app.catchURL("/give")
def giveHelp(req,res):		
	res.text = template("give.html", {"raisers": db.reference('/fundraisers').get()})