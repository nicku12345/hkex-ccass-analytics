import json
from datetime import date
from flask import Blueprint, Response, request
from hkex.managers.ResourcesManager import ResourcesManager


class ResourcesController:

    blueprint = Blueprint("resources", __name__, url_prefix="/api/resources")

    @staticmethod
    @blueprint.route("/", methods=["GET"])
    def GetShareHoldingsAndParticipants():

        args = request.args

        try:
            stockCode = args.get("stockCode")
            startDate = args.get("startDate")
            endDate = args.get("endDate")

            startDate = date(*map(int, startDate.split("-")))
            endDate = date(*map(int, endDate.split("-")))
        except:
            return "Invalid param", 400

        mgr = ResourcesManager()

        shareholdings, participants = mgr.GetParticipantsAndShareHoldings(stockCode, startDate, endDate)

        response = {
            "shareholdings": [shareholding.Serialize() for shareholding in shareholdings],
            "participants": [participant.Serialize() for participant in participants],
        }

        return Response(json.dumps(response), mimetype="application/json")
