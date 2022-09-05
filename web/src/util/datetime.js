
export function getYesterdayString() {
	let yesterday = new Date()
	yesterday.setDate(yesterday.getDate() - 1)

	const yyyy = `${yesterday.getFullYear()}`
	// month is 0-indexed
	const mm = yesterday.getMonth() >= 9 ? `${1 + yesterday.getMonth()}` : `0${1 + yesterday.getMonth()}`
	const dd = yesterday.getDate() >= 10 ? `${yesterday.getDate()}` : `0${yesterday.getDate()}`

	return yyyy + "-" + mm + "-" + dd;
}