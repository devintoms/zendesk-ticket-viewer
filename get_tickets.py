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

user = input("Please enter an email address:") + "/token"
token = input("Please enter an API token: ")


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
Formats an individual ticket in an aesthetically pleaseing manner. For readability purposes when 
viewing a large amount of tickets, only the ID, Subject, Creation time, and Ticket URL are shown.
"""
def formatTicket(ticket: dict):
    print("-----------------------------------------------------")
    print('Ticket ID #{0}: "{1}"'.format(ticket["id"], ticket["subject"]))
    print("Created on {0} at {1} UTC".format(ticket["created_at"][:10], ticket["created_at"][11:19]))
    print("URL: {0}".format(ticket["url"]))
    print("-----------------------------------------------------")


"""
Controls the the bulk ticket viewer in the case that tickets will have to be displayed over 
multiple pages (>25 tickets).
"""
def listMultipage(all_tickets: dict):
    # NOTE: what the ZCC requirements doc refers to as "pages" is referred to as "chunks" within 
    # this method. The pages referred to within this method are the same as pagination within the 
    # Ticket API.

    current_page = 0
    current_chunk = 0
    i = 0

    # continue to display ticket chunks as many times as needed until the user quits
    while (True):
        tickets = all_tickets["tickets"][(current_chunk * 25):((current_chunk * 25) + 25)]
        for ticket in tickets:
            formatTicket(ticket)
            print()

        # display user's current options
        print()
        print("!~!~!-----------------------------------------------!~!~!")
        print("The following actions can be performed:") 
        print()
        if ((current_chunk == 3 and all_tickets["next_page"] != None) or (current_chunk < 3 and (i + 25) <= len(all_tickets["tickets"]))):
            print("next (n)\t\tDisplays the next 25 tickets.")
            can_next = True
        if ((current_chunk > 0) or (current_chunk == 0 and all_tickets["previous_page"] != None)):
            print("back (b)\t\tDisplays the previous 25 tickets.")
            can_back = True
        print("quit (q)\t\tReturns to the main menu.")
        print()
        print("!~!~!-----------------------------------------------!~!~!")
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

# "JSON response -> ticket value" format: dict -> list -> dict

while(True):
    print()
    print("Welcome to the ticket viewer!")
    print()
    # display user's current options
    print("!~!~!-----------------------------------------------!~!~!")
    print("The following actions can be performed:") 
    print()
    print("1                        View a single ticket.")
    print("2                        View a list of all tickets.")
    print("quit (q)                 Exits the ticket viewer.")
    print()
    print("!~!~!-----------------------------------------------!~!~!")
    print()

    cmd = input("Please input your next action: ").lower()
    print()

    if (cmd == "quit" or cmd == "q"):
        break
    elif (cmd == "1"):
        ticket = "https://zccvt.zendesk.com/api/v2/tickets/" + input("Please enter the ID of the ticket you would like to view: ") + ".json"
        response = requests.get(ticket, auth=(user, token))
        print()
        if (response.status_code == requests.codes.ok):
            json_response = response.json()
            formatTicket(json_response["ticket"])
            print()
            input("Ticket found! When ready, press enter to return to the main menu.")
        elif (response.status_code == 404):
            print("!~!~!-----------------------------------------------------------!~!~!")
            print()
            print("The requested ticket could not be found. Please try again with a different ID.")
            print()
            print("!~!~!-----------------------------------------------------------!~!~!")
            print()
            input("Please press enter to return to the main menu.")
        else:
            print("!~!~!-----------------------------------------------------------!~!~!")
            print()
            print("The ticket request was not successful. The HTTP status code is:", response.status_code)
            print()
            print("!~!~!-----------------------------------------------------------!~!~!")
            print()
            input("Please press enter to return to the main menu.")
    elif (cmd == "2"):
        # retrieve all tickets associated with the user's account
        response = requests.get('https://zccvt.zendesk.com/api/v2/tickets.json', auth=(user, token))
        if (response.status_code == requests.codes.ok):
            json_response = response.json()
            listTicketChunk(json_response)
        else:
            print("!~!~!-----------------------------------------------------------!~!~!")
            print()
            print("The ticket request was not successful. The HTTP status code is:", response.status_code)
            print()
            print("!~!~!-----------------------------------------------------------!~!~!")
            print()
            input("Please press enter to return to the main menu.")
    else:
        print("The command entered was not valid, please try again.")