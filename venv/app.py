from flask import Flask, jsonify, render_template, request, send_from_directory, send_file
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb+srv://flight-time-logger-app:csci6710team5@anthony-test-tfdgg.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client["production"]
col = db["production"]


@app.route("/")
@app.route("/index")
@app.route("/all-flights")
def all_flights():
    docs = col.find()
    flights = list(docs)
    return render_template("index.html", flights=flights)

@app.route("/departures")
def departures():
    docs = col.find()
    departures = list(docs)
    return render_template("departures.html", departures=departures)    

@app.route("/arrivals")
def arrivals():
    docs = col.find()
    arrivals = list(docs)
    return render_template("arrivals.html", arrivals=arrivals) 

@app.route("/addFlight")
def addFlight():
    return render_template("addFlight.html")

@app.route("/reports")
def reports():
    cwd = os.getcwd()
    reportPath = os.path.join(cwd,"reports")
    listOfFiles = os.listdir(reportPath)
    reprotId = 1
    reportsList = []
    for eachFile in listOfFiles:
        currentReportPath = os.path.join(reportPath,eachFile)
        currentFile = open(currentReportPath,'r')
        currentReport={'reportName':eachFile,'reportFormat':'json','reportId':reprotId}
        reprotId+=1
        for eachLine in currentFile:
            currentReport['reportDescrip'] = eachLine
            break
        reportsList.append(currentReport)
    return render_template("reports.html",reportsList=reportsList)

@app.route("/ourTeam")
def ourTeam():
    return render_template("ourTeam.html")

@app.route("/ourMotivation")
def ourMotivation():
    return render_template("ourMotivation.html")

@app.route("/deleteFlight")
def deleteFlight():
    id_to_delete = request.args.get("id", "0", type=str)
    query = { "id" : id_to_delete }
    col.delete_one(query)
    return render_template("index.html")

@app.route("/addFlightLogic")
def addFlightLogic():
    # Insert the document
    id = request.args.get("id", "failed", type=str)
    aircraft_type = request.args.get("aircraft_type", "failed", type=str)
    aircraft_tail_num = request.args.get("aircraft_tail_num", "failed", type=str)
    departure_date = request.args.get("departure_date", "failed", type=str)
    departure_location = request.args.get("departure_location", "failed", type=str)
    departure_airport_code = request.args.get("departure_airport_code", "failed", type=str)
    departure_time_local = request.args.get("departure_time_local", "failed", type=str)
    departure_time_zulu = request.args.get("departure_time_zulu", "failed", type=str)
    arrival_date = request.args.get("arrival_date", "failed", type=str)
    arrival_location = request.args.get("arrival_location", "failed", type=str)
    arrival_airport_code = request.args.get("arrival_airport_code", "failed", type=str)
    arrival_time_local = request.args.get("arrival_time_local", "failed", type=str)
    arrival_time_zulu = request.args.get("arrival_time_zulu", "failed", type=str)
    flight_time = request.args.get("flight_time", 0, type=int)
    cargo_num_of_items = request.args.get("cargo_num_of_items", 0, type=int)
    cargo_weight_lbs = request.args.get("cargo_weight_lbs", 0, type=int)
    cargo_weight_kg = request.args.get("cargo_weight_kg", 0, type=int)
    cargo_loading_agents = request.args.get("cargo_loading_agents", "failed", type=str)
    cargo_description = request.args.get("cargo_description", "failed", type=str)
    mydict = ({"id":id, "aircraft_type":aircraft_type, "aircraft_tail_num":aircraft_tail_num, "departure_date":departure_date,
        "departure_location":departure_location, "departure_airport_code":departure_airport_code, "departure_time_local":departure_time_local,
        "departure_time_zulu":departure_time_zulu, "arrival_date":arrival_date, "arrival_location":arrival_location,"arrival_airport_code":arrival_airport_code,
        "arrival_time_local": arrival_time_local, "arrival_time_zulu":arrival_time_zulu, "flight_time":flight_time, "cargo_num_of_items":cargo_num_of_items, 
        "cargo_weight_lbs": cargo_weight_lbs, "cargo_weight_kg": cargo_weight_kg, "cargo_loading_agents":cargo_loading_agents,
        "cargo_description": cargo_description})
    x = col.insert_one(mydict)

    # Check if the document was inserted properly by querying the id string
    rcd = col.find_one({ "id" : id })
    if rcd["id"] == id:
        return {"flight_added":"1"}
    else:
        return {"flight_added":"0"}

@app.route("/searchAircraftInfo")
def searchAircraftInfo():
    print("Searching Aircraft Info")
    aircraft_type = request.args.get("aircraft_type", "failed", type=str)
    aircraft_tail_num = request.args.get("aircraft_tail_num", "failed", type=str)
    queryList = [aircraft_type,aircraft_tail_num]
    columnNames = ["aircraft_type","aircraft_tail_num"]
    queryDict = {}
    for eachIndex in range(2):
        userQuery = queryList[eachIndex].strip()
        if not userQuery =="": 
            queryDict[columnNames[eachIndex]] =userQuery
    result = col.find(queryDict)
    resultList = list(result)
    # Check if there is any result if so, write down the report
    if len(resultList) > 0:
        cwd = os.getcwd()
        nowTime = datetime.now()
        dt_string = nowTime.strftime("%d-%m-%Y-%H-%M-%S")
        fileName = dt_string+".json"
        reportPath = os.path.join(cwd,"reports",fileName)
        report = open(reportPath,"w")
        report.write("User Query:"+str(queryDict)+"\n")
        for eachJson in resultList:
            report.write(str(eachJson))
            report.write("\n")
        report.close()
        return {"searchResult":str(len(resultList)),"fileName":fileName}
    else:
        return {"searchResult":"0"}

