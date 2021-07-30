"""
***CURRENTLY WIP***
This script, given the user's Zendesk login info, retrieves a list of all the tickets associated
with the account and displays them in a nicely formatted manner within the command line.
Author: Devin Toms
Created: 2021/07/27
Written for the Zendesk Coding Challenge.
"""
import requests

"""
***DOCUMENTATION WIP***
Prints long strings
"""
def longStringPrinter(long_string: str):
    # seperate string into "words"
    words = long_string.split(" ")
    line_builder = ""
    for word in words:
        # if line length limit hasn't been reached, simply append word to line
        if (len(word) + len(line_builder) + 1 <= 100):
            if (len(line_builder) != 0):
                line_builder += " "
            line_builder += word
        # if line length limit has been reached, append word to next line 
        else:
            print(line_builder)
            line_builder = ""
            line_builder += word
    # print leftover words 
    print(line_builder)

        
"""
***DOCUMENTATION WIP***
Formats ticket to look pretty
"""
def formatTicket(ticket: dict):
    print("-----------------------------------------------------")
    print()
    print("ID #{0}: {1}".format(ticket["id"], ticket["subject"]))
    print("Created at {0}".format(ticket["created_at"]))
    print("{0}".format(ticket["url"]))
    print()
    print("Description:\n")
    longStringPrinter(ticket["description"])
    print()
    print("-----------------------------------------------------")

# get the user's Zendesk username and password for authentication purposes
username = input("Please enter a username: ")
password = input("Please enter a password: ")

# retrieve all tickets associated with the user's account
response = requests.get("https://zccvt.zendesk.com/api/v2/tickets.json", auth=(username, password))

# "JSON response -> ticket value" format: dict -> list -> dict
print(response)

json_response = response.json()

# display each ticket with formatting
for ticket in json_response["tickets"]:
    formatTicket(ticket)
    print()