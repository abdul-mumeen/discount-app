## Discount App

This is a web app to manage discounts. The user will be able to view, add, and delete discounts. The app supports 3 types of discounts:

- Flat amount, e.g. 15€ off
- Percentage, e.g. 15% off
- Free shipping

Every discount has a product category it applies to. A list of product categories available can be seen as a list when creating the a discount.

Every discount comes with a 12-character discount code of the form `XXXX-XXXX-XXXX`. `X` is either a letter of a digit.

Every discount has an optional minimum price. If it is set, the discount is only valid for products of at least the specified price.

The discount of type _Free shipping_ will not accept additional value.

Both _Flat amount_ and _Percentage_ type discounts have a positive integer discount value. Zero will not be accepted.

## Tools Used

### Docker

For easy distribution and ease of starting up, I have dockerized the frontend, backend and the postgres db used in this app.

### React

Built the frontend using react kick started by creat-react-app

### Flask

I used flask, flask-restplus to built the backend.

### Postgres

Postgres is the database used for storing discount data while using flask-SQLAlchemy as the OM.

## Starting the app

- Install Docker and ensure it's running.
- Ensure no service is running on port `5000` and `3000` as they will be used by the backend and frontend respectively.
- Cd into the root directory.
- Create a `.env` file and update it with the details in .env.sample file in the directory. Replace the values in there with your choice.
- Run the command
  ```sh
      docker-compose up --build
  ```
- After the containers have successfully built and running, open a new tab on the terminal.
- Run the command below to enter the backend service shell.
  ```sh
      docker exec -it discount_app_backend sh
  ```
- Run to the command below to create the database table.
  ```sh
  #   flask db upgrade
  ```
- Run `\exit` to close the shell.
- Goto `http://localhost:5000/api/` to see the endpoints documentation, how to use them and call them directory if need be.
- Got0 `http://localhost:3000/discounts` to see discounts available (None at this time).
- Got0 `http://localhost:3000/new` to create one.
