from DatasetGenerator.DSLGenerator.GenerateDSL import gen 
from compiler.compiler import process_dsl_files
from DatasetGenerator.SketchGenerator.webdriver import WebDriver
import os
from DatasetGenerator.SketchGenerator.generate import generate_sketch
import shutil
import time
clean=False
DSL_dir='Outputs/DSL'
HTML_dir='Outputs/HTML'
SS_dir='Outputs/Screenshot'
Sketch_dir='Outputs/Sketch'
Sketch_path='Assets/sketch'
dsl_mapping_file_path = "assets/dsl_mapping.json"

for dir in [DSL_dir,HTML_dir,SS_dir,Sketch_dir]:
    if clean:
        try:
            shutil.rmtree(dir)
        except:
            pass
    os.makedirs(dir,exist_ok=True)
        
start=time.time()
webdriver=WebDriver(w=1200+16,h=1700+95)
for n in range(int(input("No of sketch="))):
    # if(time.time()-start>60*60*2.5):
    #     break
    t=str(time.time()).replace('.','')
    
    t=str(n)
    dsl=gen()
    with open(f'{DSL_dir}/{t}.dsl','w') as f:
        f.write(dsl)
    process_dsl_files(DSL_dir, t+'.dsl',HTML_dir, dsl_mapping_file_path)
    webdriver.saveScreenshot(HTML_dir,t+'.html',SS_dir)
    generate_sketch(os.path.join(SS_dir,t+'.png'),Sketch_path,os.path.join(Sketch_dir,t+'.png'))
    print(f"{n} Sketch Generated {t}")
webdriver.quit()
