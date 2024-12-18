#!/usr/bin/env python

import json
import random
import os
dsl_mapping_path='../assets/dsl_mapping.json'
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
                'primaryColor':'red',
                'secondaryColor':'green'
            }
        if self.name=='text':
            root['text']=get_random_text(random.randint(1,4))
        elif self.name=='paragraph':
            root['text']=". ".join([get_random_text(random.randint(5,10)) for _ in range(random.randint(4,10))])
        elif self.name in ["navlink",'button']:
            root['text']=get_random_text(random.randint(1,3))
            root['href']='#'
        elif self.name=="image":
            root['url']=""
        elif self.name=='table':
            root['data']={}
        elif self.name=="carousel":
            root['images']=[]



        
        for node in self.children:
            root['nodes'].append(node.tojson())        
        return root
class Compiler:

    def __init__(self):
        with open(dsl_mapping_path) as data_file:
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

def get_random_text(n=10):
    paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia."
    words=paragraph.split()
    return " ".join(random.sample(words,n))

def process_dsl_files(dsl_folder,filename, output_folder, dsl_mapping_file_path):
    compiler = Compiler()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
   
    input_path = os.path.join(dsl_folder, filename)
    output_html_path = os.path.join(output_folder, f"{filename[:-4]}.html")

    with open(input_path, 'r') as dsl_file:
        input_dsl = dsl_file.read()
    css_path="./pages.css"
    compiler.compile(input_dsl, output_html_path, css_path)
def dsl_to_json(dsl):
    compiler=Compiler()
    return compiler.parse_dsl(dsl).tojson()

# Example usage
if __name__ == "__main__":
    dsl_mapping_path = "../assets/dsl_mapping.json"
    dsl_folder = "dsl"
    output_folder = "output"
    with open('../Outputs/DSL/1.dsl','r') as f:
        print(dsl_to_json(f.read()))
