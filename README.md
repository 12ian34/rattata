# rattata 

Resident Advisor ticket resale watcher

## Context

**Resident Advisor** is a website focused on electronic music, particularly ticket sales to live music events and club nights around the world. For some events where the tickets have sold out, a "Resale queue" is made active. If one would like to attend a sold out event with the resale queue active, they would need to keep refreshing the event page in the hope that some tickets were made available since there is no notification option. 

**Twilio** is an API platform which provides a 'virtual' SMS service.  One can sign up for a free trial which provides £15 free credit.

## Functionality

`rattata` is a python script that checks the resale queue - at an imperfectly defined interval - for the availability of a particular ticket to a particular event and sends a text message when at least 1 ticket becomes available.

## Limitations

- one must manually find the resident advisor URL (e.g. https://ra.co/events/1432652) for the event of interest. Upon running the script, the user is asked for the URL which must then manually be entered.
- one must manually create a Twilio account, and also have a mobile number. The relevant details must then be set as Environment Variables for the script to pick up.
- if a ticket is made available via resale, only 2 text messages will be sent (at hourly intervals) after which the script will be exited and will require re-running if tickets are still desired.
- unknown unknowns.

## Usage

### Compatibility 
This worked on Arch Linux `5.4.6-arch3-1` onwards, Ubuntu `19.04`, Windows Subsystem for Linux (Ubuntu 19.04 I think) and a couple of Raspberry Pis running various versions of Raspbian and the latest (as of Feb 2021) Raspberry Pi OS Lite. 
Personally, I have a Raspberry Pi permanently switched on so I run the script from there, accessing it via `ssh` and running the script in a [tmux](https://wiki.archlinux.org/index.php/tmux) session such that I can disconnect from the session as the script runs.

### Requirements

- Python 3.6 or later
- the Python packages listed in `requirements.txt` to be installed
- a Twilio account (a trial one comes with enough credit for basic usage) with a twilio phone number, your `auth token` and your `SID`
- the need to buy a ticket to a sold out event on Resident Advisor which has the resale queue active

### Installation and usage

```
git clone https://github.com/12ian34/rattata.git
cd rattata
pip install -r requirements.txt
export TWILIO_SID="<your twilio SID>"
export MY_NUMBER="<your mobile number with the plus sign and international prefix>"
export TWILIO_AUTH_TOKEN="<your twilio auth token>"
export TWILIO_NUMBER="<your twilio virtual mobile number"
python ra-ticket-resale-watch.py
```
then, enter full resident advisor url in the input field provided and press `Return` and await the SMS from your Twilio phone number to your personal phone number when a ticket becomes available! Remember that for as long as the script is running whilst at least one resale ticket is available, you will be sent up to three texts at hourly intervals, after which the script will exit and must be re-run if you still require a ticket.

## Future work

- allow user to create option for changing wait period between script re-runs.
- adjust wait period based on event local time, with longer wait periods during the night.
- allow user to select a minimum quantity of tickets required.
- warn user in case resale queue is not active for the event.
- allow user to track multiple different ticket types (e.g. different sale stages, or ticket + car park pass).
- test script against more events. perhaps there are other issues such as odd ticketing structures and hierarchies.
