import os
import re
from utils import analyze_single_file,to_file,run_test,change_line,print_file_contents,run_test_cmd
from AI import AI
class Data():
    def __init__(self,function_name : str, code : str,path:str):
        # contain the only one function 
        # just like : def exemple(...) : ....
        self.function_name = function_name
        self.code = code
        self.path = path # relative path
        self.description = None
        self.test_code = None
        self.test_code_feedback = None
     
    def set_attribute(self, attribute_name: str, attribute_value):
        """set the attribute 
            if the attribute_name is in the attribute of class, we will set it
            else will just return error.

        Args:
            attribute_name (str): the name
            attribute_value (_type_): the value
        """
        if hasattr(self, attribute_name)  :
            setattr(self, attribute_name, attribute_value)
        else:
            print(f"Error: '{attribute_name}' is not a valid attribute.")
    
    def get_attribute(self, attribute_name: str):
        """get the parameter VIA the name

        Args:
            attribute_name (str): the name of the parameter of the code

        Returns:
            _type_: the parameter, if the sttribute don't existe, this will return None
        """
        return getattr(self, attribute_name, None)
    
    def Data2File(path):
        # write the code into a file.
        pass
    
    def show(self):
        # show the function
        print(f"""code : {self.code} \n path : {self.path}\n description : {self.description}\n test_code : {self.test_code}\n function_path : {self.function_path}\n""")

