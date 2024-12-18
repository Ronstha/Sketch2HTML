#!/usr/bin/env python

import json
import random
import os
try:
    image_files = [f for f in os.listdir('../assets/images') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
except Exception as e:
    print(f"Error fetching images: {e}")
    image_files = ["placeholder.jpg"]
class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.attributes = {}

    def add_child(self, child):
        self.children.append(child)

    def set_attribute(self, key, value):
        self.attributes[key] = value

    def render(self, dsl_mapping):
        element_mapping = dsl_mapping.get(self.name, "")
        
        # Return a default representation if no mapping exists
        if not element_mapping:
            return f"<{self.name}></{self.name}>"
            # return f"<{self.name}>{self.content}</{self.name}>"

        # Replace attributes in the mapping
        result = element_mapping
        for key, value in self.attributes.items():
            result = result.replace(f"${key}", value)

        # Render child nodes
        child_content = "".join(child.render(dsl_mapping) for child in self.children)
        result = result.replace("{}", child_content)

    
        return result
    def tojson(self):
        root={
            'name':'',
            'element':self.name,
            'nodes':[]
        }
        if self.name=='root':
            root['styles']={
              'primary-color': '#6a11cd',
        'secondary-color': '#2ecc71',
        'accent-color': '#e74c3c',
        'primary-text-color': 'white',
        'secondary-text-color': '#2c3e50',
        'background-color': '#ecf0f1',
                'accent-text-color':'black',
                'color':'white',
                'font-family':'Times New Roman',
                'font-size-lg':'20px',
                'font-size-md':'16px',
                'font-size-sm':'13px',
                 'spacing-sm':'1rem',
                 'spacing-md':'1.5rem',
                 'spacing-lg':'2rem',
                 'border-radius-sm':'4px',
                  'border-radius-md': '8px',
        'border-radius-lg': '12px'
            }
        if self.name.startswith('text'):
            root['text']=get_random_text(random.randint(1,3))
        elif self.name=='paragraph':
            root['text']=". ".join([get_random_text(random.randint(5,10)) for _ in range(random.randint(4,10))])
        elif self.name=='navlink':
            root['text']=get_random_text(random.randint(1,2))
            root['href']='#'
        elif self.name.startswith('button'):
            root['text']=get_random_text(random.randint(1,2))
        elif self.name=="image":
            root['url']=random.choice(image_files)
        elif self.name=='table':
            root['data']={}
        elif self.name=="carousel":
            root['images']=random.sample(image_files,3)



        
        for node in self.children:
            root['nodes'].append(node.tojson())        
        return root
class Compiler:

    def __init__(self,):
        with open(os.environ['assets']+'/dsl_mapping.json') as data_file:
            self.dsl_mapping = json.load(data_file)

    def compile(self, input_dsl, output_html_path, output_css_path):
        try:
            root = self.parse_dsl(input_dsl)
            html_content = root.render(self.dsl_mapping)
            html_content+="<script src='./../../assets/script.js'></script>"
            html_content=html_content.replace('<img src=\"placeholder.jpg\"  class=\"image\">','<div class=\'image\'></div>')

            full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Page</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="../../assets/page.css">
    
</head>
<body>
{html_content}
</body>
</html>
            """
            
            with open(output_html_path, 'w') as output_file:
                output_file.write(full_html)

            print(f"Successfully compiled: {output_html_path}")
        except Exception as e:
            print(f"Error compiling {output_html_path}: {str(e)}")
    
    def parse_dsl(self, input_dsl):
        lines = input_dsl.split('\n')
        root = Node("root")
        stack = [root]
        
        for line_number, line in enumerate(lines, 1): 
            if not line.strip():
                continue

            try:
                indent = len(line) - len(line.lstrip())
                line = line.strip()
            
                # Adjust the stack to match the current indentation level
                while indent < len(stack) - 2:
                    stack.pop()

                if line.endswith('{'):
                    # New node with children
                    name = line[:-1].strip()
                    node = Node(name, stack[-1])
                    stack[-1].add_child(node)
                    stack.append(node)
                elif line == '}':
                    # End of current node
                    if len(stack) > 1:
                        stack.pop()
                else:
                    # Leaf node
                    node = Node(line, stack[-1])
                    stack[-1].add_child(node)

            except Exception as e:
                print(f"Error parsing line {line_number}: {line}")
                print(f"Error details: {str(e)}")

        return root
class JSONCompiler:
    def __init__(self):
        with open(os.environ['assets']+"/dsl_mapping.json") as data_file:
            self.dsl_mapping = json.load(data_file)
    def compile(self,obj):
        html_content=self.render(obj)
        css_content=self.generate_css(obj['styles'])
        with open(os.environ['assets']+"/temp.html",'r') as f:
           return f.read().format(css_content=css_content,html_content=html_content)
    def render(self,obj):
        elm=obj['element']
        if elm=='carousel':
           

            images = obj['images']
        
            # Carousel HTML template
            carousel_html = """
            <div class="carousel-container">
                <div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
                    <div class="carousel-inner">
                        {slides}
                    </div>
                    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Next</span>
                    </button>
                </div>
            </div>
            """

            
            slides = ""
            for i, img in enumerate(images):
                active_class = "active" if i == 0 else ""
                img_path = os.path.join('../assets/images', img)
                slides += f"""
                <div class="carousel-item {active_class}">
                    <img src="{img_path}" class="d-block w-100" alt="Carousel Image {i+1}">
                </div>
                """

            # Replace placeholder with slides
            return carousel_html.format(slides=slides)
        elif elm.startswith('text') or elm.startswith('button') or elm=='paragraph':
            return self.dsl_mapping[elm].format(
                obj['text']
            )
        elif elm=='navlink':
            return self.dsl_mapping[elm].format(
                obj['text'],obj['href']
            )
        elif elm=='image':
              return self.dsl_mapping[elm].format(
                os.path.join('../assets/images', obj['url'])
            )

        children_html = ''.join(self.render(child) for child in obj['nodes'])
        return self.dsl_mapping[elm].format(children_html)
    def generate_css(self,styles):
        
        css_vars = "\n".join([f"    --{key}: {value};" for key, value in styles.items()])
        with open(os.environ['assets']+'/temp.css','r') as f:
            css=f.read()
            css=css.replace('[CSS_VAR]',css_vars)
            return css
    

def get_random_text(n=10):
    paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia."
    words=paragraph.split()
    return " ".join(random.sample(words,n))

def process_dsl_files(dsl_folder,filename, output_folder, dsl_mapping_file_path):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
   
    input_path = os.path.join(dsl_folder, filename)
    output_html_path = os.path.join(output_folder, f"{filename[:-4]}.html")

    with open(input_path, 'r') as dsl_file:
        input_dsl = dsl_file.read()
    css_path="./pages.css"
    compiler.compile(input_dsl, output_html_path, css_path)
 

# Example usage
if __name__ == "__main__":
    os.environ['assets']='../assets'
    compiler=Compiler()
    jsoncompiler=JSONCompiler()
    dsl_folder = "dsl"
    output_folder = "output"
    with open('../Outputs/DSL/30.dsl','r') as f:
            

        with open('test.html','w') as f1:
            f1.write(jsoncompiler.compile(compiler.parse_dsl(f.read()).tojson()))
