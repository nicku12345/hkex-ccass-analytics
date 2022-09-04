import React, { useState } from "react";
import { v4 as uuid } from 'uuid';
import { Stack } from "@mui/system";
import TransactionAnalyticsForm from "./TransactionAnalyticsForm";
// import { MOCK_transactionsAnalytics } from "../../fake/MOCK_transactionsAnalytics";
import TransactionAnalyticsTable from "./TransactionAnalyticsTable";
import { getTransactionAnalytics } from "../../util/hkexAnalyticsHelper";
import LoadingDialog from "../Shared/LoadingDialog";
import AlertDialog from "../Shared/AlertDialog";



function TransactionAnalyticsTab( props ) {
	const { rows, setRows } = props
	const [isLoading, setIsLoading] = useState(false)
	const [isAlert, setIsAlert] = useState(false)
	const [alertMsg, setAlertMsg] = useState("")

	const handleFormOnSubmit = async (stockCode, startDate, endDate, threshold) => {

		let tableRows = []
		// let api_data = MOCK_transactionsAnalytics
		setIsLoading(true)
		let [ api_success, api_data ] = await getTransactionAnalytics(stockCode, startDate, endDate, threshold)
		setIsLoading(false)

		if (!api_success)
		{
			setIsAlert(true)
			setAlertMsg("External API failed. This error happens may be because external server is under maintenance or unavailable. For now some dummy test data is being rendered.")
		}

		api_data.forEach((transactionAnalytics) => {
			const date = transactionAnalytics.Date.replace(" 00:00:00", "")

			transactionAnalytics.ParticipantTransactions.forEach((participantTransaction) => {
				tableRows.push({
					id: uuid(),
					Date: date,
					StockCode: stockCode,
					ParticipantId: participantTransaction.TransactionSummary.Participant.ParticipantId,
					ParticipantName: participantTransaction.TransactionSummary.Participant.ParticipantName,
					UnitDifference: participantTransaction.TransactionSummary.UnitDifference,
					WeightDifference: participantTransaction.TransactionSummary.WeightDifference,
					PossibleCounterparties: participantTransaction.PossibleCounterparties.map((opponentTransaction) => "<" + (opponentTransaction.Participant.ParticipantId + " " + opponentTransaction.Participant.ParticipantName).trim() + `(${opponentTransaction.UnitDifference.toLocaleString()})>`).join(", ")
				})
			})

		})

		setRows(tableRows)
	}

	return (
		<Stack spacing={5}>
			<LoadingDialog open={isLoading} />
			<AlertDialog isAlert={isAlert} alertMsg={alertMsg} setIsAlert={setIsAlert} setAlertMsg={setAlertMsg}/>
			<TransactionAnalyticsForm handleFormOnSubmit={handleFormOnSubmit}></TransactionAnalyticsForm>
			<TransactionAnalyticsTable rows={rows} />
		</Stack>
	)
}

export default TransactionAnalyticsTab;