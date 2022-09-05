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

export function getTrendAnalytics(stockCode, startDate, endDate) {
	const url = getHost() + `/api/analytics/trends?stockCode=${stockCode}&startDate=${startDate}&endDate=${endDate}`
	return axios.get(url).then((res) => {
		return [ true, res.data ]
	}).catch((err) => {
		return [ false, MOCK_trendAnalytics ]
	})
}

export function getTransactionAnalytics(stockCode, startDate, endDate, threshold) {
	const url = getHost() + `/api/analytics/transactions?stockCode=${stockCode}&startDate=${startDate}&endDate=${endDate}&threshold=${threshold}`
	return axios.get(url).then((res) => {
		return [ true, res.data ]
	}).catch((err) => {
		return [ false, MOCK_transactionsAnalytics ]
	})
}