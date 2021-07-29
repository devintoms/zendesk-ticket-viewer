"""
***CURRENTLY WIP***

This script, given the user's Zendesk login info, retrieves a list of all the tickets associated
with the account and displays them in a nicely formatted manner within the command line.

Author: Devin Toms
Created: 2021/07/27
Written for the Zendesk Coding Challenge.
"""
import requests

# get the user's Zendesk username and password for authentication purposes
username = input("Please enter a username: ")
password = input("Please enter a password: ")

# retrieve all tickets associated with the user's account
response = requests.get("https://zccvt.zendesk.com/api/v2/tickets.json", auth=(username, password))

# test that the request was successful
print(response)
json_response = response.json()
#for item in range(len(json_response)-2):
#    print(json_response)