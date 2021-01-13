import json
import time
from datetime import datetime

def getTime(t):
    """
    Returns a string after converting time in seconds to hours/mins/secs

    Paramters:
        t (float): time in seconds
    Returns:
        s (str): number of hours, if more than 1 hour
                number of minutes and seconds, if more than 1 minute
                number of seconds, otherwise
    """
    if t >= 3600:
        s = str(round(t // (3600), 2)) + " hours.\n"
    elif t >= 60:
        s = str(t // 60) + " mins, " + str(t % 60) + " secs.\n"
    else:
        s = str(t) + " secs.\n"
    return s

# def inputDetails():
    # """
    # Inputs user details.

    # Returns:
    #     data_dict (dict): Dictionary containing user data
    # """
    # data_dict = {}
    # with open("details.json", "r+") as json_file:
    #     json_data = json.load(json_file)
    #     if "user_agent" in json_data:
    #         data_dict["user_agent"] = json_data["user_agent"]
    #     else:
    #         data_dict["user_agent"] = input("Enter your user agent (Google it!):\n")
    #         json_data["user_agent"] = data_dict["user_agent"]
    #         json_file.seek(0)
    #         json_file.truncate()
    #         json.dump(json_data, json_file, indent=4, sort_keys=True)

    #     data_dict["URL"] = input("\nEnter product URL:\n")
    #     data_dict["Intent"] = input("\nyour intent?\n")
    #     data_dict["pricedifference"]  = float(input("\nby how much?\n"))
    #     # disc = ""
    #     # while(True):
    #     #     # Continuously ask for input until valid figure is provided
    #     #     try:
    #     #         disc = float(input("\nEnter the discount % required: "))
    #     #         break
    #     #     except:
    #     #         pass

    #     # data_dict["discount"] = float(disc)
    #     data_dict["often"] = float(
    #         input("\nEnter (in secs.) how often you'd like to check the price: "))

    #     # input username or load from json
    #     # takeInput = False
    #     # if "username" in json_data:
    #     #     print("\nGmail ID:", json_data["username"])
    #     #     ch = input("Proceed? (y/ n): ")
    #     #     if ch in ['Y', 'y']:
    #     #         data_dict["username"] = json_data["username"]
    #     #     else:
    #     #         takeInput = True
    #     # if takeInput or "username" not in json_data:
    #     #     data_dict["username"] = input("\nEnter your Gmail ID: ")
    #     #     json_data["username"] = data_dict["username"]
    #     #     json_file.seek(0)
    #     #     json_file.truncate()
    #     #     json.dump(json_data, json_file, indent=4, sort_keys=True)
    #     # # input password safely
    #     # data_dict["password"] = getpass("Enter your password: ")

    # return data_dict




