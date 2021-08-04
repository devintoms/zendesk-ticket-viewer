import get_tickets
import unittest
import sys
import json
import filecmp
"""
This file is used to perform unit tests on the various helper methods within the 'get_tickets.py' 
file. 

NOTE: Unfortunately, I was unable to complete all of my unit testing within the appropriate time 
limit, and as a result only about 35% of the ticket viewer's code is covered by unit tests. In 
their place, I have done my best to place explanations and pseudocode that describe roughly what 
each test would do if I were to be able to properly implement them. Despite all this, I feel fairly
confident that this ticket viewer is functionally sound due to the large amount of exploratory 
testing I performed throughout my development process.


Author: Devin Toms
Created: 2021/07/27
Written for the Fall 2021 Zendesk Coding Challenge.
"""



"""
Lists all tickets associated with 'zccvt.zendesk.com'. In the case that >25 tickets would be
displayed, tickets are instead split up into "pages" that the user can traverse through.

Precondition: all_tickets must contain a key "tickets" corresponding to a list[dict] of at least 
              size 1 (which represents a successful API call).

NOTE: This class tests the listAllTickets method. Logically speaking, this helper method is fairly
simple, really only consisting of an if-else statement that determines how future output will be
displayed. We do not need to test the case of an empty ticket list, as this would result in a 
failed API call, which will be caught prior to this method running and will therefore never 
realistically occur.
"""
class ListAllTicketsTests(unittest.TestCase):

    # Tests that the output is properly paged when more than 25 tickets are entered
    @unittest.mock.patch("get_tickets.input", create=True)
    def testListAllTicketsHundred(self, mocked_input):
        mocked_input.side_effect = ["q"]
        
        input_file = open("test_io/more_tickets.json")
        test_file = open("test_io/LAT_101_output.txt")

        # setup method output to file
        output_file = open("test_io/more_output.txt", "r+")
        old_stdout = sys.stdout
        sys.stdout = output_file

        json_multi = json.loads(input_file.read())
        get_tickets.listAllTickets(json_multi)

        # compare the output file to the "control group" output
        assert  filecmp.cmp("test_io/LAT_101_output.txt", "test_io/more_output.txt")

        # cleanup
        sys.stdout = old_stdout
        input_file.close()
        test_file.close()
        output_file.close()

    # Tests that the output is properly paged when less than 25 tickets are entered
    @unittest.mock.patch("get_tickets.input", create=True)
    def testListAllTicketsOne(self, mocked_input):
        mocked_input = 'q'
        
        input_file = open("test_io/less_tickets.json")
        test_file = open("test_io/LAT_1_output.txt")

        # setup method output to file
        output_file = open("test_io/less_output.txt", "r+")
        old_stdout = sys.stdout
        sys.stdout = output_file

        json_multi = json.loads(input_file.read())
        get_tickets.listAllTickets(json_multi)

        # compare the output file to the "control group" output
        assert  filecmp.cmp("test_io/LAT_1_output.txt", "test_io/less_output.txt")

        # cleanup
        sys.stdout = old_stdout
        input_file.close()
        test_file.close()
        output_file.close()

"""
Formats an individual ticket in an aesthetically pleaseing manner. For readability purposes when 
viewing a large amount of tickets, only the ID, Subject, Creation time, and Ticket URL are shown.

Precondition: The given ticket must include the following four keys: "id", "subject", 
                                                                     "created_at", "url"

NOTE: This method is purely front-end oriented, and is therefore being tested primarily for code 
coverage purposes.
"""
class FormatTicketTests(unittest.TestCase):
    
    # Tests the the given ticket was output in a properly formatted manner
    @unittest.mock.patch("get_tickets.input", create=True)
    def testFormatTicket(self, mocked_input):
        mocked_input = 'q'

        input_file = open("test_io/lone_ticket.json")
        test_file = open("test_io/FT_output.txt")

        # setup method output to file
        output_file = open("test_io/lone_output.txt", "r+")
        old_stdout = sys.stdout
        sys.stdout = output_file

        json_multi = json.loads(input_file.read())
        get_tickets.formatTicket(json_multi)

        # compare the output file to the "control group" output
        assert  filecmp.cmp("test_io/FT_output.txt", "test_io/lone_output.txt")

        # cleanup
        sys.stdout = old_stdout
        input_file.close()
        test_file.close()
        output_file.close()

