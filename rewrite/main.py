from Dataloader import DataLoader

if __name__ == "__main__":
    # Data = Data(code = "code",path = "./")
    # Data.show()
        
    # function_contents, function_calls = analyze_single_file("/home/rewrite2/gpt-engineer/test_repo/gpt_engineer/chat_to_files.py")
    # function_name = re.search(r'def (\w+)\(', function_contents[1]).group(1)
    # print(function_name)
    # print(f"function_calls : {function_calls}\n")
    # print(f"function_contents : \n{function_contents[1]}\n")
    
    DataLoader = DataLoader(working_path = "/home/rewrie_code/test_repo")
    DataLoader.load_data()
    DataLoader.load_preprompts()
    
    # DataLoader.get_docstring() # get the description for all of it.
    # DataLoader.get_test_code() # generate the test code
    # DataLoader.save_test_code() # save the test code to file
    DataLoader.run_test_code() # this will fix the code based on the test result