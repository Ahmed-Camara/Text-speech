from flask import Flask,request,jsonify
import utils
from flask_cors import CORS
import common as c
from waitress import serve
import logging
from logging.handlers import TimedRotatingFileHandler
import os

app = Flask(__name__)
CORS(app)

if not os.path.exists('logs'):
    os.makedirs('logs')
    
log_handler = TimedRotatingFileHandler(
    'logs/app.log',
    when='midnight',
    interval=2,
    backupCount=1
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))

app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

@app.get("/")
def home():
    return jsonify({
        "message":"Welcome to our flask app."
    })
    
@app.get("/convert")
def convertFromTextToAudio():
    
    try:
        textFR = request.json['textFR']
        textEN = request.json['textEN']
        TicketNum = request.json['TicketNum']
        path = request.json['path']
        address = request.json['address']
        pathRacine = request.json["pathRacine"]
        c.address = address
        c.PATH_FOLDER = pathRacine + "/" + path
        
        #c.PATH_FOLDER = "/src/"+path
        app.logger.info("Fonction de la conversion du texte en vocale")
        app.logger.info("textFR : {}".format(textFR))
        app.logger.info("textEN : {}".format(textEN))
        app.logger.info("TicketNum : {}".format(TicketNum))
        app.logger.info("path : {}".format(path))
        app.logger.info("address : {}".format(address))
        app.logger.info("pathRacine : {}".format(pathRacine))
        app.logger.info("c.address : {}".format(c.address))
        app.logger.info("c.PATH_FOLDER : {}".format(c.PATH_FOLDER))
       
        if textFR is None or len(textFR) == 0:
            c.dataENURL,c.dataEN = utils.generateAudio(textEN,'en',TicketNum,path)
            c.dataFRURL = c.dataFR = ""
        
        elif textEN is None or len(textEN) == 0:
            c.dataFRURL,c.dataFR = utils.generateAudio(textFR,'fr',TicketNum,path)
            c.dataENURL = c.dataEN = ""
            

        elif textFR is not None and textEN is not None and TicketNum is not None:
            c.dataFRURL,c.dataFR = utils.generateAudio(textFR,'fr',TicketNum,path)
            c.dataENURL,c.dataEN = utils.generateAudio(textEN,'en',TicketNum,path)

    except Exception as e:
        c.status = "0"
        c.ERROR_MSG = "Une erreur s'est produite, veuillez contacter l'administrateur! \n"
        app.logger.error(c.ERROR_MSG+ str(e))
        return jsonify({
            
            "status":c.status,
            "message":c.ERROR_MSG+ str(e)
        })
    
    app.logger.info("Succès de la conversion du texte en voie")
    return jsonify({
        "data_french":c.dataFR,
        "data_english":c.dataEN,
        "data_french_url":c.dataFRURL,
        "data_english_url":c.dataENURL
    })

@app.get("/process_files")
def getBase64Files():
    try:
        
        data = request.get_json()
        if "files" not in data:
            raise("erreur sur le formattage du json")
        
        filePaths = data["files"]
        path = data["path"]
        app.logger.info("filePaths : {}".format(filePaths))
        app.logger.info("path : {}".format(path))
        
        utils.handleRepository(path)
        
        result = []
        for filePath in filePaths:
            base64Data = utils.getBase64Files(filePath,path)
            compressed_base64_data = utils.compress_base64_data(base64Data)
            #result.append(base64Data)
            result.append(compressed_base64_data)
    except Exception as e:
        c.status = "0"
        c.ERROR_MSG = "Une erreur s'est produite, veuillez contacter l'administrateur :\n"
        app.logger.error(c.ERROR_MSG+ str(e))
        return jsonify({
            "status":c.status,
            "message":c.ERROR_MSG+ str(e)
        })
    app.logger.info("Succès de la conversion du fichier en base64")   
    return jsonify({
        "status":"1",
        "base_64_data":result
    })

if __name__ == "__main__":
    serve(app,host=c.host,port=c.port,threads=1)
