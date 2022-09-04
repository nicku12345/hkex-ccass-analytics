import * as React from 'react';
import Box from '@mui/material/Box';
import { DataGrid, GridToolbarQuickFilter, GridToolbarContainer } from '@mui/x-data-grid';
import { formatInteger, formatPercentage } from '../../util/numberFormatter';

function TrendAnalyticsTableToolBar( props ) {
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

function TrendAnalyticsTable( props ) {
	const columns = [
		{
			field: "id", headerName: "id", width: 100, hide: true
		},
		{
			field: "Date", headerName: "Date", width: 120
		},
		{
			field: "StockCode", headerName: "Stock Code", width: 100
		},
		{
			field: "Shareholding", headerName: "Shareholding", width: 200, valueFormatter: formatInteger, align: "right"
		},
		{
			field: "Weight", headerName: "Weight", width: 100, valueFormatter: formatPercentage, align: "right"
		},
		{
			field: "ParticipantId", headerName: "Participant Id", width: 200
		},
		{
			field: "ParticipantName", headerName: "Participant Name", width: 600
		},
	];

	return (
		<Box sx={{ height: '1000px', width: '100%' }}>
			<DataGrid
				rows={props.rows}	columns={columns} pageSize={100} rowsPerPageOptions={[100]} disableSelectionOnClick	experimentalFeatures={{ newEditingApi: true }}
				components={{ Toolbar: TrendAnalyticsTableToolBar }}
			/>
		</Box>
	);
}

export default TrendAnalyticsTable;