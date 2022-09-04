import axios from "axios"
import { MOCK_trendAnalytics } from '../fake/MOCK_trendAnalytics'
import { MOCK_transactionsAnalytics } from '../fake/MOCK_transactionsAnalytics'

function getHost(env) {
	return "http://127.0.0.1:5000"
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