import axios from 'axios';

export const discountAppServer = axios.create({
	baseURL: 'http://localhost:5000/api/',
	headers: {
		post: {
			'Access-Control-Allow-Origin': '*'
		}
	}
});
