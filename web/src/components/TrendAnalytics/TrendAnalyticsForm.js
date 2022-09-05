import React, { useState } from "react";
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import { getYesterdayString } from "../../util/datetime";

function TrendAnalyticsForm( props ) {
	const stockCodeDefaultValue = "00001"
	const startDateDefaultValue = getYesterdayString ()
	const endDateDefaultValue = getYesterdayString ()

	const [stockCode, setStockCode] = useState(stockCodeDefaultValue)
	const [startDate, setStartDate] = useState(startDateDefaultValue)
	const [endDate, setEndDate] = useState(endDateDefaultValue)

	const handleStockCodeOnInput = (e) => setStockCode(e.target.value)
	const handleStartDateOnInput = (e) => setStartDate(e.target.value)
	const handleEndDateOnInput = (e) => setEndDate(e.target.value)

	const handleButtonOnClick = () => {
		if (stockCode.length === 0 || startDate.length === 0 || endDate.length === 0)
		{
			console.log("Invalid param")
			return;
		}

		props.handleFormOnSubmit(stockCode, startDate, endDate);
	}

	return (
		<Stack component="form" noValidate spacing={3} justifyContent="center" alignItems="center" direction="row">
			<TextField
				id="stockCode" label="Stock Code" type="text" sx={{ width: 220 }} InputLabelProps={{ shrink: true, }}
				onInput={handleStockCodeOnInput}
				defaultValue={stockCodeDefaultValue}
			/>
			<TextField
				id="startDate" label="Start Date" type="date" sx={{ width: 220 }} InputLabelProps={{ shrink: true, }}
				onInput={handleStartDateOnInput}
				defaultValue={startDateDefaultValue}
			/>
			<TextField
				id="endDate" label="End Date" type="date" sx={{ width: 220 }} InputLabelProps={{ shrink: true, }}
				onInput={handleEndDateOnInput}
				defaultValue={endDateDefaultValue}
			/>
			<Button onClick={handleButtonOnClick} sx={{ width: 220 }} variant="contained">
				Submit
			</Button>
		</Stack>
  );
}

export default TrendAnalyticsForm;
