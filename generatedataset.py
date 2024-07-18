from DatasetGenerator.DSLGenerator.GenerateDSL import gen 
from compiler.compiler import process_dsl_files
from DatasetGenerator.SketchGenerator.webdriver import WebDriver
import os
from DatasetGenerator.SketchGenerator.generate import generate_sketch
import shutil
clean=True
DSL_dir='Outputs/DSL'
HTML_dir='Outputs/HTML'
SS_dir='Outputs/Screenshot'
Sketch_dir='Outputs/Sketch'
Sketch_path='Assets/sketch'
for dir in [DSL_dir,HTML_dir,SS_dir,Sketch_dir]:
    if clean:
        try:
            shutil.rmtree(dir)
        except:
            pass
    os.makedirs(dir,exist_ok=True)
        

for n in range(int(input("No of sketch="))):
    dsl=gen()
    with open(f'{DSL_dir}/{n+1}.dsl','w') as f:
        f.write(dsl)
dsl_mapping_file_path = "assets/dsl_mapping.json"

process_dsl_files(DSL_dir, HTML_dir, dsl_mapping_file_path)
webdriver=WebDriver(w=1200,h=2200)
for file in os.listdir(HTML_dir):
    if(not file.endswith('.html')): continue
    webdriver.saveScreenshot(HTML_dir,file,SS_dir)
webdriver.quit()
for file in os.listdir(SS_dir):
    generate_sketch(os.path.join(SS_dir,file),Sketch_path,os.path.join(Sketch_dir,file))