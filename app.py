from flask import Flask, request, send_file
from dotenv import load_dotenv
import mimetypes
import requests
import json
import soundfile as sf
import ffmpeg
from ffmpy import FFmpeg
import os

app = Flask(__name__)

@app.get("/home")
def hello():
    return{
        "message" : "running correct"
    }

@app.post("/convert/<type>")
def convert():   
   # 
   if 'Content_Type' not in request.headers:
      return {
         'message' : 'Content-Type must be provided',
         'status':'203'
        }
   else:
      h= request.headers['Content_Type']
      
      if(h!="application/json"):
         return{
            'message' : "Invalid type"
         }
      else:
         data = request.json
         url = data.get('audiourl')
         user = data.get('user_identifier')
         signedurl = data.get('signedUrl')
         auth = data.get('auth')
         file_name = user
         response = requests.get(url)
         
         if(response.status_code==200):
            content_type = response.headers.get('content-type')
            extension = mimetypes.guess_extension(content_type)
            if extension is None:
               extension = ".wav"
            file_name+= extension
            with open(file_name,'wb')as file:
               file.write(response.content)
            
           
            header = {"Authorization": auth}
            data = {'grant_type':'client_credentials',
            'scope':'sonde-platform/users.write sonde-platform/voice-feature-scores.write sonde-platform/voice-feature-scores.read sonde-platform/storage.write'
            }

            resp = requests.post(url='https://api.sondeservices.com/platform/v1/oauth2/token',
                    headers= header,data=data)

            r = resp.json()
            access_token=str(r['access_token'])
         

            # file conversion
            wave_file = user+".wav"

            ff = FFmpeg(inputs={file_name:None},outputs={wave_file:None})
            ff.run()
                        
           

           

            header = {'Content-Type': 'audio/wave'}
           
            with open(r'C:\Users\GS-3930\Desktop\flask-to-convert\{}'.format(wave_file),'rb') as audio_file:
             resp = requests.put(url=signedurl,                   
                      headers=header,data=audio_file)
             if(resp.status_code==200): 
                return{
                   "Message" : "File Uploaded"
                }
             else:
                return{
                "Message" : "Error while uploading"
             }
                
                # final score
                
                                
         else:
                return {
                   "Message" : "Error while uploading you data"
                }

@app.get("/delfile/<value>")
def delete_file(value):
  oga=value+".oga"
  wav=value+".wav"
#   ogafilepath = r"C:\Users\GS-3930\Desktop\flask-to-convert\{}".format(oga)
#   wavfilepath = r"C:\Users\GS-3930\Desktop\flask-to-convert\{}".format(wav)
   
  if(os.path.exists(oga)):
      os.remove(oga)
      os.remove(wav)
      return{
         "Message" : "File Deleted"
      }
  else:
     return{
        "Message" : "File Not found"
     }

              
            
            
         
       
   

          
       


