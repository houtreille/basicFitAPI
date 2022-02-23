from json import dumps
import requests
from datetime import datetime

class basicfitSession:

    HOST = 'my.basic-fit.com'
    HEADER = {
        'Host': 'my.basic-fit.com',
        'Connection':'keep-alive',
        'Accept-Language': 'fr-BE,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'mbfLoginHeadVForm': 'jk#Bea201',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    HEADER_VISITS = {
        'Host': 'my.basic-fit.com',
        'Connection': 'keep-alive',
        'content-type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'mbf-rct-app-api-2-caller': 'true',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'fr-BE,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
    }


    def __init__(self, user, password, cardNumber):
        self.credentials= dumps({"email":user,"password":password,"cardNumber":cardNumber})
        self.getSession()

    def getSession(self):
        self.session = requests.Session()
        response = self.session.post("https://"+basicfitSession.HOST+"/authentication/login", data=self.credentials, headers=basicfitSession.HEADER,verify=False)

        if response.status_code != 200:
            raise Exception("Unable to authenticate at Basic-Fit")


    def getVisits(self):
        response= self.session.get("https://"+basicfitSession.HOST+"/member/visits", headers=basicfitSession.HEADER_VISITS,verify=False)
        return response.json()

    def getAvailability(self, dayTime, clubId):
        data=dumps({"dateTime": dayTime, "clubId": clubId})
        response = self.session.post("https://" + basicfitSession.HOST + "/door-policy/get-availability", data=data,headers=basicfitSession.HEADER_VISITS, verify=False)
        return response.json()


    def getClub(self, clubName):
        clubs = self.session.get("https://" + basicfitSession.HOST + "/door-policy/get-clubs", data={},headers=basicfitSession.HEADER_VISITS, verify=False)
        for club in clubs.json():
            if club["name"]==clubName:
                return club


    def getOpenReservations(self):
        bookings=self.session.get("https://" + basicfitSession.HOST + "/door-policy/get-open-reservation", data={},headers=basicfitSession.HEADER_VISITS, verify=False)
        return bookings.json()["data"]


    def bookAt(self, dayTime, dateTime, clubName):

        dictClub=self.getClub(clubName)
        dictPolicyId=None

        requestedDate=datetime.strptime(dayTime+' '+dateTime,'%Y-%m-%d %H:%M')
        policyIds=self.getAvailability(dayTime, dictClub["id"])



        for policyId in policyIds:
            doorPolicyId=policyId["doorPolicyId"]
            startDateTime = datetime.strptime(policyId["startDateTime"],'%Y-%m-%dT%H:%M:%S.%f')
            openForReservation=bool(policyId["openForReservation"])

            if openForReservation and startDateTime==requestedDate and not dictPolicyId:
                dictPolicyId=policyId



        dataPolicy={"doorPolicy":dictPolicyId}
        dataPolicy.update({"clubOfChoice": dictClub})
        dataPolicy.update( {"duration":"90"})
        bookingData=dumps(dataPolicy)

        response=self.session.post("https://" + basicfitSession.HOST + "/door-policy/book-door-policy", data=bookingData,headers=basicfitSession.HEADER_VISITS, verify=False)

        if response.status_code != 200:
            raise Exception("Unable to authenticate at Basic-Fit")
        else:
            return response.json()


    def cancelBookings(self, doorPolicyIdToCancel):

        for cancellation in doorPolicyIdToCancel:
            data = dumps({"doorPolicyPeopleId": cancellation["doorPolicyPeopleId"]}) #"361a6154-9155-4e04-9017-a9c1ef9ef995"
            response = self.session.post("https://" + basicfitSession.HOST + "/door-policy/cancel-door-policy", data=data, headers=basicfitSession.HEADER_VISITS, verify=False)
