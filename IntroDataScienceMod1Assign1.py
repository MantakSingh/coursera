import re
'''
Part A
Find a list of all of all of the names in the following string using regex.'''

simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
Ruth and Peter, their parents, have 3 kids."""

def names(text: str = simple_string):
    result = re.findall(r"\b[A-Z][a-zA-Z]*", text)
    return result

'''Part B
The dataset file in assets/grades.txt contains a line separated list of people with their grade in a class. 
Create a regex to generate a list of just those students who received a B in the course.'''

def grades():
    B_Students = []
    with open ("assets/grades.txt", "r") as file:
        for line in file:
            b_check = re.search(r"B\s*$",line)
            if b_check:
                temp_name = re.match(r"([A-Z][a-z]+) ([A-Z][a-z]+)", line)
                B_Students.append(temp_name.group())
    return B_Students

'''Part C
Consider the standard web log file in assets/logdata.txt. This file records the access a user makes when visiting a web page (like this one!). 
Each line of the log has the following items:

a host (e.g., '146.204.224.152')
a user_name (e.g., 'feest6811' note: sometimes the user name is missing! In this case, use '-' as the value for the username.)
the time a request was made (e.g., '21/Jun/2019:15:45:24 -0700')
the post request type (e.g., 'POST /incentivize HTTP/1.1' note: not everything is a POST!)
Your task is to convert this into a list of dictionaries, where each dictionary looks like the following:

example_dict = {"host":"146.204.224.152", 
                "user_name":"feest6811", 
                "time":"21/Jun/2019:15:45:24 -0700",
                "request":"POST /incentivize HTTP/1.1"}'''
def logs():
    logs_list = []
    log_dict_keys = ["host", "user_name", "time", "request"]
    with open("assets/logdata.txt", "r") as file:
        for line in file:
            temp_dict = dict.fromkeys(log_dict_keys, None)
            
            ## host
            host_match = re.search(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", line)
            temp_dict["host"] = host_match.group()
            
            #user_name
            user_match = re.search(r"-\s(\S+)\s\[", line)
            temp_dict["user_name"] = user_match.group(1) if user_match else "-"
 
            # time
            time_match = re.search(r"\[([^\]]+)\]",line)
            temp_dict["time"] = time_match.group(1)
            
            #request
            request_match = re.search(r'"([^"]+)"',line)
            temp_dict["request"] = request_match.group(1) if request_match else "-"
            
            logs_list.append(temp_dict)
    return logs_list
