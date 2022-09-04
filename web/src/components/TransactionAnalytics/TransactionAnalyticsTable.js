import * as React from 'react';
import Box from '@mui/material/Box';
import { DataGrid, GridToolbarQuickFilter, GridToolbarContainer } from '@mui/x-data-grid';
import { formatInteger, formatPercentage } from '../../util/numberFormatter'


function TransactionAnalyticsTableToolBar( props ) {
	return (
		<GridToolbarContainer>
			<Box marginLeft={2}>
				Quick Filter
			</Box>
			<Box marginLeft={2}>
				<GridToolbarQuickFilter />
			</Box>
		</GridToolbarContainer>
	);
}

function TransactionAnalyticsTable( props ) {
	const columns = [
		{
			field: "id", headerName: "id", width: 100, hide: true
		},
		{
			field: "Date", headerName: "Date", width: 120, 
		},
		{
			field: "StockCode", headerName: "Stock Code", width: 100
		},
		{
			field: "UnitDifference", headerName: "Unit Difference", width: 200, valueFormatter: formatInteger, align: "right"
		},
		{
			field: "WeightDifference", headerName: "Weight Difference", width: 200, valueFormatter: formatPercentage, align: "right"
		},
		{
			field: "ParticipantId", headerName: "Participant Id", width: 200
		},
		{
			field: "ParticipantName", headerName: "Participant Name", width: 600
		},
		{
			field: "PossibleCounterparties", headerName: "Possible Counterparties: A List of <ID Name(UnitDifference)>", width: 1000
		},
	]

	return (
		<Box sx={{ height: '1000px', width: '100%' }}>
			<DataGrid
				rows={props.rows}	columns={columns} pageSize={100} rowsPerPageOptions={[100]} disableSelectionOnClick	experimentalFeatures={{ newEditingApi: true }}
				components={{ Toolbar: TransactionAnalyticsTableToolBar }}
			/>
		</Box>
	)
}

export default TransactionAnalyticsTable;