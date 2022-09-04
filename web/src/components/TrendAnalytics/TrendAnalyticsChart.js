import React from 'react';
import { v4 as uuid } from 'uuid';
import { Chart, Series, ArgumentAxis, CommonSeriesSettings, Title, ValueAxis } from 'devextreme-react/chart';

 
function TrendAnalyticsChart( props ) {
 
	return (
		props.participants.length > 0
		?
		<Chart dataSource={ props.bars }>
			<Title text={props.stockCode.length > 0 ? `Top shareholding participants of ${props.stockCode}` : ""}/>
			<CommonSeriesSettings argumentField="Date" valueField="Weight" type="stackedBar"/>
			{
				props.participants.map((p) => <Series key={uuid()} valueField={p.ParticipantName} name={p.ParticipantName}/>)
			}
			<ValueAxis title="Weight"/>
			<ArgumentAxis />
		</Chart>
		:
		<></>
	);
}
export default TrendAnalyticsChart;