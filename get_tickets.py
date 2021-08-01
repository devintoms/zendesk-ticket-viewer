"""
***CURRENTLY WIP***
This script, given the user's Zendesk login info, retrieves a list of all the tickets associated
with the account and displays them in a nicely formatted manner within the command line.
Author: Devin Toms
Created: 2021/07/27
Written for the Fall 2021 Zendesk Coding Challenge.
"""
import requests
import json

user = input("Please input username: ")
token = input("Please input API token: ")

"""
Prints the given string into the terminal window such that no single line exceeds 100 characters
in length. Includes newline and tab characters, and finishes with a newline character.
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

"""
Controls the the bulk ticket viewer in the case that tickets will have to be displayed over 
multiple pages (>25 tickets).
"""
def listMultipage(all_tickets: dict):
    # NOTE: what the documentation refers to as "pages" and referred to as "chunks" within this 
    # method. The pages referred to within this method are the same as pagination within the 
    # Ticket API.

    # cursor-style

    # if on chunk 3 and select "next", go to next page

    # if on chunk 0 and select "back", go to previous page
    current_page = 0
    current_chunk = 0
    i = 0

    # continue to display ticket chunks as many times as needed until the user quits
    while (True):
        tickets = all_tickets["tickets"][(current_chunk * 25):((current_chunk * 25) + 25)]
        for ticket in tickets:
            formatTicket(ticket)
            print()

        print("curent page:", current_page)
        print("current chunk:", current_chunk)
        print("i = ", i)

        # display user's current options
        print()
        print("!~~-----------------------------------------------~~!")
        print("The following actions can be performed:") 
        if ((current_chunk == 3 and all_tickets["next_page"] != None) or (current_chunk < 3 and (i + 25) <= len(all_tickets["tickets"]))):
            print("next\t\tDisplays the next 25 tickets.")
            can_next = True
        if ((current_chunk > 0) or (current_chunk == 0 and all_tickets["previous_page"] != None)):
            print("back\t\tDisplays the previous 25 tickets.")
            can_back = True
        print("quit\t\tReturns to the main menu.")
        print("!~~-----------------------------------------------~~!")
        print()

        cmd = input("Please input your next action: ").lower()
        print()

        if (cmd == "quit" or cmd == "q"):
            break
        elif (cmd == "next" or cmd == "n"):
            # ensure that moving forward is legal
            if (can_next):
                if (current_chunk == 3):
                    current_page += 1
                    current_chunk = 0
                    response = requests.get(all_tickets["next_page"], auth=(user, token))
                    all_tickets = response.json()
                else:
                    current_chunk += 1
            else:
                print()
                print("You cannot use this command here, please try a different one.")
        elif (cmd == "back" or cmd == "b"):
            # ensure that going backward is legal
            if (can_back):
                if (current_chunk == 0):
                    current_page -= 1
                    current_chunk = 3
                    response = requests.get(all_tickets["previous_page"], auth=(user, token))
                    all_tickets = response.json()
                else:
                    current_chunk -= 1
            else:
                print()
                print("You cannot use this command here, please try a different one.")
        # catches invalid commands
        else:
            print("Unrecognized command, please try again.")

        # reset cursory flags
        can_next = False
        can_back = False

        print()

"""
***DOCUMENTATION WIP***
"""
def listTicketChunk(all_tickets: dict):
    # show tickets on-screen in 25 ticket chunks
    if (all_tickets["count"] < 1):
        print("There are no tickets! Please add some and try again.")

    elif (all_tickets["count"] > 25):
        listMultipage(all_tickets)

    else:
        # display each ticket with formatting
        for ticket in all_tickets["tickets"]:
            formatTicket(ticket)
            print()

# retrieve all tickets associated with the user's account
response = requests.get('https://zccvt.zendesk.com/api/v2/tickets.json', auth=(user, token))
# "JSON response -> ticket value" format: dict -> list -> dict

if (response.status_code == 200):
    print("Welcome to the ticket viewer!")
    print()
    json_response = response.json()

    listTicketChunk(json_response)

else:
    print("The ticket request has failed. The HTTP status code is:", response.status_code)