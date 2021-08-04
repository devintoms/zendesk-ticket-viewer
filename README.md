# zendesk-ticket-viewer

Hello, and welcome to the ZCCVT Ticket Viewer!
This document is split into two distinct parts. The first contains information about the ticket viewer itself, including isntructions on installation and usage. The second is similar in nature, but covers how to conduct unit tests on the ticket viewer.


Section 1: Ticket Viewer
----------------------------------------------------
Installation: 
    
   1. Download and install the latest version of Python. It can be found here: https://www.python.org/downloads/

   2. Download or pull this repository to the directory from which you woud like this program to run.
    
   3. Create a file named "login.txt" (no quotations). 
    
   4. Open "login.txt". On the first line, enter the email address you would like to use to access zccvt.zendesk.com from.
 
   5. At the end of your email address, add the phrase "/token" (no quotations). Ex: "example@email.com/token"
    
   6. On the second line, enter an API token for zccvt.zendesk.com. 
    
   7. Once entered, save and exit "login.txt". Installation is now complete.
    
Usage:
    
   The ticket viewer can be launched by running the "get_tickets.py" file. How this is done is up to the user, though command line access is recommended since that is  how the ticket viewer takes user I/O. Once the programs starts, the user is presented with 3 options, of which they type their selection into the prompt and press 'enter':
    
   1:   View a single ticket. If the user selects this option, they are presented a prompt which requires them to enter a valid ticket ID. If they do, they are presented with a short summary of information about the ticket; if not, they are given an error message. Pressing 'enter' on either prompt will return the user to the main menu.
    
   2:   View a list of all tickets. If the user selects this option. They are given a list of all tickets currently associated with zccvt.zendesk.com, seperated into groups of 25 for greater readability. These tickets are listed in ascending order of ticket ID number. The user is also given another prompt, which they are able to use in the same way as the main menu's prompt. These prompt options change dynamically as the user moves through the different ticket groups, though the "quit" option is always available to return to the main menu.
    
   quit: Allows the user to exit the program.
   
   
   Section 2: Unit Tests
   ---------------------------------------

NOTE: While comparisons and user input mocking are performed using the syntax of the unittest framework, actual testing and validation were performed using the pytest framework through a Windows command line. Because of this, results may vary if you choose to run the test file using the standard unittest framework, and I instead recommend using pytest instead.

Installation/Usage:

   1. Install pytest. Instructions to do so can be found here: https://docs.pytest.org/en/6.2.x/getting-started.html#getstarted

   2. Using a command line tool (such as Command Prompt), locate and move to the directory containing the ticket viewer.
   
   3. Enter and run the following command: "pytest -s unittests.py"

