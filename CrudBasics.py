import sqlite3 as lit
from prettytable import PrettyTable
from datetime import datetime

class CRUDCar:
    def __init__(self, cur, db):
        self.cur = cur
        self.db = db

    def is_id_unique(self, id):
        self.cur.execute('SELECT id FROM cars WHERE id = ?', (id,))
        return self.cur.fetchone() is None

    def add_car(self):
        while True:
            try:
                id = int(input("Enter car ID: "))
                if not self.is_id_unique(id):
                    print("Error: ID already exists. Please choose a unique ID.")
                    continue
                brand = input("Enter car brand: ")
                model = input("Enter car model: ")
                price = int(input("Enter car price: "))
                rented = input("Enter 'true' or 'false' for rented status: ")
                if rented!='true':
                    rented="false"
                car_data = (id, brand, model, price, rented)
                self.cur.execute('INSERT INTO cars VALUES (?,?,?,?,?)', car_data)
                self.db.commit()
                print("Car added")
                break
            except ValueError as e:
                print("Error: Invalid input. Please enter valid IDs and price.")

    def delete_car(self, car_id):
        self.cur.execute('SELECT id FROM cars WHERE id = ?', (car_id,))
        existing_record = self.cur.fetchone()
        if existing_record:
            self.cur.execute('DELETE FROM cars WHERE id = ?', (car_id,))
            self.db.commit()
            print(f"Car with ID {car_id} has been deleted.")
        else:
            print(f"Error: Car with ID {car_id} does not exist.")

    def update_car(self, car_id):
        self.cur.execute('SELECT id FROM cars WHERE id = ?', (car_id,))
        existing_record = self.cur.fetchone()
        if existing_record:
            brand = input("Enter the new brand: ")
            model = input("Enter the new model: ")
            price = int(input("Enter the new price: "))
            rented = input("Enter the new 'true' or 'false' for rented status: ")
            if rented!='true':
                rented='false'

            else:
                self.cur.execute('UPDATE cars SET brand=?, model=?, price=?, rented=? WHERE id=?',
                                (brand, model, price, rented, car_id))
                self.db.commit()
                print(f"Car with ID {car_id} has been modified.")
        else:
            print(f"Error: Car with ID {car_id} does not exist.")

    def read_cars(self):
        self.cur.execute('SELECT * FROM cars')
        data = self.cur.fetchall()
        if not data:
            print("No car records found.")
        else:
            table = PrettyTable()
            table.field_names = ["ID", "Brand", "Model", "Price", "Rented"]
            for row in data:
                table.add_row(row)
            print(table)

class CRUDCustomer:
    def __init__(self, cur, db):
        self.cur = cur
        self.db = db


    def is_id_unique(self, id):
        self.cur.execute('SELECT id FROM customers WHERE id = ?', (id,))
        return self.cur.fetchone() is None

    def add_customer(self):
        while True:
            try:
                id = int(input("Enter customer ID: "))
                if not self.is_id_unique(id):
                    print("Error: ID already exists. Please choose a unique ID.")
                    continue
                first_name = input("Enter customer's first name: ")
                last_name = input("Enter customer's last name: ")
                phone_number = input("Enter customer's phone number: ")
                customer_data = (id, first_name, last_name, phone_number)
                self.cur.execute('INSERT INTO customers VALUES (?,?,?,?)', customer_data)
                self.db.commit()
                print("Customer added")
                break
            except ValueError as e:
                print("Error: Invalid input. Please enter a valid ID.")

    def delete_customer(self, customer_id):
        self.cur.execute('SELECT id FROM customers WHERE id = ?', (customer_id,))
        existing_record = self.cur.fetchone()
        if existing_record:
            self.cur.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
            self.db.commit()
            print(f"Customer with ID {customer_id} has been deleted.")
        else:
            print(f"Error: Customer with ID {customer_id} does not exist.")

    def update_customer(self, customer_id):
        self.cur.execute('SELECT id FROM customers WHERE id = ?', (customer_id,))
        existing_record = self.cur.fetchone()
        if existing_record:
            first_name = input("Enter the new first name: ")
            last_name = input("Enter the new last name: ")
            phone_number = input("Enter the new phone number: ")
            self.cur.execute('UPDATE customers SET first_name=?, last_name=?, phone_number=? WHERE id=?',
                            (first_name, last_name, phone_number, customer_id))
            self.db.commit()
            print(f"Customer with ID {customer_id} has been modified.")
        else:
            print(f"Error: Customer with ID {customer_id} does not exist.")

    def read_customers(self):
        self.cur.execute('SELECT * FROM customers')
        data = self.cur.fetchall()
        if not data:
            print("No customer records found.")
        else:
            table = PrettyTable()
            table.field_names = ["ID", "First Name", "Last Name", "Phone Number"]
            for row in data:
                table.add_row(row)
            print(table)

