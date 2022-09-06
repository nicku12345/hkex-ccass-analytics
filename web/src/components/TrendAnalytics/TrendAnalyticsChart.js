import React, { useState } from 'react';
import { v4 as uuid } from 'uuid';
import { Chart, Series, ArgumentAxis, CommonSeriesSettings, Title, ValueAxis } from 'devextreme-react/chart';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import { Box, Button, Stack } from '@mui/material';


function TrendAnalyticsChartFilterFormGroup( props ) {
	const { allParticipants, participants, setParticipants } = props
	const [open, setOpen] = useState(false)

	const getHandleCheckBoxOnChange = (participantName) => {
		return () => {
			const newParticipants = []
			participants.forEach((x) => {
				if (x !== participantName)
				{
					newParticipants.push(x)
				}
			})

			if (newParticipants.length === participants.length)
			{
				newParticipants.push(participantName)
			}

			setParticipants(newParticipants)
		}
	}

	return (
		<Box
			sx={{
				display: 'grid',
				bgcolor: (theme) =>
					theme.palette.mode === 'dark' ? '#101010' : 'grey.100',
				color: (theme) =>
					theme.palette.mode === 'dark' ? 'grey.300' : 'grey.800',
				border: '1px solid',
				borderColor: (theme) =>
					theme.palette.mode === 'dark' ? 'grey.800' : 'grey.300',
				p: 1,
				borderRadius: 2,
				gap:2,
				maxWidth:"500px",
				marginLeft: "auto",
				marginRight: "auto"
			}}
		>
			<Button variant="contained" onClick={() => setOpen(!open)}>{(open ? "Close" : "Open") + " Chart Filter"}</Button>
			{
				open
				?
				<FormGroup>
					{
						allParticipants.map((participantName) => 
							<FormControlLabel key={`FCL-${participantName}`} control={<Checkbox onChange={getHandleCheckBoxOnChange(participantName)} checked={participants.includes(participantName)}/>} label={participantName}/>
						)
					}
				</FormGroup>
				:
				null
			}
		</Box>
	)
}
 
function TrendAnalyticsChart( props ) {
	const { participants, setParticipants, allParticipants, bars, stockCode } = props
 
	return (
		allParticipants.length > 0
		?
		<Stack spacing={2}>
			<Box>
				<Chart dataSource={ bars }>
					<Title text={stockCode.length > 0 ? `Top shareholding participants of ${stockCode}` : ""}/>
					<CommonSeriesSettings argumentField="Date" valueField="Weight" type="line"/>
					{
						participants.map((participantName) => <Series key={uuid()} valueField={participantName} name={participantName}/>)
					}
					<ValueAxis title="Weight"/>
					<ArgumentAxis />
				</Chart>
			</Box>
			<Box>
				<TrendAnalyticsChartFilterFormGroup 
					allParticipants={allParticipants}
					participants={participants}
					setParticipants={setParticipants}
				/>
			</Box>
		</Stack>
		:
		null
	);
}
export default TrendAnalyticsChart;