from __future__ import annotations
import re
from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
from hkex.managers.BaseManager import BaseManager
from hkex.database.repositories.ParticipantsRepository import ParticipantsRepository
from hkex.database.repositories.ShareHoldingsRepository import ShareHoldingsRepository
from hkex.database.models.ShareHolding import ShareHolding
from hkex.database.models.Participant import Participant


class ResourcesManager(BaseManager):

    def __init__(self):
        super().__init__()
        self._participantsRepo = ParticipantsRepository()
        self._shareholdingRepo = ShareHoldingsRepository()

    def GetParticipantsAndShareHoldings(self, stockCode: str, startDate: date, endDate: date) -> tuple[list[ShareHolding], list[Participant]]:
        """
        Gets participants and shareholdings for given stockCode and daterange.

        First query database. If there are missing dates, go to fetch external website.

        :param stockCode:
        :param startDate:
        :param endDate:
        :return:
        """
        self._logger.info(f"Get participants and shareholdings for {stockCode} from {startDate} to {endDate}")

        existingParticipants = self._participantsRepo.GetParticipantsByStockCodeAndDates(stockCode, startDate, endDate)
        existingShareHoldings = self._shareholdingRepo.GetShareHoldingByStockCodeAndDates(stockCode, startDate, endDate)
        existingDates = set()
        missingDates = []

        for shareholding in existingShareHoldings:
            yy = shareholding.Date.year
            mm = shareholding.Date.month
            dd = shareholding.Date.day
            existingDates.add((yy,mm,dd))

        curDate = startDate
        while curDate <= endDate:
            if (curDate.year, curDate.month, curDate.day) not in existingDates:
                missingDates.append(curDate)
            curDate = curDate + timedelta(days=1)

        fetchedShareHoldings, fetchedParticipants = self.GetParticipantsAndShareHoldingsForMissingDates(stockCode, missingDates)

        return existingShareHoldings + fetchedShareHoldings, existingParticipants + fetchedParticipants

    def GetParticipantsAndShareHoldingsForMissingDates(self, stockCode: str, missingDates: list[date]):
        if missingDates:
            self._logger.info(f"Get Participants and Shareholdings for {len(missingDates)} missing dates.")

        shareHoldings = []
        participants = []

        for missingDate in missingDates:
            shareHoldingsForDate, participantsForDate = self.FetchParticipantsAndShareHoldings(stockCode, missingDate)

            shareHoldings += shareHoldingsForDate
            participants += participantsForDate

        self._participantsRepo.AddParticipants(participants)
        self._shareholdingRepo.AddShareHoldings(shareHoldings)

        return shareHoldings, participants

    def FetchParticipantsAndShareHoldings(self, stockCode: str, singleDate: date):
        self._logger.info(f"Fetching external API. StockCode={stockCode}, Date={singleDate}")

        yyyy = str(singleDate.year)
        mm = str(singleDate.month)
        dd = str(singleDate.day)

        if len(mm) == 1: mm = "0" + mm
        if len(dd) == 1: dd = "0" + dd

        url = "https://www3.hkexnews.hk/sdw/search/searchsdw.aspx"
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = {
            "__EVENTTARGET": "btnSearch",
            "sortBy": "shareholding",
            "sortDirection": "desc",
            "txtShareholdingDate": f"{yyyy}/{mm}/{dd}",
            "txtStockCode": stockCode,
        }

        res = requests.post(url, headers=headers, data=data)
        soup = BeautifulSoup(res.text, "html.parser")

        # check whether external server is under maintenance
        maintenanceTag = soup.find(class_="ccass-search-maintenance")
        if maintenanceTag is not None:
            self._logger.error(f"External server is under maintenance. Skipped fetching for stockCode={stockCode}")
            raise Exception(f"External server is under maintenance. Full response from external API: "
                            f"{soup.prettify()}")

        searchRemarks = soup.find(class_="ccass-search-remarks")
        if searchRemarks is None:
            self._logger.warn(f"No data fetched from site. stockCode={stockCode}, date={yyyy}-{mm}-{dd}")
            raise Exception(f"External server could not provide data for {stockCode} on {yyyy}-{mm}-{dd}")

        tag = soup.find(class_="ccass-search-remarks").find(class_="summary-value")
        totalShare = int(tag.string.replace(",",""))

        participantIds = soup.find_all("td", class_="col-participant-id")
        participantIds = [tag.find(class_="mobile-list-body").string for tag in participantIds]

        participantNames = soup.find_all("td", class_="col-participant-name")
        participantNames = [tag.find(class_="mobile-list-body").string for tag in participantNames]

        shareHoldings = soup.find_all("td", class_=re.compile("(?!col-shareholding-percent)(col-shareholding)"))
        shareHoldings = [int(tag.find(class_="mobile-list-body").string.replace(",","")) for tag in shareHoldings]

        stockShareHoldings = [ ShareHolding(StockCode = stockCode, Date = singleDate, ShareHolding = totalShare) ]
        participants = []

        if len(participantIds)!=len(participantNames) or len(participantIds)!=len(shareHoldings):
            self._logger.error(f"Fetched ParticipantIds, ParticipantNames, ShareHoldings have different sizes. "
                               f"({len(participantIds)}, {len(participantNames)}, {len(shareHoldings)})")

        for participantId, participantName, shareholding in zip(participantIds, participantNames, shareHoldings):
            participants.append(Participant(
                StockCode = stockCode,
                Date = singleDate,
                Shareholding = shareholding,
                ParticipantId = participantId,
                ParticipantName = participantName
            ))

        return stockShareHoldings, participants


