import wx
import wx.grid as gridlib
import sqlite3
from datetime import datetime

class CRUDCar:
    def __init__(self, cur, db):
        self.cur = cur
        self.db = db

class CarRentalApp(wx.Frame):
    def __init__(self, parent, title):
        super(CarRentalApp, self).__init__(parent, title=title, size=(400, 300))

        # Create a database connection and cursor
        self.db = sqlite3.connect("database.db")
        self.cur = self.db.cursor()

        # Create car table if it doesn't exist
        self.create_table()

        # Create an instance of the CRUDCar class
        self.car_manager = CRUDCar(self.cur, self.db)

        # Create a panel
        panel = wx.Panel(self)
        self.set_background(panel, "360_F_408511812_8UGTuX8BieG571jrbmz0PYsqLv1xPrjO.jpg")

        # Create a sizer for the main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a menu bar
        menu_bar = wx.MenuBar()

        # Create a "Cars" menu
        cars_menu = wx.Menu()
        customes_menu=wx.Menu()
        rental_menu=wx.Menu()
        # Create menu items
        add_car_item = wx.MenuItem(cars_menu, wx.ID_ANY, "Add Car")
        self.Bind(wx.EVT_MENU, self.on_add_car, add_car_item)

        delete_car_item = wx.MenuItem(cars_menu, wx.ID_ANY, "Delete Car")
        self.Bind(wx.EVT_MENU, self.on_delete_car, delete_car_item)

        update_car_item = wx.MenuItem(cars_menu, wx.ID_ANY, "Update Car")
        self.Bind(wx.EVT_MENU, self.on_update_car, update_car_item)

        read_car_item = wx.MenuItem(cars_menu, wx.ID_ANY, "Show Car")
        self.Bind(wx.EVT_MENU, self.on_read_car, read_car_item)
         
        add_customers_item = wx.MenuItem(customes_menu, wx.ID_ANY, "Add Customers")
        self.Bind(wx.EVT_MENU, self.on_add_customers, add_customers_item)

        delete_customers_item = wx.MenuItem(customes_menu, wx.ID_ANY, "Delete Customers")
        self.Bind(wx.EVT_MENU, self.on_delete_customers, delete_customers_item)
        update_customers_item = wx.MenuItem(customes_menu, wx.ID_ANY, "Update Customers")
        self.Bind(wx.EVT_MENU, self.on_update_customers, update_customers_item)
        show_customers_item = wx.MenuItem(customes_menu, wx.ID_ANY, "Show Customers")
        self.Bind(wx.EVT_MENU, self.on_show_customers, show_customers_item)
        add_rental_item = wx.MenuItem(rental_menu, wx.ID_ANY, "Add Rentals")
        self.Bind(wx.EVT_MENU, self.on_add_rental, add_rental_item)
        read_rental_item = wx.MenuItem(cars_menu, wx.ID_ANY, "Show Rentals")
        self.Bind(wx.EVT_MENU, self.on_read_rental, read_rental_item)


        # Add menu items to the "Cars" menu
        cars_menu.Append(add_car_item)
        cars_menu.Append(delete_car_item)
        cars_menu.Append(update_car_item)
        cars_menu.Append(read_car_item)

        ##### customers
        customes_menu.Append(add_customers_item)
        customes_menu.Append(delete_customers_item)
        customes_menu.Append(update_customers_item)
        customes_menu.Append(show_customers_item)
        #
        rental_menu.Append(add_rental_item) 
        rental_menu.Append(read_rental_item) 


        menu_bar.Append(cars_menu, "Cars")
        menu_bar.Append(customes_menu,"Customers")
        #
        menu_bar.Append(rental_menu, "Rentals")



        # Set the menu bar for the frame
        self.SetMenuBar(menu_bar)

        # Set the sizer for the panel
        panel.SetSizer(main_sizer)

        self.Show()
    def set_background(self, panel, image_path):
        # Load the image
        img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        img = img.Scale(400, 300)  # Adjust the size of the image to fit the panel

        # Convert it to a bitmap
        bmp = wx.Bitmap(img)

        # Use wx.StaticBitmap to display the image on the panel
        background = wx.StaticBitmap(panel, -1, bmp, (0, 0))
    def create_table(self):
        car_table_query = "CREATE TABLE IF NOT EXISTS cars (id INT, brand TEXT, model TEXT, price INT, rented TEXT)"
        customer_table_query = "CREATE TABLE IF NOT EXISTS customers (id INT, first_name TEXT, last_name TEXT, phone_number TEXT)"
        rental_table_query = "CREATE TABLE IF NOT EXISTS rentals (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INT, car_id INT, start_date DATE, end_date DATE, price REAL)"

        self.cur.execute(car_table_query)
        self.cur.execute(customer_table_query)
        self.cur.execute(rental_table_query)
        self.db.commit()

    def on_add_car(self, event):
        add_car_frame = wx.Frame(self, title="Add Car", size=(600, 600))
        panel = wx.Panel(add_car_frame)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        id_label = wx.StaticText(panel, label="ID:")
        id_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="id")

        brand_label = wx.StaticText(panel, label="Brand:")
        brand_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="brand")

        model_label = wx.StaticText(panel, label="Model:")
        model_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="model")

        price_label = wx.StaticText(panel, label="Price:")
        price_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="price")

        rented_label = wx.StaticText(panel, label="Rented (true/false):")
        rented_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="rented")

        add_button = wx.Button(panel, label="Add Car")
        add_button.Bind(wx.EVT_BUTTON, self.add_car_to_database)

        main_sizer.Add(id_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(id_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(brand_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(brand_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(model_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(model_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(price_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(price_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(rented_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(rented_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(add_button, 0, wx.ALL | wx.EXPAND, 5)


        panel.SetSizer(main_sizer)

        add_car_frame.Show()
        

    def add_car_to_database(self, event):
        frame = self.FindWindowById(event.GetId()).GetParent()
        id = frame.FindWindowByName("id").GetValue()
        brand = frame.FindWindowByName("brand").GetValue()
        model = frame.FindWindowByName("model").GetValue()
        price = frame.FindWindowByName("price").GetValue()
        rented = frame.FindWindowByName("rented").GetValue()
        self.cur.execute('SELECT id FROM cars WHERE id = ?', (id,))
        existing_record = self.cur.fetchone()
        if existing_record:
            print(f"Error: Car with ID {id} already exists. Please choose a different ID.")
            return
        try:
            price = int(price)
        except ValueError:
            print("Error: Price must be an integer.")
            return
        if rented!='true'or'TRUE':
            rented='false'
        car_data = (id, brand, model, price, rented)
        self.cur.execute('INSERT INTO cars (id, brand, model, price, rented) VALUES (?,?,?,?,?)', car_data)
        self.db.commit()
        print("Car added successfully.")
        wx.MessageBox(f"Car with ID {id} has been Added.", "Success", wx.OK | wx.ICON_INFORMATION)
        
    def on_delete_car(self, event):

        delete_car_frame = wx.Frame(self, title="Delete Car", size=(300, 200))


        panel = wx.Panel(delete_car_frame)

  
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        id_label = wx.StaticText(panel, label="Enter car ID to delete:")
        id_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="id")

        delete_button = wx.Button(panel, label="Delete Car")
        delete_button.Bind(wx.EVT_BUTTON, self.perform_delete_car)

        main_sizer.Add(id_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(id_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(delete_button, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(main_sizer)

        delete_car_frame.Show()

    def perform_delete_car(self, event):
        frame = self.FindWindowById(event.GetId()).GetParent()
        car_id = frame.FindWindowByName("id").GetValue()
        self.cur.execute('SELECT id FROM cars WHERE id = ?', (car_id,))
        existing_record = self.cur.fetchone()

        if existing_record:
          
            self.cur.execute('DELETE FROM cars WHERE id = ?', (car_id,))
            self.db.commit()
            wx.MessageBox(f"Car with ID {car_id} has been deleted.", "Success", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f"Error: Car with ID {car_id} does not exist.", "Error", wx.OK | wx.ICON_ERROR)

        print(f"Delete car with ID {car_id}")

        
    def on_update_car(self, event):
       
        update_car_frame = wx.Frame(self, title="Update Car", size=(600, 600))

       
        panel = wx.Panel(update_car_frame)

    
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        id_label = wx.StaticText(panel, label="Car ID to Update:")
        id_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="id")

        brand_label = wx.StaticText(panel, label="New Brand:")
        brand_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="brand")

        model_label = wx.StaticText(panel, label="New Model:")
        model_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="model")

        price_label = wx.StaticText(panel, label="New Price:")
        price_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="price")

        rented_label = wx.StaticText(panel, label="New Rented (true/false):")
        rented_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="rented")

        update_button = wx.Button(panel, label="Update Car")
        update_button.Bind(wx.EVT_BUTTON, self.perform_update_car)

     
        main_sizer.Add(id_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(id_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(brand_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(brand_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(model_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(model_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(price_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(price_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(rented_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(rented_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(update_button, 0, wx.ALL | wx.EXPAND, 5)

     
        panel.SetSizer(main_sizer)

        update_car_frame.Show()
    def perform_update_car(self, event):
        frame = self.FindWindowById(event.GetId()).GetParent()
        car_id = frame.FindWindowByName("id").GetValue()
        new_brand = frame.FindWindowByName("brand").GetValue()
        new_model = frame.FindWindowByName("model").GetValue()
        new_price = frame.FindWindowByName("price").GetValue()
        new_rented = frame.FindWindowByName("rented").GetValue()
        self.cur.execute('SELECT id FROM cars WHERE id = ?', (car_id,))
        existing_record = self.cur.fetchone()
        if not existing_record:
            print(f"Error: Car with ID {id} not exict. Please choose a different ID.")
            return
        
        try:
            new_price = int(new_price)
        except ValueError:
            wx.MessageBox("Error: Price must be an integer.", "Error", wx.OK | wx.ICON_ERROR)
            return
        if new_rented!="true":
            new_rented="false"
        if existing_record:
          
            self.cur.execute('UPDATE cars SET brand=?, model=?, price=?, rented=? WHERE id=?',
                            (new_brand, new_model, new_price, new_rented, car_id))
            self.db.commit()
            wx.MessageBox(f"Car with ID {car_id} has been updated.", "Success", wx.OK | wx.ICON_INFORMATION)
            
        else:
            wx.MessageBox(f"Error: Car with ID {car_id} does not exist.", "Error", wx.OK | wx.ICON_ERROR)
    def on_read_car(self, event):
        self.read_cars()
    def read_cars(self):
        # Read and display cars from the database
        self.cur.execute('SELECT * FROM cars')
        data = self.cur.fetchall()

        if not data:
            wx.MessageBox("No cars found.", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            # Create a new window to display cars
            cars_window = wx.Frame(self, title="Car Records", size=(500, 300))

            # Create a wxGrid widget to display the table
            grid = gridlib.Grid(cars_window)
            grid.CreateGrid(len(data), len(data[0]))

            # Set column labels
            columns = ["ID", "Brand", "Model", "Price", "Rented"]
            for col, label in enumerate(columns):
                grid.SetColLabelValue(col, label)

            # Insert data into the wxGrid
            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data):
                    grid.SetCellValue(row_index, col_index, str(value))

            grid.AutoSizeColumns()
            cars_window.Show()
    def on_add_customers(self, event):
    
        add_customers_frame = wx.Frame(self, title="Add Customers", size=(600, 600))
        panel = wx.Panel(add_customers_frame)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        id_label = wx.StaticText(panel, label="ID:")
        id_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="id")

        first_name_label = wx.StaticText(panel, label="First_name:")
        first_name_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="first_name")

        last_name_label = wx.StaticText(panel, label="Last_name:")
        last_name_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="last_name")

        phone_label = wx.StaticText(panel, label="Phone:")
        phone_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="phone")

        

        add_button = wx.Button(panel, label="Add Customer")
        add_button.Bind(wx.EVT_BUTTON, self.add_customer_to_database)

        main_sizer.Add(id_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(id_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(first_name_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(first_name_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(last_name_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(last_name_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(phone_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(phone_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        

        main_sizer.Add(add_button, 0, wx.ALL | wx.EXPAND, 5)


        panel.SetSizer(main_sizer)

        add_customers_frame.Show()
    def add_customer_to_database(self, event):
   
        frame = self.FindWindowById(event.GetId()).GetParent()
        id = frame.FindWindowByName("id").GetValue()
        first_name = frame.FindWindowByName("first_name").GetValue()
        last_name = frame.FindWindowByName("last_name").GetValue()
        phone = frame.FindWindowByName("phone").GetValue()
        
        self.cur.execute('SELECT id FROM customers WHERE id = ?', (id,))
        existing_record = self.cur.fetchone()
        if existing_record:
            print(f"Error: Customer with ID {id} already exists. Please choose a different ID.")
            return
        if not phone.isdigit() or len(phone) != 10:
            wx.MessageBox("Error: Phone number must be a 10-digit number.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        customer_data = (id, first_name, last_name, phone)
        self.cur.execute('INSERT INTO customers (id, first_name, last_name, phone_number) VALUES (?,?,?,?)', customer_data)
        self.db.commit()
        print("Car added successfully.")
        wx.MessageBox(f"Customer with ID {id} has been Added.", "Success", wx.OK | wx.ICON_INFORMATION)
    def on_delete_customers(self,event):
        delete_customers_frame = wx.Frame(self, title="Delete customers", size=(300, 200))


        panel = wx.Panel(delete_customers_frame)

  
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        id_label = wx.StaticText(panel, label="Enter car ID to delete:")
        id_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="id")

        delete_button = wx.Button(panel, label="Delete customers")
        delete_button.Bind(wx.EVT_BUTTON, self.perform_delete_customers)

        main_sizer.Add(id_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(id_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(delete_button, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(main_sizer)

        delete_customers_frame.Show()
    def perform_delete_customers(self,event):
        frame = self.FindWindowById(event.GetId()).GetParent()
        customers_id = frame.FindWindowByName("id").GetValue()
        self.cur.execute('SELECT id FROM customers WHERE id = ?', (customers_id,))
        existing_record = self.cur.fetchone()

        if existing_record:
          
            self.cur.execute('DELETE FROM customers WHERE id = ?', (customers_id,))
            self.db.commit()
            wx.MessageBox(f"Car with ID {customers_id} has been deleted.", "Success", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f"Error: Car with ID {customers_id} does not exist.", "Error", wx.OK | wx.ICON_ERROR)
    def on_update_customers(self,event):
        update_customers_frame = wx.Frame(self, title="Update customers", size=(600, 600))

       
        panel = wx.Panel(update_customers_frame)

    
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        id_label = wx.StaticText(panel, label="customer ID to Update:")
        id_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="id")

        first_name_label = wx.StaticText(panel, label="New First name:")
        first_name_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="first_name")

        last_name_label = wx.StaticText(panel, label="New last_name:")
        last_name_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="last_name")

        phone_label = wx.StaticText(panel, label="New phone:")
        phone_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="phone")

        update_button = wx.Button(panel, label="Update customer")
        update_button.Bind(wx.EVT_BUTTON, self.perform_update_customer)
    

     
        main_sizer.Add(id_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(id_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(first_name_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(first_name_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(last_name_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(last_name_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(phone_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(phone_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(update_button, 0, wx.ALL | wx.EXPAND, 5)

     
        panel.SetSizer(main_sizer)

        update_customers_frame.Show()
    def perform_update_customer(self,event):
        frame = self.FindWindowById(event.GetId()).GetParent()
        customer_id = frame.FindWindowByName("id").GetValue()
        new_first_name = frame.FindWindowByName("first_name").GetValue()
        new_last_name = frame.FindWindowByName("last_name").GetValue()
        new_phone = frame.FindWindowByName("phone").GetValue()
        self.cur.execute('SELECT id FROM customers WHERE id = ?', (customer_id,))
        existing_record = self.cur.fetchone()
        if not existing_record:
            print(f"Error: Customer with ID {id} not exict. Please choose a different ID.")
            return
        if not new_phone.isdigit() or len(new_phone) != 10:
            wx.MessageBox("Error: Phone number must be a 10-digit number.", "Error", wx.OK | wx.ICON_ERROR)
            return
       
        if existing_record:
          
            self.cur.execute('UPDATE customers SET first_name=?, last_name=?, phone_number=? WHERE id=?',
                            (new_first_name, new_last_name, new_phone, customer_id))
            self.db.commit()
            wx.MessageBox(f"Customers with ID {customer_id} has been updated.", "Success", wx.OK | wx.ICON_INFORMATION)
            
        else:
            wx.MessageBox(f"Error: Customer with ID {customer_id} does not exist.", "Error", wx.OK | wx.ICON_ERROR)
    def on_show_customers(self,event):
        self.read_customers()
    def read_customers(self):
        # Read and display cars from the database
        self.cur.execute('SELECT * FROM customers')
        data = self.cur.fetchall()

        if not data:
            wx.MessageBox("No cars found.", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            # Create a new window to display cars
            customers_window = wx.Frame(self, title="Customers Records", size=(500, 300))

            # Create a wxGrid widget to display the table
            grid = gridlib.Grid(customers_window)
            grid.CreateGrid(len(data), len(data[0]))

            # Set column labels
            columns = ["ID", "First_name", "Last_name", "Phone"]
            for col, label in enumerate(columns):
                grid.SetColLabelValue(col, label)

            # Insert data into the wxGrid
            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data):
                    grid.SetCellValue(row_index, col_index, str(value))

            grid.AutoSizeColumns()
            customers_window.Show()
    def on_add_rental(self,event):
        frame = wx.Frame(self, title="Add Car", size=(600, 600))
        panel = wx.Panel(frame)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        customer_id = wx.StaticText(panel, label="customer_id:")
        customer_id_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="customer_id")

        car_id_label = wx.StaticText(panel, label="car_id:")
        car_id_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="car_id")

        start_date_label = wx.StaticText(panel, label="start_date:")
        start_date_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="start_date")

        end_date_label = wx.StaticText(panel, label="end_date:")
        end_date_textctrl = wx.TextCtrl(panel, id=wx.ID_ANY, name="end_date")
        add_button = wx.Button(panel, label="Add Rental")
        add_button.Bind(wx.EVT_BUTTON, self.add_rental_to_database)

        main_sizer.Add(customer_id, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(customer_id_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(car_id_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(car_id_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(start_date_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(start_date_textctrl, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(end_date_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(end_date_textctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(add_button, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(main_sizer)
        frame.Show()   
    def add_rental_to_database(self, event):
        try:
            frame = self.FindWindowById(event.GetId()).GetParent()
            customer_id = int(frame.FindWindowByName("customer_id").GetValue())
            car_id = int(frame.FindWindowByName("car_id").GetValue())
            start_date = frame.FindWindowByName("start_date").GetValue()
            end_date = frame.FindWindowByName("end_date").GetValue()

            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            with self.db:
                self.cur.execute('SELECT id FROM cars WHERE id = ?', (car_id,))
                existing_car = self.cur.fetchone()
                if not existing_car:
                    print(f"Error: Car with ID {car_id} does not exist. Please choose a different ID.")
                    return

                self.cur.execute('SELECT id FROM customers WHERE id = ?', (customer_id,))
                existing_customer = self.cur.fetchone()
                if not existing_customer:
                    print(f"Error: Customer with ID {customer_id} does not exist. Please choose a different ID.")
                    return

                if end_date <= start_date:
                    print("Error: The end date must be greater than the start date.")
                    wx.MessageBox("Error: The end date must be greater than the start date.", "Error", wx.OK | wx.ICON_ERROR)
                    return

                if  self.is_car_available(car_id, start_date, end_date):
                    print("Error: The car is not available for the selected dates.")
                    wx.MessageBox("Error: The car is not available for the selected dates.", "Error", wx.OK | wx.ICON_ERROR)
                    return


                rental_data = (customer_id, car_id, start_date, end_date)
                rental_price = self.calculate_rental_price(car_id, start_date, end_date)
                rental_data += (rental_price,)
                self.cur.execute('INSERT INTO rentals (customer_id, car_id, start_date, end_date, price) VALUES (?,?,?,?,?)', rental_data)

                self.cur.execute('UPDATE cars SET rented = "true" WHERE id = ?', (car_id,))

            self.db.commit()
            print(f"Car rented successfully. Total Price: ${rental_price:.2f}")
            wx.MessageBox(f"Car rented successfully. Total Price: ${rental_price:.2f}", "Success", wx.OK | wx.ICON_INFORMATION)

        except ValueError:
            wx.MessageBox("Error: Invalid date format (YYYY-MM-DD).", "Error", wx.OK | wx.ICON_ERROR)
            return

    
    def is_car_available(self, car_id, start_date, end_date):

        start_date = start_date.date()
        end_date = end_date.date()

        query = 'SELECT id FROM rentals WHERE car_id = ? AND NOT (end_date < ? OR start_date > ?)'
        self.cur.execute(query, (car_id, start_date, end_date))
        result = self.cur.fetchone()
        print(f"Checking availability for car {car_id} between {start_date} and {end_date}. Result: {result}")
        return result



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
            wx.MessageBox(f"Rental with ID {rental_id} has expired and has been automatically deleted.", "Success", wx.OK | wx.ICON_INFORMATION)
    def calculate_rental_price(self, car_id, start_date, end_date):
        self.cur.execute('SELECT price FROM cars WHERE id = ?', (car_id,))
        car_price = self.cur.fetchone()[0]
        rental_period = (end_date - start_date).days
        total_price = car_price * rental_period
        return total_price
    def on_read_rental(self,event):
        self.read_rentals()
    def read_rentals(self):
        self.check_expired_rentals()
        self.cur.execute('SELECT rentals.id, customers.first_name, customers.last_name, cars.brand, cars.model, rentals.start_date, rentals.end_date, rentals.price FROM rentals INNER JOIN customers ON rentals.customer_id = customers.id INNER JOIN cars ON rentals.car_id = cars.id')
        data = self.cur.fetchall()

        if not data:
            wx.MessageBox("No rentals found.", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            rentals_window = wx.Frame(self, title="Rentals Records", size=(600, 400))
            grid = gridlib.Grid(rentals_window)
            grid.CreateGrid(len(data), len(data[0]))
            columns = ["ID", "First Name", "Last Name", "Brand", "Model", "Start Date", "End Date", "Price"]
            for col, label in enumerate(columns):
                grid.SetColLabelValue(col, label)
            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data):
                    grid.SetCellValue(row_index, col_index, str(value))

            grid.AutoSizeColumns()
            rentals_window.Show()


        
        


       


    
if __name__ == "__main__":
    app = wx.App(False)
    frame = CarRentalApp(None, "Car Rental Management System")
    frame.Show()
    app.MainLoop()