"""
NOTE: I faced particular difficulty with the following two methods, as most of if not all of the 
routes being tested involve at least one call to the Zendesk API, which I had challenges properly
mocking.

class ListMultipageTests(unittest.TestCase):

    ***PSEUDOCODE***

    # Tests when the user tries to go back and forth from another page of tickets
    @unittest.mock.patch("get_tickets.input", create=True)
    def testListMultipageNextPage(self, mocked_input):

        mock inputs required to go to the next page, then back again, then quit
        mock return value from API call for next page of tickets

        open input file (that contains first 100 tickets)
        open test file (that contains desired output)

        # setup method output to file
        open output file
        change sys.stdout to output file

        read input file and convert from JSON

        # compare the output file to the desired output
        assert that contents of output file match contents of test file

        # cleanup
        revert sys.stdout from file to terminal window
        close input, test, and output files


    # Tests when the user goes back and forth through the same page of tickets
    @unittest.mock.patch("get_tickets.input", create=True)
    def testListMultipageSamePage(self, mocked_input):

        mock inputs required to go up until the next page, then back to first chunk, then quit

        open input file (that contains 100 tickets)
        open test file (that contains desired output)

        # setup method output to file
        open output file
        change sys.stdout to output file

        read input file and convert from JSON

        # compare the output file to the desired output
        assert that contents of output file match contents of test file

        # cleanup
        revert sys.stdout from file to terminal window
        close input, test, and output files


    # Tests when the user tries to move forward/backward but cannot
    @unittest.mock.patch("get_tickets.input", create=True)
    def testListMultipageNextPage(self, mocked_input):

        mock inputs required to go back on first chunk of 25, and next on last chunk, then quit

        open input file (that contains first 100 tickets)
        open test file (that contains desired output)

        # setup method output to file
        open output file
        change sys.stdout to output file

        read input file and convert from JSON

        # compare the output file to the desired output
        assert that contents of output file match contents of test file

        # cleanup
        revert sys.stdout from file to terminal window
        close input, test, and output files


    # Tests when the user enters an incorrect command
    @unittest.mock.patch("get_tickets.input", create=True)
    def testListMultipageNextPage(self, mocked_input):

        mock input representing a garbage command, then quit

        open input file (that contains at least 1 ticket)
        open test file (that contains desired output)

        # setup method output to file
        open output file
        change sys.stdout to output file

        read input file and convert from JSON

        # compare the output file to the desired output
        assert that contents of output file match contents of test file

        # cleanup
        revert sys.stdout from file to terminal window
        close input, test, and output files

"""

"""

class MainTests(unittest.TestCase):

    ***PSEUDOCODE***

    # Tests when the user successfully chooses the first option
    @unittest.mock.patch("get_tickets.input", create=True)
    @mock-patch HTTP response
    def testMainOne():
    mock input for selecting the 1st option, the selecting a ticket, then return to main menu, then quit
    mock HTTP response with status code #200 (successful)

    open input file (that contains what mimics a valid HTTP response from the Zendesk Ticket API)
    open test file (that contains desired output)

    # setup method output to file
    open output file
    change sys.stdout to output file

    # compare the output file to the desired output
    assert that contents of output file match contents of test file

    # cleanup
    revert sys.stdout from file to terminal window
    close input, test, and output files


    # Tests when the user successfully chooses the first option but selects a non-existent ticket
    @unittest.mock.patch("get_tickets.input", create=True)
    @mock-patch HTTP response
    def testMainOneNoTicket():
        mock input for selecting the 2nd option, then return to main menu after error, then quit
        mock HTTP response with status code #404 (for ticket not found)

        open test file (that contains desired output)

        # setup method output to file
        open output file
        change sys.stdout to output file

        # compare the output file to the desired output
        assert that contents of output file match contents of test file

        # cleanup
        revert sys.stdout from file to terminal window
        close input, test, and output files


    # Tests when the user successfully chooses the second option
    @unittest.mock.patch("get_tickets.input", create=True)
    @mock-patch HTTP response
    def testMainTwo():    
    mock input for selecting the 2nd option, then return to main menu, then quit
    mock HTTP response with status code #200 (successful)

    open input file (that contains what mimics a valid HTTP response from the Zendesk Ticket API)
    open test file (that contains desired output)

    # setup method output to file
    open output file
    change sys.stdout to output file

    # compare the output file to the desired output
    assert that contents of output file match contents of test file

    # cleanup
    revert sys.stdout from file to terminal window
    close input, test, and output files



    # Tests when the user enters an invalid command
    @unittest.mock.patch("get_tickets.input", create=True)
    def testMainInvalid():
        mock input representing a garbage command, then quit

        open test file (that contains desired output)

        # setup method output to file
        open output file
        change sys.stdout to output file

        # compare the output file to the desired output
        assert that contents of output file match contents of test file

        # cleanup
        revert sys.stdout from file to terminal window
        close input, test, and output files


    # Tests when the user makes a valid request, but the Zendesk Ticket API is unavailable to
    # fulfill the request
    @unittest.mock.patch("get_tickets.input", create=True) 
    @mock-patch HTTP response
    def testMainAPIUnavailable():
        mock input for selecting the 2nd option, then return to main menu after error, then quit
        mock HTTP response with status code #503 (for server unavailable)

        open test file (that contains desired output)

        # setup method output to file
        open output file
        change sys.stdout to output file

        # compare the output file to the desired output
        assert that contents of output file match contents of test file

        # cleanup
        revert sys.stdout from file to terminal window
        close input, test, and output files



"""