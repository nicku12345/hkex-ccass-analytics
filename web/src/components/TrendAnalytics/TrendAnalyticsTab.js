import React, { useState } from "react";
import TrendAnalyticsForm from './TrendAnalyticsForm';
import TrendAnalyticsTable from './TrendAnalyticsTable';
import TrendAnalyticsChart from "./TrendAnalyticsChart";
import { v4 as uuid } from 'uuid';
// import { MOCK_trendAnalytics } from '../../fake/MOCK_trendAnalytics';
import { Stack } from "@mui/system";
import { checkStockCodeValidity, getTrendAnalytics } from "../../util/hkexAnalyticsHelper";
import LoadingDialog from "../Shared/LoadingDialog";
import AlertDialog from "../Shared/AlertDialog";



function TrendAnalyticsTab( props ) {
	const { rows, stockCode, bars, participants, setRows, setStockCode, setBars, setParticipants, allParticipants, setAllParticipants } = props
	const [isLoading, setIsLoading] = useState(false)
	const [isAlert, setIsAlert] = useState(false)
	const [alertMsg, setAlertMsg] = useState("")


	const handleFormOnSubmit = async (stockCode, startDate, endDate) => {
		const [ stockCodeValid, errMsg ] = checkStockCodeValidity(stockCode)
		if (!stockCodeValid)
		{
			setIsAlert(true)
			setAlertMsg(errMsg)
			return
		}

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
			setAlertMsg("External API failed. This error may happen because (1) the requested stock code does not exist or is not available for query; (2) external server is under maintenance; or (3) the stock data on requested date range is empty. Please consider querying for a smaller date range. For now some dummy test data is being rendered.")
			setStockCode("(Fake) 00001 ")
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
					chartParticipants.push(participant.ParticipantName)
				}
				bar[participant.ParticipantName] = participant.ShareHolding / totalShareholding

			})

			chartBars.push(bar)
		})

		setBars(chartBars)
		setParticipants(chartParticipants)
		setAllParticipants(chartParticipants)
		setRows(tableRows)
	}

	return (
		<Stack spacing={5}>
			<LoadingDialog open={isLoading} />
			<AlertDialog isAlert={isAlert} alertMsg={alertMsg} setIsAlert={setIsAlert}/>
			<TrendAnalyticsForm handleFormOnSubmit={handleFormOnSubmit}></TrendAnalyticsForm>
			<TrendAnalyticsChart stockCode={stockCode} bars={bars} participants={participants} allParticipants={allParticipants} setAllParticipants={setAllParticipants} setParticipants={setParticipants}></TrendAnalyticsChart>
			<TrendAnalyticsTable rows={rows}></TrendAnalyticsTable>
		</Stack>
	)
}

export default TrendAnalyticsTab