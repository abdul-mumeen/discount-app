import React from 'react';
import { Link } from 'react-router-dom';
import { Table, Menu, Icon, Button } from 'semantic-ui-react';
import times from 'lodash.times';
import { fetchAllDiscounts } from '../../actions';
import Page from '../common/Page';

const TOTAL_PER_PAGE = 1;

/**
 *
 * @class DiscountsPage
 * @extends {React.Component}
 */
class DiscountsPage extends React.Component {
	state = {
		discounts: [],
		page: 0,
		totalPages: 0
	};

	async componentDidMount() {
		const data = await fetchAllDiscounts();
		const discounts = data.discounts;
		const totalPages = Math.ceil(discounts.length / TOTAL_PER_PAGE);

		this.setState({
			discounts,
			page: 0,
			totalPages
		});
	}

	setPage(page) {
		return () => {
			this.setState({ page });
		};
	}

	nextPage = () => {
		const { page } = this.state;
		this.setState({ page: page - 1 });
	};

	prevPage = () => {
		const { page } = this.state;
		this.setState({ page: page + 1 });
	};

	handleDelete = discountId => {
		const { discounts } = this.state;

		this.setState({
			discounts: discounts.filter(discount => discounts.id !== discountId)
		});
	};

	renderTable() {
		const { discounts, page, totalPages } = this.state;
		const startIndex = page * TOTAL_PER_PAGE;
		return (
			<Table celled striped>
				<Table.Header>
					<Table.Row>
						<Table.HeaderCell>Code</Table.HeaderCell>
						<Table.HeaderCell>Type</Table.HeaderCell>
						<Table.HeaderCell>Value</Table.HeaderCell>
						<Table.HeaderCell>Minimum value to discount</Table.HeaderCell>
						<Table.HeaderCell>Category</Table.HeaderCell>
						<Table.HeaderCell>Date updated</Table.HeaderCell>
					</Table.Row>
				</Table.Header>
				<Table.Body>
					{discounts
						.slice(startIndex, startIndex + TOTAL_PER_PAGE)
						.map(discount => (
							<Table.Row key={discount.id}>
								<Table.Cell>
									<Link to={`/discounts/${discount.id}`}>{discount.code}</Link>
								</Table.Cell>
								<Table.Cell>{discount.type_id}</Table.Cell>
								<Table.Cell>{discount.value}</Table.Cell>
								<Table.Cell>{discount.min_apply_value}</Table.Cell>
								<Table.Cell>{discount.category_id}</Table.Cell>
								<Table.Cell>{discount.modified_at}</Table.Cell>
							</Table.Row>
						))}
				</Table.Body>
				<Table.Footer>
					<Table.Row>
						<Table.HeaderCell colSpan={6}>
							<Menu floated="right" pagination>
								{page !== 0 && (
									<Menu.Item as="a" icon onClick={this.prevPage}>
										<Icon name="left chevron" />
									</Menu.Item>
								)}
								{times(totalPages, n => (
									<Menu.Item
										as="a"
										key={n}
										active={n === page}
										onClick={this.setPage(n)}
									>
										{n + 1}
									</Menu.Item>
								))}
								{page !== totalPages - 1 && (
									<Menu.Item as="a" icon onClick={this.nextPage}>
										<Icon name="right chevron" />
									</Menu.Item>
								)}
							</Menu>
						</Table.HeaderCell>
					</Table.Row>
				</Table.Footer>
			</Table>
		);
	}

	render() {
		const { discounts } = this.state;
		return (
			<Page title="Discounts">
				<Button positive>New Discount</Button>
				{discounts.length > 0 ? (
					this.renderTable()
				) : (
					<div>No discount found.</div>
				)}
			</Page>
		);
	}
}

export default DiscountsPage;