class CRUDRental:
    def __init__(self, cur, db):
        self.cur = cur
        self.db = db

    def calculate_rental_price(self, car_id, start_date, end_date):
        # Retrieve the car's price
        self.cur.execute('SELECT price FROM cars WHERE id = ?', (car_id,))
        car_price = self.cur.fetchone()[0]

        # Calculate the number of days the car is rented
        rental_period = (end_date - start_date).days

        # Calculate the total rental price
        total_price = car_price * rental_period

        return total_price

    def rent_car(self):
        while True:
            try:
                customer_id = int(input("Enter customer ID: "))
                car_id = int(input("Enter car ID: "))
                start_date_str = input("Enter start date (YYYY-MM-DD): ")
                end_date_str = input("Enter end date (YYYY-MM-DD): ")

                # Parse dates
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

                # Check if the car exists in the "cars" table
                if not self.car_exists(car_id):
                    print("Error: The car does not exist.")
                    continue

                # Check if the end date is greater than the start date
                if end_date <= start_date:
                    print("Error: The end date must be greater than the start date.")
                    continue

                # Check if the car is available for the given date range
                if not self.is_car_available(car_id, start_date, end_date):
                    print("Error: The car is not available for the selected dates.")
                    continue

                rental_data = (customer_id, car_id, start_date_str, end_date_str)

                # Calculate the rental price
                rental_price = self.calculate_rental_price(car_id, start_date, end_date)
                rental_data += (rental_price,)  # Add the rental price to the tuple

                self.cur.execute('INSERT INTO rentals (customer_id, car_id, start_date, end_date, price) VALUES (?,?,?,?,?)', rental_data)

                # Set the "Rented" status of the car to True
                self.cur.execute('UPDATE cars SET rented = "true" WHERE id = ?', (car_id,))

                self.db.commit()
                print(f"Car rented successfully. Total Price: ${rental_price:.2f}")
                break
            except ValueError as e:
                print("Error: Invalid input. Please enter valid IDs and date format (YYYY-MM-DD).")

    def car_exists(self, car_id):
        self.cur.execute('SELECT id FROM cars WHERE id = ?', (car_id,))
        return self.cur.fetchone() is not None
    def is_car_available(self, car_id, start_date, end_date):
        self.cur.execute('SELECT id FROM rentals WHERE car_id = ? AND (end_date >= ? OR start_date <= ?)', (car_id, start_date, end_date))
        return self.cur.fetchone() is None
    def check_expired_rentals(self):
        current_date = datetime.now().date()
        self.cur.execute('SELECT id, end_date FROM rentals WHERE end_date <= ?', (current_date,))
        expired_rentals = self.cur.fetchall()

        for rental_id, end_date in expired_rentals:
            self.cur.execute('DELETE FROM rentals WHERE id = ?', (rental_id,))
            self.db.commit()

            
            self.cur.execute('UPDATE cars SET rented = "false" WHERE id IN (SELECT car_id FROM rentals WHERE id = ?)', (rental_id,))
            self.db.commit()

            print(f"Rental with ID {rental_id} has expired and has been automatically deleted.")
    def show_rentals(self):
        self.check_expired_rentals()
        self.cur.execute('SELECT rentals.id, customers.first_name, customers.last_name, cars.brand, cars.model, rentals.start_date, rentals.end_date FROM rentals INNER JOIN customers ON rentals.customer_id = customers.id INNER JOIN cars ON rentals.car_id = cars.id')
        data = self.cur.fetchall()
        if not data:
            print("No rental records found.")
        else:
            table = PrettyTable()
            table.field_names = ["Rental ID", "Customer Name", "Car", "Start Date", "End Date"]
            for row in data:
                rental_id, first_name, last_name, car_brand, car_model, start_date, end_date = row
                customer_name = f"{first_name} {last_name}"
                car_name = f"{car_brand} {car_model}"
                table.add_row([rental_id, customer_name, car_name, start_date, end_date])
            print(table)


def main():
    try:
        db = lit.connect("database.db")
        cur = db.cursor()

        # Create car, customer, and rental tables if they don't exist
        car_table_query = "CREATE TABLE IF NOT EXISTS cars (id INT, brand TEXT, model TEXT, price INT, rented TEXT)"
        customer_table_query = "CREATE TABLE IF NOT EXISTS customers (id INT, first_name TEXT, last_name TEXT, phone_number TEXT)"
        rental_table_query = "CREATE TABLE IF NOT EXISTS rentals (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INT, car_id INT, start_date DATE, end_date DATE)"

        cur.execute(car_table_query)
        cur.execute(customer_table_query)
        cur.execute(rental_table_query)
        db.commit()
        print("Tables created")

        car_manager = CRUDCar(cur, db)
        customer_manager = CRUDCustomer(cur, db)
        rental_manager = CRUDRental(cur, db)
        rental_manager.check_expired_rentals()

        while True:
            print("Options:")
            print("1. Add Car")
            print("2. Delete Car")
            print("3. Update Car")
            print("4. Add Customer")
            print("5. Delete Customer")
            print("6. Update Customer")
            print("7. Rent a Car")
            print("8. Show Available Cars")
            print("9. Show Customers")
            print("10. Show Rentals")
            print("11. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                car_manager.add_car()
                input("Press Enter to continue...")
            elif choice == "2":
                car_id = input("Enter car ID to delete: ")
                car_manager.delete_car(car_id)
                input("Press Enter to continue...")
            elif choice == "3":
                car_id = input("Enter car ID to update: ")
                car_manager.update_car(car_id)
                input("Press Enter to continue...")
            elif choice == "4":
                customer_manager.add_customer()
                input("Press Enter to continue...")
            elif choice == "5":
                customer_id = input("Enter customer ID to delete: ")
                customer_manager.delete_customer(customer_id)
                input("Press Enter to continue...")
            elif choice == "6":
                customer_id = input("Enter customer ID to update: ")
                customer_manager.update_customer(customer_id)
                input("Press Enter to continue...")
            elif choice == "7":
                rental_manager.rent_car()
                input("Press Enter to continue...")
            elif choice == "8":
                car_manager.read_cars()
                input("Press Enter to continue...")
            elif choice == "9":
                customer_manager.read_customers()
                input("Press Enter to continue...")
            elif choice == "10":
                rental_manager.show_rentals()
                input("Press Enter to continue...")
            elif choice == "11":
                break
            else:
                print("Invalid option. Please enter a valid choice.")

    except lit.Error as e:
        print("Unable to create the tables or connect to the database")

    finally:
        db.close()

if __name__ == "__main__":
    main()
