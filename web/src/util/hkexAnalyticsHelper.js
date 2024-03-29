import axios from "axios"
import { MOCK_trendAnalytics } from '../fake/MOCK_trendAnalytics'
import { MOCK_transactionsAnalytics } from '../fake/MOCK_transactionsAnalytics'

function getHost() {
	switch (process.env.REACT_APP_NODE_ENV) {
		case "production":
			return "http://ec2-18-237-117-90.us-west-2.compute.amazonaws.com:5000"
		default:
			return "http://localhost:5000"
	}
}

export function checkStockCodeValidity(stockCode) {
	const disallowedCharacters = "~!@#$%^&*()"
	if (stockCode.length === 0)
		return [ false, "Stock Code is empty" ]
	
	for (let i=0; i<stockCode.length; i++) { 
		if (disallowedCharacters.includes(stockCode[i]))
			return [ false, "Invalid Stock Code" ]
	}

	return [ true, "" ]
}

export function getTrendAnalytics(stockCode, startDate, endDate) {
	const url = getHost() + `/api/analytics/trends`
	const params = {
		stockCode: stockCode,
		startDate: startDate,
		endDate: endDate
	}

	return axios.get(url, { params }).then((res) => {
		return [ true, res.data ]
	}).catch((err) => {
		return [ false, MOCK_trendAnalytics ]
	})
}

export function getTransactionAnalytics(stockCode, startDate, endDate, threshold) {
	const url = getHost() + `/api/analytics/transactions`
	const params = {
		stockCode: stockCode,
		startDate: startDate,
		endDate: endDate,
		threshold: threshold
	}

	return axios.get(url, { params }).then((res) => {
		return [ true, res.data ]
	}).catch((err) => {
		return [ false, MOCK_transactionsAnalytics ]
	})
}