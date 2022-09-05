import React, { useState } from "react";
import TrendAnalyticsTab from './TrendAnalytics/TrendAnalyticsTab';
import { Button, Stack } from '@mui/material';
import TransactionAnalyticsTab from "./TransactionAnalytics/TransactionAnalyticsTab";


function Dashboard() {
	//const [[trendRows, trendStockCode, trendBars, trendParticipants], setTrendAnalyticsTabProps] = useState([[], "", [], []])
	const [trendRows, setTrendRows] = useState([])
	const [trendStockCode, setTrendStockCode] = useState("")
	const [trendBars, setTrendBars] = useState([])
	const [trendParticipants, setTrendParticipants] = useState([])
	const [trendAllParticipants, setTrendAllParticipants] = useState([])

	const [transactionRows, setTransactionRows] = useState([])

	const tab = {
		TrendAnalytics: 0,
		TransactionAnalytics: 1
	}

	const [currentTab, setCurrentTab] = useState(tab.TrendAnalytics)
	const [trendAnalyticsBtnVariant, setTrendAnalyticsBtnVariant] = useState("contained")
	const [transactionAnalyticsBtnVariant, setTransactionAnalyticsBtnVariant] = useState("outlined")

	const showTrendAnalytics = () => {
		setCurrentTab(tab.TrendAnalytics)
		setTrendAnalyticsBtnVariant("contained")
		setTransactionAnalyticsBtnVariant("outlined")
	}

	const showTransactionAnalytics = () => {
		setCurrentTab(tab.TransactionAnalytics)
		setTrendAnalyticsBtnVariant("outlined")
		setTransactionAnalyticsBtnVariant("contained")
	}

	return (
		<Stack spacing={2}>
			<Stack direction="row" spacing={2}>
				<Button onClick={showTrendAnalytics} variant={trendAnalyticsBtnVariant}>
					Trend Analytics
				</Button>
				<Button onClick={showTransactionAnalytics} variant={transactionAnalyticsBtnVariant}>
					Transaction Analytics
				</Button>
			</Stack>
			{
				currentTab === tab.TrendAnalytics
				?
				<TrendAnalyticsTab 
					rows={trendRows} 
					stockCode={trendStockCode} 
					bars={trendBars} 
					participants={trendParticipants}
					setRows={setTrendRows}
					setStockCode={setTrendStockCode}
					setBars={setTrendBars}
					setParticipants={setTrendParticipants}
					allParticipants={trendAllParticipants}
					setAllParticipants={setTrendAllParticipants}
				/>
				:
				<TransactionAnalyticsTab
					rows={transactionRows}
					setRows={setTransactionRows}
				/>
			}
		</Stack>
	);
}

export default Dashboard;