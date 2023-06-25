import ast
from ast import get_source_segment
import os
import unittest
import os
import re
import openai
from AI import AI
import astor
import subprocess

def analyze_single_file(filename,target = ast.FunctionDef):
    # we can change the target to ast.ClassDef\
    # to analyse the source of the code.
    with open(filename, 'r') as file:
        content = file.read()
        tree = ast.parse(content)

    # functions = [func for func in ast.walk(tree) if isinstance(func,target) and not isinstance(func.parent, ast.ClassDef)]
    # select just the functions
    function_defs = get_function_defs(tree)
    functions = [func for func, parent in function_defs if not isinstance(parent, ast.ClassDef)]
    
    function_names = [func.name for func in functions]

    function_bodies = []
    function_calls = {}

    for function in functions:
        function_bodies.append(get_source_segment(content, function))

        calls = [node.func.id for node in ast.walk(function) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)]
        function_calls[function.name] = [call for call in calls if call in function_names]

    return function_bodies, function_calls

def get_function_defs(node, parent=None):
    function_defs = []
    for child_node in ast.iter_child_nodes(node):
        if isinstance(child_node, ast.FunctionDef):
            function_defs.append((child_node, parent))
        else:
            function_defs.extend(get_function_defs(child_node, parent=child_node))
    return function_defs

def get_class_function_defs(node, class_name=None):
    class_function_defs = []
    for child_node in ast.iter_child_nodes(node):
        if isinstance(child_node, ast.ClassDef):
            class_name = child_node.name
            class_function_defs.extend(get_class_function_defs(child_node, class_name=class_name))
        elif isinstance(child_node, ast.FunctionDef):
            if class_name:
                class_function_defs.append((child_node, class_name))
        else:
            class_function_defs.extend(get_class_function_defs(child_node, class_name=class_name))
    return class_function_defs

def to_file(path:str,code:str):
    # check the folder
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    # create the file
    if os.path.exists(path):
        os.remove(path)  
    with open(path, "w") as file:
        file.write(code)
        
class run_test():
    def __init__(self,test_file_path) -> None:
        self.test_file_path = test_file_path
    
        #use the test_loader to load all the files in folder "tests"
        self.test_loader = unittest.TestLoader()
        self.test_module = self.test_loader.discover(self.test_file_path)
        self.test_runner = unittest.TextTestRunner()
    def run(self):
        print_file_contents(self.test_file_path)
        
        self.test_result  = self.test_runner.run(self.test_module)
        
        self.success = self.test_result.wasSuccessful()
        self.errors = self.test_result.errors
        self.failures = self.test_result.failures
    
        error_info = []
        # extract the information from the failures.
        for failure_info in self.failures:
            failure_info = str(failure_info)
            match = re.search(r'\(<([^>]+) testMethod=\w+\>', failure_info)
            matched_string = match.group(1) if match else None
            function_name, test_class = matched_string.split('.') if matched_string else (None, None)
            function_name = function_name.replace("test_", "") # replace it with funciton name
            
            match = re.search(r'line .*', failure_info)
            info = match.group() if match else None
            data = {
                'function_name': f'{function_name}',
                'test_class': f"{test_class}",
                'error_info': f'{info}'
            }
            error_info.append(data)
        print("run the test")
        return self.success,error_info

def run_test_cmd(test_file_path:str):
    # file_name = "/home/rewrite2/gpt-engineer/test_repo/tests"
    file_name = test_file_path
    result = subprocess.run(['python', '-m', 'unittest', "discover", "-s", file_name], capture_output=True, text=True)
    sucess = not bool(result.returncode)
    text = result.stderr
    
    pattern = r"FAIL: (.*?) \((.*?)\)\n-*\nTraceback.*?File \"(.*?)\", line (\d+).*?\n(.*?)\nAssertionError: (.*?)\n"
    matches = re.findall(pattern, text, re.DOTALL)

    # 保存提取的信息到字典
    results = []
    for match in matches:
        test_function = match[0]
        test_class = match[1]
        file_name = match[2]
        line_number = match[3]
        error_message = match[4].strip()
        assertion_error = match[5]

        result = {
            "test_function": test_function,
            "test_class": test_class,
            "file_name": file_name,
            "line_number": line_number,
            "error_message": error_message,
            "assertion_error": assertion_error
        }
        results.append(result)

    return sucess,results

def change_line(path,function_name,code):
    with open(path, "r") as file:
        source_code = file.read()
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            tree.body.remove(node)
            new_code_ast = ast.parse(code)
            new_code_body = new_code_ast.body
            tree.body.extend(new_code_body)
            new_source_code = astor.to_source(tree)

            with open(path, "w") as file:
                file.write(new_source_code)
            break
    
def print_folder_contents(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.endswith('.py'):
            print("文件名:", item)
            with open(item_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print("内容:")
                print(content)
            print("-------------------------------------------")
        elif os.path.isdir(item_path):
            print_file_contents(item_path)

def print_file_contents(file_path):
    if os.path.isfile(file_path) and file_path.endswith('.py'):
        print("文件名:", file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print("内容:")
            print(content)
        print("-------------------------------------------")

if __name__ == "__main__":
    # function_bodies, function_calls = analyze_single_file(filename = "/home/rewrite2/gpt-engineer/test_repo/func.py")
    # print(function_bodies)
    # to_file(code = "test the to_file",path="/home/rewrite2/gpt-engineer/test_repo/gpt_engineer/tests/test_to_file.py")
    # run_test(test_file_path = "/home/rewrite2/gpt-engineer/test_repo/tests")
    # print_file_contents("/home/rewrite2/gpt-engineer/test_repo/func.py")
    
    run_test_cmd(test_file_path="/home/rewrite2/gpt-engineer/test_repo/tests")