import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import DiscountsPage from './pages/DiscountsPage';
import DiscountInfo from './pages/DiscountInfo';
import 'semantic-ui-css/semantic.min.css';

const Routes = () => (
	<Router>
		<Switch>
			<Route exact path="/discounts/:discountId" component={DiscountInfo} />
			<Route path="*" component={DiscountsPage} />
		</Switch>
	</Router>
);

export default Routes;
