import { discountAppServer } from './helpers/services';

export const fetchAllDiscounts = async () => {
	try {
		const response = await discountAppServer.get('/discounts');
		return response.data;
	} catch (err) {
		throw new Error(err.message);
	}
};

export const fetchDiscountInfo = async discountId => {
	try {
		const response = await discountAppServer.get(`/discounts/${discountId}`);
		return response.data;
	} catch (err) {
		throw new Error(err.message);
	}
};

export const deleteDiscount = async discountId => {
	try {
		const response = await discountAppServer.delete(`/discounts/${discountId}`);
		return response.data;
	} catch (err) {
		throw new Error(err.message);
	}
};

export const createDiscount = async (
	typeId,
	value,
	minApplyValue,
	categoryId
) => {
	const payload = {
		type_id: typeId,
		value,
		min_apply_value: minApplyValue,
		category_id: categoryId
	};
	try {
		const response = await discountAppServer.post('/discounts/', payload);
		return response.data;
	} catch (err) {
		throw new Error(err.message);
	}
};
