
export const formatInteger = (params) => {
	if (params.value == null) {
		return '';
	}

	const valueFormatted = Number(params.value).toLocaleString();
	return `${valueFormatted}`;
};

export const formatPercentage = (params) => {
	if (params.value == null) {
		return '';
	}

	const valueFormatted = Number(params.value * 100).toLocaleString();
	return `${valueFormatted}%`;
};