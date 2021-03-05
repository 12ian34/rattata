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
- if a ticket is made available via resale, only 3 text messages will be sent (at hourly intervals) after which the script will be exited and will require re-running if tickets are still desired.
- this script completely ignores "add-ons" (e.g. car parking pass)
- unknown unknowns.

## Usage

### Compatibility 
This worked on Arch Linux `5.4.6-arch3-1` and Ubuntu `19.04`. I have a Virtual Private Server from Digital Ocean which is permanently on. I `ssh` into it and run the script in a [tmux](https://wiki.archlinux.org/index.php/tmux) session such that I can disconnect (and thus don't need to leave a physical computer running). This can also be achieved through other, simpler methods but I like this one.

For Windows, (aside from switching to Linux) I recommend you install [Anaconda](https://docs.anaconda.com/anaconda/install/windows/) for the full Python experience, or even [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) if you want to play around with more Linux tools in a whole `bash`-like environment. Both of these ways require your Windows computer to be kept on while running the script, obviously.

For Mac, I don't know what you should do but it's probably worth Googling "how to run Python script on mac". You'll be able to do it using terminal but I'm not sure if Python comes installed (probably not) and I'm not sure if you'll need `homebrew`.

### Requirements

- Python
- the Python packages listed in `requirements.txt`
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

- implement interactive function for setting Environment Variables according to the relevant Twilio and phone number details. 
- implement interactive function for choosing and setting the correct event URL. 
- create option for changing wait period between script re-runs.
- implement functionality for having two different wait periods per day, with a longer wait period being applied during the local night-time of the country in which the event is being held (since people probably put their tickets up for resale when they're awake ;) ).
- introduce ability to only notify when a certain minimum number of tickets become available.
- introduce ability for script to check if the resale queue is indeed active and warn if not.
- allow user to specify the particular type of tickets they're looking for (useful for events with multiple tiers of tickets or festivals with multiple days as separate tickets)
- include and monitor "add-ons" to an event (e.g. car parking pass)
