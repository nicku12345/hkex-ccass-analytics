import React, { useState } from "react";
import TrendAnalyticsForm from './TrendAnalyticsForm';
import TrendAnalyticsTable from './TrendAnalyticsTable';
import TrendAnalyticsChart from "./TrendAnalyticsChart";
import { v4 as uuid } from 'uuid';
// import { MOCK_trendAnalytics } from '../../fake/MOCK_trendAnalytics';
import { Stack } from "@mui/system";
import { getTrendAnalytics } from "../../util/hkexAnalyticsHelper";
import LoadingDialog from "../Shared/LoadingDialog";
import AlertDialog from "../Shared/AlertDialog";



function TrendAnalyticsTab( props ) {
	const { rows, stockCode, bars, participants, setRows, setStockCode, setBarsAndParticipants } = props
	const [isLoading, setIsLoading] = useState(false)
	const [isAlert, setIsAlert] = useState(false)
	const [alertMsg, setAlertMsg] = useState("")


	const handleFormOnSubmit = async (stockCode, startDate, endDate) => {
		setStockCode(stockCode)

		let tableRows = []
		let chartBars = []
		let chartParticipants = []
		let participantNames = new Set()

		setIsLoading(true)
		let [ api_success, api_data ] = await getTrendAnalytics(stockCode, startDate, endDate)
		setIsLoading(false)

		if (!api_success)
		{
			setIsAlert(true)
			setAlertMsg("External API failed. This error happens may be because external server is under maintenance or unavailable. For now some dummy test data is being rendered.")
		}

		api_data.forEach((trendAnalytics) => {
			const date = trendAnalytics.Date.replace(" 00:00:00", "")
			const bar = { Date: date }
			let totalShareholding = trendAnalytics.TotalShareHolding.Shareholding

			trendAnalytics.TopParticipants.forEach((participant) => {
				tableRows.push({
					id: uuid(),
					StockCode: participant.StockCode,
					ParticipantId: participant.ParticipantId,
					ParticipantName: participant.ParticipantName,
					Shareholding: participant.ShareHolding,
					Date: date,
					Weight: participant.ShareHolding / totalShareholding,
				})
				
				if (!participantNames.has(participant.ParticipantName))
				{
					participantNames.add(participant.ParticipantName)
					chartParticipants.push({
						ParticipantName: participant.ParticipantName
					})
				}
				bar[participant.ParticipantName] = participant.ShareHolding / totalShareholding

			})

			chartBars.push(bar)
		})

		setBarsAndParticipants([chartBars, chartParticipants])
		setRows(tableRows)
	}

	return (
		<Stack spacing={5}>
			<LoadingDialog open={isLoading} />
			<AlertDialog isAlert={isAlert} alertMsg={alertMsg} setIsAlert={setIsAlert} setAlertMsg={setAlertMsg}/>
			<TrendAnalyticsForm handleFormOnSubmit={handleFormOnSubmit}></TrendAnalyticsForm>
			<TrendAnalyticsChart stockCode={stockCode} bars={bars} participants={participants}></TrendAnalyticsChart>
			<TrendAnalyticsTable rows={rows}></TrendAnalyticsTable>
		</Stack>
	)
}

export default TrendAnalyticsTab