import datetime
from basicFit.basicfitSession import basicfitSession
from datetime import timedelta, date
import argparse


MAX_RESERVATIONS=2

def main():

    #datePlus1 = datetime.now() + timedelta(days=1)
    parser = argparse.ArgumentParser()
    # Add arguments
    parser.add_argument('-email', dest="email", help="E-mail used for your Basic-Fit account")
    parser.add_argument('-pwd', dest="password", help="Password used for your Basic-Fit account")
    parser.add_argument('-cardNumber', dest="cardNumber", help="cardnumber")

    parser.add_argument('-date', dest="date", help="Date for the reservations (yyyy-mm-dd)")
    parser.add_argument('-time', dest="time", help="Time for the reservations (hh:mm)")
    parser.add_argument('-club', dest="club", help="club Name")
    parser.add_argument('-cancellAll', dest="cancellAll", help="Cancell all bookings")

    args = parser.parse_args()

    date=None
    if args.date == 'D+1':
        date=(datetime.datetime.now()+ timedelta(days=1)).strftime("%Y-%m-%d")
    elif args.date == 'D':
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        date = args.date

    basicFit = basicfitSession(args.email, args.password, args.cardNumber)

    visitList=basicFit.getVisits()
    print(f"Total Visits : {len(visitList)}")
    for visit in visitList:
        print(visit)
    print("\n")

    print("Requested Club :")
    print(basicFit.getClub(args.club))
    print("\n")


    openReservations=basicFit.getOpenReservations()

    if(args.cancellAll):
        cancelAll = bool(args.cancellAll=="True")

    if not cancelAll and len(openReservations)<MAX_RESERVATIONS:
        print(f"Try booking session @{args.club} on {date} {args.time}")
        response=basicFit.bookAt(date, args.time ,args.club)
        print(response)
    elif cancelAll:
        print(f"Try cancelling session {openReservations}")
        response=basicFit.cancelBookings(openReservations)
        print(response)
    else:
        print(f"session has been already planned: {openReservations}")


main()