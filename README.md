# basicFitAPI
Basic Fit API allowing Booking - Cancelling - Viewing gym time sessions

**Disclaimer:** _Use this script on your own risks._

## Requirements

| Package | Version |
|---------|---------|
| Python  | 3       |


## Usage
After installation you'll be able the use the script, below is the most easy way to start the script.
```
python main.py
```
usage: main.py [-club CLUB NAME] [-cardNumber CARD_NUMBER] [-pwd PASSWORD] [-email EMAIL] [-date DATE] [-time TIME] [-cancellAll CANCEL]
```
 arguments:
  -h, --help                 show this help message and exit
  -club CLUB NAME            Name of the club , example "Libramont 24/7"
  -cardNumber CARD_NUMBER    card number
  -pwd PASSWORD              Password used for your Basic-Fit account
  -email EMAIL               E-mail used for your Basic-Fit account
  -date DATE                 Date for the reservations (yyyy-mm-dd) or 'D'   book for today or 'D+1' book for tomorrow
  -time TIME                 Time for the reservations (hh:mm)
  -cancellAll CANCEL         True or False - If true cancell all booked sessions
   -i INTERVAL  Interval in seconds before retrying again

```
