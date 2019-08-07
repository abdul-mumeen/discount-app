import React from 'react';
import { Link } from 'react-router-dom';
import { fetchDiscountInfo } from '../../actions';

/**
 *
 * @class DiscountInfo
 * @extends {React.Component}
 */
class DiscountInfo extends React.Component {
	state = {
		discount: {}
	};

	async componentDidMount() {
		const {
			match: { params }
		} = this.props;
		const data = await fetchDiscountInfo(params.discountId);
		this.setState({ discount: data });
	}

	render() {
		const { discount } = this.state;
		return (
			<div>
				<div>
					<Link to={`/discounts/${discount.id}`}>{discount.code}</Link>
				</div>
				<div>{discount.type_id}</div>
				<div>{discount.value}</div>
				<div>{discount.min_apply_value}</div>
				<div>{discount.category_id}</div>
				<div>{discount.modified_at}</div>
			</div>
		);
	}
}

export default DiscountInfo;