@app.route("/searchFlightInfo")
def searchFlightInfo():
    print("Searching Flight Info")
    departure_date = request.args.get("departure_date", "failed", type=str)
    departure_location = request.args.get("departure_location", "failed", type=str)
    departure_airport_code = request.args.get("departure_airport_code", "failed", type=str)
    departure_time_local = request.args.get("departure_time_local", "failed", type=str)
    departure_time_zulu = request.args.get("departure_time_zulu", "failed", type=str)
    arrival_date = request.args.get("arrival_date", "failed", type=str)
    arrival_location = request.args.get("arrival_location", "failed", type=str)
    arrival_airport_code = request.args.get("arrival_airport_code", "failed", type=str)
    arrival_time_local = request.args.get("arrival_time_local", "failed", type=str)
    arrival_time_zulu = request.args.get("arrival_time_zulu", "failed", type=str)
    flight_time = request.args.get("flight_time", 0, type=int)
    queryList = [departure_date,departure_location,departure_airport_code,departure_time_local,departure_time_zulu,arrival_date,arrival_location,arrival_airport_code,arrival_time_local,arrival_time_zulu,flight_time]
    columnNames = ['departure_date','departure_location','departure_airport_code','departure_time_local','departure_time_zulu','arrival_date','arrival_location','arrival_airport_code','arrival_time_local','arrival_time_zulu','flight_time']
    queryDict = {}
    for eachIndex in range(11):
        if not columnNames[eachIndex] == "flight_time":
           userQuery = queryList[eachIndex].strip()
           if not userQuery =="":
                queryDict[columnNames[eachIndex]] = userQuery
        else:
            if not queryList[eachIndex] == 0:
                queryDict[columnNames[eachIndex]] = queryList[eachIndex]
    result = col.find(queryDict)
    resultList = list(result)
    # Check if there is any result if so, write down the report
    if len(resultList) > 0:
        cwd = os.getcwd()
        nowTime = datetime.now()
        dt_string = nowTime.strftime("%d-%m-%Y-%H-%M-%S")
        fileName = dt_string+".json"
        reportPath = os.path.join(cwd,"reports",fileName)
        report = open(reportPath,"w")
        report.write("User Query:"+str(queryDict)+"\n")
        for eachJson in resultList:
            report.write(str(eachJson))
            report.write("\n")
        report.close()
        return {"searchResult":str(len(resultList)),"fileName":fileName}
    else:
        return {"searchResult":"0"}

@app.route("/searchCargoInfo")
def searchCargoInfo():
    print("Searching Cargo Info")
    cargo_num_of_items = request.args.get("cargo_num_of_items", "", type=int)
    cargo_weight_lbs = request.args.get("cargo_weight_lbs", "", type=int)
    cargo_weight_kg = request.args.get("cargo_weight_kg", "", type=int)
    cargo_loading_agents = request.args.get("cargo_loading_agents", "failed", type=str)
    cargo_description = request.args.get("cargo_description", "failed", type=str)
    queryList = [cargo_num_of_items,cargo_weight_lbs,cargo_weight_kg,cargo_loading_agents,cargo_description]
    columnNames = ['cargo_num_of_items','cargo_weight_lbs','cargo_weight_kg','cargo_loading_agents','cargo_description']
    queryDict = {}
    for eachIndex in range(5):
        if columnNames[eachIndex] == "cargo_loading_agents" or columnNames[eachIndex] == "cargo_description":
            userQuery = queryList[eachIndex].strip()
            if not userQuery == "":
                queryDict[columnNames[eachIndex]] = userQuery
        else:
            if not queryList[eachIndex] == "":
                queryDict[columnNames[eachIndex]] = queryList[eachIndex]
        
    result = col.find(queryDict)
    resultList = list(result)
    # Check if there is any result if so, write down the report
    if len(resultList) > 0:
        cwd = os.getcwd()
        nowTime = datetime.now()
        dt_string = nowTime.strftime("%d-%m-%Y-%H-%M-%S")
        fileName = dt_string+".json"
        reportPath = os.path.join(cwd,"reports",fileName)
        report = open(reportPath,"w")
        report.write("User Query:"+str(queryDict)+"\n")
        for eachJson in resultList:
            report.write(str(eachJson))
            report.write("\n")
        report.close()
        return {"searchResult":str(len(resultList)),"fileName":fileName}
    else:
        return {"searchResult":"0"}

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    cwd = os.getcwd()
    reports = os.path.join(cwd,"reports")
    return send_from_directory(directory=reports, filename=filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/editFlight")
def editFlight():
    id = request.args.get("id", "failed", type=str)
    field = request.args.get("field", "failed", type=str)
    newData = request.args.get("newData", "failed", type=str)
    myQuery = {"id":id}
    myData = {"$set": {field:newData}}
    col.update_one(myQuery, myData)

    # Check if record properly updated and return 1 if so
    check = col.find_one(myQuery)
    if check[field] == newData:
        return {"updated":"1"}
    else:
        return {"updated":"0"}
