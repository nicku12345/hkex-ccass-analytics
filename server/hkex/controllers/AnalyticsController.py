import json
from datetime import date
from flask import Blueprint, Response, request
from hkex.managers.AnalyticsManager import AnalyticsManager


class AnalyticsController:

    blueprint = Blueprint("analytics", __name__, url_prefix="/api/analytics")

    @staticmethod
    @blueprint.route("/trends", methods=["GET"])
    def GetTrendAnalytics():

        args = request.args

        try:
            stockCode = args.get("stockCode")
            startDate = args.get("startDate")
            endDate = args.get("endDate")

            startDate = date(*map(int, startDate.split("-")))
            endDate = date(*map(int, endDate.split("-")))
        except:
            return "Invalid param", 400

        mgr = AnalyticsManager()

        try:
            trendAnalytics = mgr.GetTrendAnalytics(stockCode, startDate, endDate)
        except BaseException as err:
            return f"Server error: {err}", 500

        res = [t.Serialize() for t in trendAnalytics]

        return Response(json.dumps(res), mimetype="application/json")

    @staticmethod
    @blueprint.route("/transactions", methods=["GET"])
    def GetTransactionAnalytics():

        args = request.args

        try:
            stockCode = args.get("stockCode")
            startDate = args.get("startDate")
            endDate = args.get("endDate")
            threshold = float(args.get("threshold"))

            startDate = date(*map(int, startDate.split("-")))
            endDate = date(*map(int, endDate.split("-")))
        except:
            return "Invalid param", 400

        mgr = AnalyticsManager()

        try:
            transactionAnalytics = mgr.GetTransactionAnalytics(stockCode, startDate, endDate, threshold)
        except BaseException as err:
            return f"Server error: {err}", 500

        res = [t.Serialize() for t in transactionAnalytics]

        return Response(json.dumps(res), mimetype="application/json")


