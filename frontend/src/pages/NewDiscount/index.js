import React from 'react';
import { Form } from 'semantic-ui-react';
import Page from '../common/Page';
import categories_data from '../../assests/categories.json';
import { createDiscount } from '../../actions';
import { Button, Modal } from 'semantic-ui-react';

const categories = categories_data.Categories.map(category => ({
	key: category.id,
	value: category.id,
	text: category.name
}));

const type_data = [
	{
		key: 'free_shipping',
		value: 'free_shipping',
		text: 'Free shipping'
	},
	{
		key: 'exact_value',
		value: 'exact_value',
		text: 'Flat amount e.g 50$ off'
	},
	{
		key: 'percentage_value',
		value: 'percentage_value',
		text: 'Percentage amount e.g 30% off'
	}
];

class NewDiscount extends React.Component {
	state = {
		value: 0,
		minValue: 0,
		category: null,
		type: null,
		loading: false,
		showModal: false,
		code: null,
		id: null
	};

	handleSubmit = async e => {
		e.preventDefault();
		const { type, value, minValue, category } = this.state;
		this.setState({ loading: true });

		try {
			const data = await createDiscount(
				type,
				parseInt(value),
				parseInt(minValue),
				parseInt(category)
			);
			this.setState({ code: data.code, id: data.id, showModal: true });
		} catch {
			alert('Error occured, try again');
		} finally {
			this.setState({ loading: false });
		}
	};

	handleChange = (e, { name, value }) => {
		this.setState({ ...this.state, [name]: value });
	};

	resetState = () => {
		this.setState({
			value: 0,
			minValue: 0,
			category: null,
			type: null,
			loading: false,
			showModal: false,
			code: null,
			id: null
		});
	};

	redirectToDetails = () => {
		this.props.history.push(`/discounts/${this.state.id}`);
	};

	render() {
		const { value, minValue, category, type, showModal, code } = this.state;

		return (
			<Page title="Add new discount">
				<Form onSubmit={this.handleSubmit}>
					<Form.Dropdown
						placeholder="Select discount type"
						fluid
						selection
						options={type_data}
						onChange={this.handleChange}
						value={type}
						name="type"
					/>
					<Form.Input
						label="Value"
						type="number"
						name="value"
						value={value}
						disabled={type === 'free_shipping'}
						onChange={this.handleChange}
					/>
					<Form.Input
						label="Minimum Value Applicable"
						type="number"
						name="minValue"
						value={minValue}
						onChange={this.handleChange}
					/>
					<Form.Dropdown
						placeholder="Select discount category"
						fluid
						selection
						options={categories}
						name="category"
						value={category}
						onChange={this.handleChange}
					/>

					<Form.Group>
						<Form.Button type="submit">Add Discount</Form.Button>
					</Form.Group>
				</Form>
				<Modal
					open={showModal}
					closeOnEscape={true}
					closeOnDimmerClick={true}
					onClose={this.resetState}
				>
					<Modal.Header>Success!</Modal.Header>
					<Modal.Content>
						<p>
							New discount has been successfully created! <br />
							Here is the code {code}
						</p>
					</Modal.Content>
					<Modal.Actions>
						<Button onMouseUp={this.redirectToDetails} positive>
							View details
						</Button>
					</Modal.Actions>
				</Modal>
			</Page>
		);
	}
}

export default NewDiscount;