class DataLoader():
    def __init__(self,working_path:str) -> None:
        # working_path(str) : the working path of the project
        # data_list(Data) : store the data of the code
        # call_graph(name of the Data function ) : use topological sorting to decide which function to test first. using the adjacency list
        self.working_path = working_path
        self.data_list = {}
        self.file2function = {} # store the data 
        self.function2file = {}
        self.preprompts = {}
        self.call_graph = None
        self.delimiter = "####"
        self.AI = AI()
        
    def load_data(self):
        # get the code from the python file
        # python_files = []
        # for root, dirs, files in os.walk(self.working_path):
        #     for file in files:
        #         if file.endswith('.py'):
        #             file_path = os.path.join(root, file)
        #             python_files.append(file_path)
        
        file_paths = [os.path.join(self.working_path, file_name) for file_name in os.listdir(self.working_path)]
        # this will Skip all test files and only select the python file
        filtered_files = [file_path for file_path in file_paths if not os.path.basename(file_path).startswith("test_") and file_path.endswith(".py")]
        

        for file in filtered_files:
            # function_content will be stored in the Data.
            # function_calls will be used in the call_graph.
            function_contents, function_calls = analyze_single_file(file)
            
            # get the relative_dir for the files(to import the files)
            relative_dir = os.path.relpath(file, self.working_path)
    
            # store the Data
            for function_content in function_contents:
                function_name = re.search(r'def (\w+)\(', function_content).group(1)
                # create the object 
                function_code = Data(function_name = function_name,code = function_content, path = relative_dir)
                # load the code
                self.data_list[function_name] = function_code
                
                # file2function
                if self.file2function.get(relative_dir) is None:
                    self.file2function[relative_dir] = [function_name]
                else:
                    self.file2function[relative_dir].append(function_name)

                # function2file
                if self.function2file.get(function_name) is None:
                    self.function2file[function_name] = [relative_dir]
                else:
                    self.function2file[function_name].append(relative_dir)                    
        print(f"Code loaded from {self.working_path}")
        
    def load_preprompts(self):
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        prompt_dir = os.path.join(current_file_path,"preprompts")
        for file_name in os.listdir(prompt_dir):
            file_path = os.path.join(prompt_dir, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    file_content = file_content.replace("{delimiter}", self.delimiter) #change the delimiter
                    self.preprompts[file_name] = file_content
        print(f"Prompt loaded from {prompt_dir}")      
            
    def get_file(self,function_name):
        if self.function2file.get(function_name) is None:
            return None
        else : 
            return self.function2file.get(function_name)
    
    def get_function(self,file_name):
        if self.file2function.get(file_name) is None:
            return None
        else:
            return self.file2function.get(file_name)
        
    def set_attribute(self, attribute_name: str, attribute_value):
        """set the attribute 
            if the attribute_name is in the attribute of class, we will set it
            else will just return error.

        Args:
            attribute_name (str): the name
            attribute_value (_type_): the value
        """
        if hasattr(self, attribute_name)  :
            setattr(self, attribute_name, attribute_value)
        else:
            print(f"Error: '{attribute_name}' is not a valid attribute.")
    
    def get_attribute(self, attribute_name: str):
        """get the parameter VIA the name

        Args:
            attribute_name (str): the name of the parameter of the code

        Returns:
            _type_: the parameter, if the sttribute don't existe, this will return None
        """
        return getattr(self, attribute_name, None)
    
    def get_docstring(self):
        # generate the docstring for the code.
        for key, data in self.data_list.items():
            code = data.get_attribute("code")
            function_name = data.get_attribute("function_name")
            path = data.get_attribute("path")
            system_message = DataLoader.preprompts["docstring"]
            messages =  [  
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{self.delimiter}{code}{self.delimiter}, the path for the relative path is {path}"},  
            ]
            while True:
                # Avoid problems caused by network fluctuations
                try:
                    docstring = self.AI.get_completion_from_messages(messages)
                    data.set_attribute(attribute_name = "description", attribute_value = docstring)
                    break
                except Exception as e:
                    print(f"openai api error on get_docstring function, trying again.")
        print(f"docstring generated for the code")
    
    def get_test_code(self):
        # generate the unittest code
        for key, data in self.data_list.items():
            code = data.get_attribute("code")
            function_name = data.get_attribute("function_name")
            path = self.get_attribute("path")
            file = self.get_file(f"{function_name}")
            system_message = DataLoader.preprompts["get_test_code"]
            messages =  [  
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{self.delimiter}{code}{self.delimiter}, \the path for the relative path is {path},the function is in the {file},the test code path is ./tests"},  
            ]
            while True:
                # Avoid problems caused by network fluctuations
                try:
                    docstring = self.AI.get_completion_from_messages(messages)
                    data.set_attribute(attribute_name = "test_code", attribute_value = docstring)
                    break
                except Exception as e:
                    print(f"openai api error on test_code function, trying again.")
        print(f"test code is generated")
    
    def save_test_code(self):
        # use to_file to write the code in the file.
        for key, data in self.get_attribute(attribute_name = "data_list").items():
            test_code = data.get_attribute(attribute_name = "test_code")
            name = data.get_attribute(attribute_name = "function_name")
            path = os.path.join(self.working_path,"tests","test_"+name+".py")
            to_file(code=test_code,path=path)
            
    def run_test_code(self):
        data_list = self.get_attribute(attribute_name = "data_list")
        path = os.path.join(self.working_path,"tests")
        
        #the first time to change the file
        success,error_info = run_test_cmd(path)
        print("################ STARTING TESTING THE CODE ################")
        print(f"RUNNING THE TEST CODE\n   RESULT : {success}\n   ERROR_INFO : {error_info} ")
        
        while success == False: 
            print("FIXING THE CODE")
            
            for data in error_info:
                
                function_name = data["test_function"].replace("test_", "")
                test_class = data["test_class"]
                file_name = data["file_name"]
                line_number = data["line_number"]
                error_message = data["error_message"]
                assertion_error = data["assertion_error"]
                info = f"in line {line_number}, the error happen in {error_message}, the reason is{assertion_error}"
                    
                code = data_list[function_name].get_attribute(attribute_name = "code")
                test_code = data_list[f"{function_name}"].get_attribute(attribute_name = "test_code")
            
                # give the data feedback to change the function or test_data.
                
                fixed_code = self.fix_code(test_class,info,code,test_code)
                print(f"THE FIXED CODE FROM OPANAI IS \n{fixed_code}")
                data_list[f"{function_name}"].set_attribute(attribute_name = "code",attribute_value = fixed_code)
                relative_path = data_list[f"{function_name}"].get_attribute(attribute_name = "path")
                function_name= data_list[f"{function_name}"].get_attribute(attribute_name = "function_name")
                code = data_list[f"{function_name}"].get_attribute(attribute_name = "code")
                data_list[f"{function_name}"].set_attribute(attribute_name = "code",attribute_value = "fixed_code")
                
                # find the line and change it.
                change_line(path = os.path.join(self.working_path,relative_path),function_name = function_name,code = fixed_code)
                
            print("################ RETESTING THE CODE ################")
            success,error_info = run_test_cmd(path)
            print(f"THE RESULT AFTER FIXTING\n   RESULT : {success}")
            
        print("PASS ALL THE TESTS") 
        
    def fix_code(self,test_class,info,code,test_code):
        # generate single fixed code
        system_message = self.preprompts["fix_code"]
        messages =  [  
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"the function code : {self.delimiter}{code}{self.delimiter},\
            the unittest code : {self.delimiter}{test_code}{self.delimiter},\
            the error happens on {test_class} test class.\
            the error message is :{self.delimiter}{info}{self.delimiter}"},  
            ]
        while True:
            # Avoid problems caused by network fluctuations
            try:
                fixed_code = self.AI.get_completion_from_messages(messages)
                break
            except Exception as e:
                print(f"openai api error on get_docstring function, trying again.")
        # get the clean code VIA re
        pattern = r"'''python(.*?)'''"
        for match in re.finditer(pattern, fixed_code, re.DOTALL):
            fixed_code = match.group(1)
        # print(f"##################fixed_code##################\n{fixed_code}")
        return fixed_code
        
        
if __name__ == "__main__":
    # Data = Data(code = "code",path = "./")
    # Data.show()
    
    DataLoader = DataLoader(working_path = "/home/rewrie_code/test_repo")
    DataLoader.load_data()
    DataLoader.load_preprompts()
    
    # DataLoader.get_docstring() # get the description for all of it.
    # DataLoader.get_test_code() # generate the test code
    # DataLoader.save_test_code() # save the test code to file
    DataLoader.run_test_code()

    
        
