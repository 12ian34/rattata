# rattata 

Resident Advisor ticket resale watcher

## Context

**Resident Advisor** is a fantastic website focused on electronic music, particularly on ticket sales to live music events and club nights around the world. For some events where the tickets have sold out, a "Resale queue" is made active. If one would like to attend a sold out event with the resale queue active, they would need to keep refreshing the event page in the hope that some tickets were made available since there is no notification option. 

**Twilio** is an API platform company which provides a tool to programmatically send text messages. One can sign up for a free trial which provides £15 free credit.

## Functionality

`rattata` is a python script that checks the resale queue - at an imperfectly defined interval - for available tickets to a particular event and sends a text message when at least 1 ticket becomes available.

## Limitations

- one must manually find the resident advisor URL (e.g. https://www.residentadvisor.net/events/1346399) for the event of interest. Upon running the script, the user is asked for the URL which must then manually be entered.
- one must manually create a Twilio account, and also have a mobile number. The relevant details must then be set as Environment Variables for the script to pick up.
- the defined interval doesn't take into account the time it takes to run the script. This isn't very Pythonic but I don't care.
- if a ticket is made available via resale, only 3 text messages will be sent after which the script will be exited and will require re-running if tickets are still desired.
- unknown unknowns.

## Future work

- implement interactive function for setting Environment Variables according to the relevant Twilio and phone number details. 
- implement interactive function for choosing and setting the correct event URL. 
