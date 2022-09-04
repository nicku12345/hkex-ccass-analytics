import * as React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import { DialogContent, Stack } from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';


function LoadingDialog( props ) {
	const { open } = props;

	return (
		<Dialog open={open}>
			<DialogTitle>Loading...</DialogTitle>
			<Stack alignItems="center" justifyContent="center">
				<CircularProgress />
			</Stack>
			<DialogContent>
				Note: 
				It may a few minutes to collect data analytics. 
				Please consider query for a smaller date range, e.g. 1 month or 1 week.
				Because HKEX only offers data within the most recent year, old data may be unavailable.
			</DialogContent>
		</Dialog>
	);
}

export default LoadingDialog