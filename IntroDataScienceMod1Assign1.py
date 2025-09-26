import re
simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
Ruth and Peter, their parents, have 3 kids."""

def names(text: str = simple_string):
    result = re.findall(r"\b[A-Z][a-zA-Z]*", text)
    return result
  
def grades():
    B_Students = []
    with open ("assets/grades.txt", "r") as file:
        for line in file:
            b_check = re.search(r"B\s*$",line)
            if b_check:
                temp_name = re.match(r"([A-Z][a-z]+) ([A-Z][a-z]+)", line)
                B_Students.append(temp_name.group())
    return B_Students

import re
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
