import * as React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import { Button, DialogContent, Stack } from '@mui/material';


function AlertDialog( props ) {
	const { isAlert, alertMsg, setIsAlert, setAlertMsg } = props;

	const handleButtonOnClick = () => {
		setIsAlert(false)
		setAlertMsg("")
	}

	return (
		<Dialog open={isAlert}>
			<DialogTitle>Error</DialogTitle>
			<DialogContent>
				{alertMsg}
			</DialogContent>
			<Stack alignItems="center" justifyContent="center" margin={2}>
				<Button onClick={handleButtonOnClick} variant="contained">
					Close
				</Button>
			</Stack>
		</Dialog>
	);
}

export default AlertDialog