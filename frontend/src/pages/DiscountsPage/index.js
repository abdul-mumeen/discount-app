import React from 'react';
import { Link } from 'react-router-dom';
import { fetchAllDiscounts } from '../../actions';

/**
 *
 * @class DiscountsPage
 * @extends {React.Component}
 */
class DiscountsPage extends React.Component {
	state = {
		discounts: []
	};

	async componentDidMount() {
		const data = await fetchAllDiscounts();
		this.setState({ discounts: data.discounts });
	}

	render() {
		const { discounts } = this.state;
		const TOTAL_PER_PAGE = 10;
		const startIndex = 0;
		return (
			<div>
				{discounts
					.slice(startIndex, startIndex + TOTAL_PER_PAGE)
					.map(discount => (
						<div key={discount.id}>
							<div>
								<Link to={`/discounts/${discount.id}`}>{discount.code}</Link>
							</div>
							<div>{discount.type_id}</div>
							<div>{discount.value}</div>
							<div>{discount.min_apply_value}</div>
							<div>{discount.category_id}</div>
							<div>{discount.modified_at}</div>
						</div>
					))}
			</div>
		);
	}
}

export default DiscountsPage;
