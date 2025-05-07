from flask import Flask,jsonify,request,send_file
from flask_cors import CORS
from predict import predict
import os
import sys
import time
import shutil
import zipfile
os.environ['assets']='../../assets'
os.environ['url']='http://localhost:5000/get_image/'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from compiler.compiler import Compiler,JSONCompiler
import random
from data import Db
app = Flask(__name__)
CORS(app) 

db=Db()
compiler=Compiler()
jsoncompiler=JSONCompiler()
jsoncompiler2=JSONCompiler(False)
def zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
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
       
        data={'success':True,'data': db.create_ui(compiler.parse_dsl(predict('images/sketch/'+name+'.png')).tojson())}
        # f=open(f'../1.dsl','r')
        # data={'success':True,'data': db.create_ui(compiler.parse_dsl(f.read()).tojson())}
        shutil.move('images/sketch/'+name+'.png','images/sketch/'+str(data['data']['id'])+'.png')
        return jsonify(data),200
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': 'Processing Error'}), 400

@app.route('/add_image/<int:method>',methods=['POST'])
def add_image(method):
    
    if method==0:
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        name=file.filename.split('.')
        name=name[0]+'-'+str(time.time())+"."+name[1]
        file.save('images/images/'+name)
        url='images/'+name
    else:
        url=request.json['url']
    res=db.add_image(url)       
    return jsonify(res[0]),res[1]
@app.route('/remove_image/<int:id>',methods=['DELETE'])
def remove_image(id):
    res=db.remove_image(id)
    return jsonify(res[0]),res[1]
@app.route('/save_file/<int:id>',methods=['GET'])
def save_file(id):
    res=db.getbyid(id)
    compiled=jsoncompiler2.compile(res[0]['node'])
    try:
        os.removedirs('output')
    except:
        pass
    os.makedirs('output/images',exist_ok=True)
    for img in jsoncompiler2.images:
        shutil.copy(f'images/{img}',f'output/{img}')
    with open('output/index.html','w',encoding='utf-8') as f:
        f.write(compiled)
    zip_folder('output','output.zip')
    
    return send_file('output.zip')

@app.route('/get_imagelist',methods=["GET"])
def get_list():
    res=db.get_images()
    return jsonify(res[0]),res[1]


@app.route('/get_ui',methods=['GET'])
def get_ui():
   return jsonify(db.get_ui()),200
   
@app.route('/get_ui/<int:id>',methods=['GET'])
def getbyid(id):
   res=db.getbyid(id)
   try:
    res[0].update({'html':jsoncompiler.compile(res[0]['node'])})
   except:
       pass
   return jsonify(res[0]),res[1]
@app.route('/get_image/<path:img>',methods=['GET'])
def get_image(img):
    try:
        return send_file(f'images/{img}')
    except Exception as e:
        return jsonify({'error':"NOT FOUND"}),400
@app.route('/update_name/<int:id>',methods=['POST'])
def update_name_ui(id):
    res=db.update_ui_name(id,request.json['name'])
    return jsonify(res[0]),res[1]
@app.route('/update_elm/<int:id>',methods=['POST'])
def update_data(id):
    try:
        res=db.update_data(id,request.json['name'],request.json['data'])
        return jsonify(res[0]),res[1]
    except:
        pass

@app.route('/delete_ui/<int:id>',methods=['DELETE'])
def delete_ui(id):
    res=db.delete_ui(id)
    return jsonify(res[0]),res[1]

if __name__=="__main__":
    app.run(debug=False)