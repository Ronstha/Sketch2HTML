from flask import Flask,jsonify,request,send_file
from flask_cors import CORS
from predict import predict
import os
import sys
import shutil
os.environ['assets']='../../assets'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from compiler.compiler import compiler
import random
from data import Db
app = Flask(__name__)
CORS(app) 

db=Db()

@app.route('/add_data',methods=['POST'])
def add_data():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        name=str(random.randint(1,10000000000))
        file.save('images/sketch/'+name+'.png')
       
        # data={'success':True,'data': db.create_ui(compiler.parse_dsl(predict('images/sketch'+name+'.png')).tojson())}
        f=open(f'../../outputs/dsl/{random.randint(1,100)}.dsl','r')
        data={'success':True,'data': db.create_ui(compiler.parse_dsl(f.read()).tojson())}
        shutil.move('images/sketch/'+name+'.png','images/sketch/'+str(data['data']['id'])+'.png')
        return jsonify(data),200
    except Exception as e:
        return jsonify({'error': 'Processing Error'}), 400

@app.route('/get_ui',methods=['GET'])
def get_ui():
   return jsonify(db.get_ui()),200
   
@app.route('/get_ui/<int:id>',methods=['GET'])
def getbyid(id):
   res=db.getbyid(id)
   return jsonify(res[0]),res[1]
@app.route('/get_image/<path:img>',methods=['GET'])
def get_image(img):
    try:
        return send_file(f'images/{img}')
    except Exception as e:
        print(e)
        return jsonify({'error':"NOT FOUND"}),400
@app.route('/update_name/<int:id>',methods=['POST'])
def update_name_ui(id):
    res=db.update_ui_name(id,request.json['name'])
    return jsonify(res[0]),res[1]
@app.route('/update_elm/<int:id>',methods=['POST'])
def update_data(id):
    res=db.update_data(id,request.json['name'],request.json['data'])
    return jsonify(res[0]),res[1]

@app.route('/delete_ui/<int:id>',methods=['DELETE'])
def delete_ui(id):
    res=db.delete_ui(id)
    return jsonify(res[0]),res[1]

if __name__=="__main__":
    app.run(debug=False)