import React from 'react';
import { fetchDiscountInfo, deleteDiscount } from '../../actions';
import Page from '../common/Page';
import { Button, Modal } from 'semantic-ui-react';
import categories_data from '../../assests/categories.json';

const categories_object = {};
categories_data.Categories.forEach(category => {
	categories_object[category.id] = category;
});

const type = {
	free_shipping: 'Free Shipping',
	exact_value: 'Flat Amount',
	percentage_value: 'Percentage Amount'
};

/**
 *
 * @class DiscountInfo
 * @extends {React.Component}
 */
class DiscountInfo extends React.Component {
	state = {
		discount: {},
		showModal: false
	};

	async componentDidMount() {
		const {
			match: { params }
		} = this.props;
		try {
			const data = await fetchDiscountInfo(params.discountId);
			this.setState({ discount: data });
		} catch {
			this.setState({ discount: null });
		}
	}

	showWarning = () => {
		this.setState({ showModal: true });
	};

	closeModal = () => {
		this.setState({ showModal: false });
	};

	deleteDiscountDetails = async () => {
		try {
			await deleteDiscount(this.state.discount.id);
			alert('Successfully deleted!');
			this.props.history.push('/discounts/');
		} catch {
			alert('Error has occured, try again!');
		}
	};

	render() {
		const { discount, showModal } = this.state;
		return (
			<Page title="Discount">
				{discount ? (
					<React.Fragment>
						<Button negative onClick={this.showWarning}>
							Delete discount
						</Button>
						<div>
							<p>
								<br />
								Code:
								{discount.code}
							</p>
							<p>Type: {type[discount.type_id]}</p>
							<p>Value: {discount.value}</p>
							<p>Minimum Value Applicable: {discount.min_apply_value}</p>
							<p>
								Category:{' '}
								{categories_object[discount.category_id]
									? categories_object[discount.category_id].name
									: 'Missing'}
							</p>
							<p>Date updated {discount.modified_at}</p>
						</div>
						<Modal
							open={showModal}
							closeOnEscape={true}
							closeOnDimmerClick={true}
						>
							<Modal.Header>Warning!</Modal.Header>
							<Modal.Content>
								<p>Are you sure you want to delete this Discount?</p>
							</Modal.Content>
							<Modal.Actions>
								<Button onClick={this.closeModal} positive>
									No
								</Button>
								<Button onClick={this.deleteDiscountDetails} negative>
									Yes
								</Button>
							</Modal.Actions>
						</Modal>
					</React.Fragment>
				) : (
					<div>
						<h3>No record found!</h3>
					</div>
				)}
			</Page>
		);
	}
}

export default DiscountInfo;
