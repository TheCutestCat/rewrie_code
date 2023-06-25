from Dataloader import DataLoader

if __name__ == "__main__":

    DataLoader = DataLoader(working_path = "/home/rewrie_code/test_repo")
    DataLoader.load_data()
    DataLoader.load_preprompts()
    
    # DataLoader.get_docstring() # get the description for all of it.
    # DataLoader.get_test_code() # generate the test code
    # DataLoader.save_test_code() # save the test code to file
    DataLoader.run_test_code() # this will fix the code based on the test result