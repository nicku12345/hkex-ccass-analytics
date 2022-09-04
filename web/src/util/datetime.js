
export function getTodateString() {
	let today = new Date()
	const yyyy = `${today.getFullYear()}`
	// month is 0-indexed
	const mm = today.getMonth() >= 9 ? `${1 + today.getMonth()}` : `0${1 + today.getMonth()}`
	const dd = today.getDate() >= 10 ? `${today.getDate()}` : `0${today.getDate()}`

	return yyyy + "-" + mm + "-" + dd;
}