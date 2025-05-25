### Database Structures for OLTP Systems

To keep the applications realistic and diverse, we'll define separate schemas for each OLTP database while ensuring they can be integrated into a unified Data Warehouse. Here's the proposed structure:

---

### **1. Desktop Application: Inventory Management**
- **Purpose**: Generate CSV files for inventory and restocking.
- **Database**: `InventoryDB`

#### **Tables**
1. **Products**
   - `ProductID` (PK) - Unique identifier.
   - `ProductName` - Name of the product.
   - `CategoryID` (FK) - Links to Categories.
   - `SupplierID` (FK) - Links to Suppliers.
   - `UnitPrice` - Price per unit.
   - `UnitsInStock` - Current stock quantity.

2. **Categories**
   - `CategoryID` (PK) - Unique identifier.
   - `CategoryName` - Name of the category.
   - `Description` - Category description.

3. **Suppliers**
   - `SupplierID` (PK) - Unique identifier.
   - `SupplierName` - Name of the supplier.
   - `ContactName` - Contact person.
   - `Phone` - Contact phone number.
   - `Address` - Supplier's address.

4. **InventoryTransactions**
   - `TransactionID` (PK) - Unique identifier.
   - `ProductID` (FK) - Links to Products.
   - `TransactionDate` - Date of transaction.
   - `Quantity` - Quantity added or removed.
   - `TransactionType` - `IN` for stock added, `OUT` for stock removed.

#### **Relationships**
- Products ↔ Categories (Many-to-One)
- Products ↔ Suppliers (Many-to-One)
- Products ↔ InventoryTransactions (One-to-Many)

---

### **2. Web Application: Sales Management**
- **Purpose**: Provide APIs for recording sales and managing customer orders.
- **Database**: `SalesDB`

#### **Tables**
1. **Customers**
   - `CustomerID` (PK) - Unique identifier.
   - `FirstName` - Customer's first name.
   - `LastName` - Customer's last name.
   - `Email` - Email address.
   - `Phone` - Contact phone number.
   - `Address` - Billing address.

2. **Orders**
   - `OrderID` (PK) - Unique identifier.
   - `CustomerID` (FK) - Links to Customers.
   - `OrderDate` - Date of the order.
   - `TotalAmount` - Total price for the order.

3. **OrderDetails**
   - `OrderDetailID` (PK) - Unique identifier.
   - `OrderID` (FK) - Links to Orders.
   - `ProductID` (FK) - Links to Products in `InventoryDB`.
   - `Quantity` - Quantity of the product.
   - `UnitPrice` - Price per unit.

#### **Relationships**
- Customers ↔ Orders (One-to-Many)
- Orders ↔ OrderDetails (One-to-Many)
- OrderDetails ↔ Products in `InventoryDB` (Foreign Key Relationship)

---

### **3. Telegram Bot: Employee Attendance**
- **Purpose**: Track employee attendance and daily activity.
- **Database**: `HRDB`

#### **Tables**
1. **Employees**
   - `EmployeeID` (PK) - Unique identifier.
   - `FirstName` - First name.
   - `LastName` - Last name.
   - `Position` - Job title.
   - `HireDate` - Date of hiring.
   - `Phone` - Contact phone number.

2. **Attendance**
   - `AttendanceID` (PK) - Unique identifier.
   - `EmployeeID` (FK) - Links to Employees.
   - `AttendanceDate` - Date of attendance.
   - `CheckInTime` - Time of check-in.
   - `CheckOutTime` - Time of check-out.

3. **Shifts**
   - `ShiftID` (PK) - Unique identifier.
   - `EmployeeID` (FK) - Links to Employees.
   - `ShiftDate` - Date of the shift.
   - `StartTime` - Shift start time.
   - `EndTime` - Shift end time.

#### **Relationships**
- Employees ↔ Attendance (One-to-Many)
- Employees ↔ Shifts (One-to-Many)

---

### **Integration Considerations for Data Warehouse**
To integrate the three databases into a unified Data Warehouse:
- **Common Dimensions**:
  - `Date` dimension for linking orders, inventory transactions, and attendance.
  - `Product` dimension for inventory and sales analysis.
- **Fact Tables**:
  - `SalesFact` combining sales data.
  - `InventoryFact` capturing inventory movement.
  - `AttendanceFact` summarizing employee attendance.
