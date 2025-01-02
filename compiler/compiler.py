#!/usr/bin/env python

import json
import random
import os

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

        # Handle nodes that might have content replacement
        if self.name in ['text', 'paragraph']:
            result = result.replace('[]', generate_random_text())
    

        return result
    
class Compiler:
    def __init__(self, dsl_mapping_file_path):
        with open(dsl_mapping_file_path) as data_file:
            self.dsl_mapping = json.load(data_file)

    def compile(self, input_dsl, output_html_path, output_css_path):
        try:
            root = self.parse_dsl(input_dsl)
            html_content = root.render(self.dsl_mapping)
            html_content+="<script src='./../../assets/script.js'></script>"
            html_content=html_content.replace('src=""','src="./../../../assets/blank.png"')

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

def generate_random_text():
    lorem_ipsum = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia."
    ]
    return random.choice(lorem_ipsum)

def generate_css():
    return """
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.container {
    display: flex;
    flex-direction: column;
    margin: 20px 0;
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin: -10px;
}

.col-lg-3, .col-lg-6, .col-lg-9, .col-lg-12 {
    padding: 10px;
    box-sizing: border-box;
}

.col-lg-3 { width: 25%; }
.col-lg-6 { width: 50%; }
.col-lg-9 { width: 75%; }
.col-lg-12 { width: 100%; }

.d-flex {
    display: flex;
}

.justify-content-between {
    justify-content: space-between;
}

.justify-content-center {
    justify-content: center;
}

.justify-content-end {
    justify-content: flex-end;
}

.text {
    margin: 0;
}

.text-center {
    text-align: center;
}

.text-right {
    text-align: right;
}

.paragraph {
    margin: 0;
}

.card {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 20px;
    margin-bottom: 20px;
}

.img-fluid {
    max-width: 100%;
    height: auto;
}

.form-control {
    width: 100%;
    padding: 10px;
    border-radius: 4px;
}

.btn-primary {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 4px;
}

.mx-auto {
    margin-left: auto;
    margin-right: auto;
}

.float-right {
    float: right;
}

.site-footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 1rem;
    margin-top: 20px;
}

@media (max-width: 768px) {
    .col-lg-3, .col-lg-6, .col-lg-9 {
        width: 100%;
    }
}
  """

def process_dsl_files(dsl_folder,filename, output_folder, dsl_mapping_file_path):
    compiler = Compiler(dsl_mapping_file_path)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate CSS file
    # css_path = os.path.join(output_folder, "styles.css")
    # css_content = generate_css()
    # with open(css_path, 'w') as css_file:
    #     css_file.write(css_content)

    # Process each .dsl file
   
    input_path = os.path.join(dsl_folder, filename)
    output_html_path = os.path.join(output_folder, f"{filename[:-4]}.html")

    with open(input_path, 'r') as dsl_file:
        input_dsl = dsl_file.read()
    css_path="./pages.css"
    compiler.compile(input_dsl, output_html_path, css_path)
  

# Example usage
if __name__ == "__main__":
    dsl_mapping_file_path = "dsl_mapping.json"
    dsl_folder = "dsl"
    output_folder = "output"

    process_dsl_files(dsl_folder, output_folder, dsl_mapping_file_path)
    print("All DSL files have been processed.")