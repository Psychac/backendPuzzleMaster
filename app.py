from flask import Flask, request, url_for, jsonify
from werkzeug.utils import secure_filename
#from rubikscubetracker import  RubiksImage
from rbt import RubiksImage
import json
import helpers
import os
import ast

app = Flask(__name__,static_url_path = "/static")
UPLOAD_FOLDER ='static/uploads/'
DOWNLOAD_FOLDER = 'static/downloads/'
#ALLOWED_EXTENSIONS = {‘jpg’, ‘png’,’.jpeg’}

# APP CONFIGURATIONS
app.config['SECRET_KEY'] = 'PuzzleMaster'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size to 2mb
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 


prominent_color_palette = {
    'Red'   : [185, 0, 0],
    'Orange': [255, 89, 0],
    'Blue'  : [0, 69, 173],
    'Green' : [0, 155, 72],
    'White' : [255, 255, 255],
    'Yellow': [255, 213, 0]
}
calibrated_colors = {}
colors_per_square = {}
notations = {}
cubestring = {}


@app.route('/', methods=['GET','POST'])
def function():
  return jsonify({"msg" : True})

@app.route('/calibratePallete', methods=['GET','POST'])
def setPallete():

   data = request.form.to_dict()

   colors = ast.literal_eval(data['colors'])
   for key,value in colors.items():
     calibrated_colors[key] = value
   #print(calibrated_colors)

  #  sidenotation = ast.literal_eval(data['side'])
  #  for key,value in sidenotation.items():
  #    notations[str(value)] = str(key)
  #print(notations)
   #print(data)
   
   return jsonify({"status": True,"msg":"Colors Calibrated Successfully"})
   #return jsonify({"status": False,"msg":"Color Calibration Failed"})

@app.route('/calibrate',methods=["POST"])
def calibrate():
  file = request.files['image']
  filename = secure_filename(file.filename)
  file.save(os.path.join(UPLOAD_FOLDER, filename))
  #file.save(file.filename)
  payload = request.form.to_dict()
  color = payload['color']
  side = payload['side']
  try:
    rimg = RubiksImage()
    rimg.analyze_file(os.path.join(UPLOAD_FOLDER,filename))
    #print(rimg.data.items())
    middle_square_color = rimg.data[5]
    calibrated_colors[color] = middle_square_color
    notations[color] = side
    return jsonify({'msg':"%s color has been calibrated successfully"%color})
    #return jsonify({'msg':'success, %s has been calibrated'%coloor,'result':json.dumps(calibrated_colors),'notation':json.dumps(notations)})
  except:
    return jsonify({"status":False,"message":"unable to detect colors, try again..."})


@app.route('/colors',methods=["POST"])
def notation():
  file = request.files['image']
  filename = secure_filename(file.filename)
  file.save(os.path.join(UPLOAD_FOLDER, filename))
  #file.save(file.filename)
  payload = request.form.to_dict()
  side = payload['side']

  try:
    rimg = RubiksImage()
    rimg.analyze_file(os.path.join(UPLOAD_FOLDER,filename))
    #rimg.analyze_file(file.filename)
    colors_for_side = {}
    sidenot = ""
    color_rgb = []
    color_short = ""

    if calibrated_colors:
        color_pallete = calibrated_colors
    else:
        color_pallete = prominent_color_palette

    middle_square_color = rimg.data[5]
    color = helpers.get_closest_color(middle_square_color,color_pallete)['color_name']
    #print(color)
    notations[color] = side[0]

    for key,value in rimg.data.items():
      color_name = helpers.get_closest_color(value,color_pallete)
      colors_for_side[key] = color_name['color_name']
      #sidenot = sidenot + notations[color_name['color_name']]
      color_rgb.append(value)
      color_short += color_name['color_name'][0]

    colors_per_square[side] = colors_for_side
    #cubestring[side] = sidenot
    print(color_short)
    print(color_rgb)
    print(notations)
    #print(cubestring)
    #return jsonify({'status':True,'side':side,"color_rgb":color_rgb,'result':json.dumps(colors_for_side)})
    return jsonify({'status':True,"color_rgb":color_rgb,"color_name":color_short})

  except:
    return jsonify({"status":False,"message":"unable to detect colors, try again..."})


@app.route('/result', methods=['GET','POST'])
def solve():
    print(notations)
    
    for sidename in ("Up","Right","Front","Down","Left","Back"):
      colors_per_side = colors_per_square[sidename]
      #print(colors_per_side)
      sidenot = ""
      for key,value in colors_per_square[sidename].items():
        sidenot = sidenot + notations[value]
      cubestring[sidename] = sidenot
      #print(sidenot)        
      #print(colors_per_side)
    
    resultstring = ""

    for sidename in ("Up","Right","Front","Down","Left","Back"):
        resultstring += cubestring[sidename]

    return jsonify({"status":True,'result': resultstring})

@app.route('/resetapp', methods=['GET','POST'])
def reset_app():

   calibrated_colors.clear()
   notations.clear()
   cubestring.clear()
   colors_per_square.clear()

   return jsonify({'msg':'Reset Successful'})


if __name__ == '__main__':
  #app.run(host='127.0.0.1', port=8000, debug=True)
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
 
