### **Data Warehouse Database Structure**

The Data Warehouse (`RetailDW`) will integrate data from the three OLTP databases (`InventoryDB`, `SalesDB`, and `HRDB`) and organize it into a dimensional model for efficient analysis and reporting. Here's the detailed structure:

---

### **1. Dimensions**

1. **DimDate**
   - `DateKey` (PK) - Unique identifier for the date (e.g., `YYYYMMDD`).
   - `Date` - Full date (e.g., `2025-01-16`).
   - `Day` - Day of the month.
   - `Month` - Month name.
   - `Year` - Year.
   - `Quarter` - Quarter of the year.
   - `DayOfWeek` - Day name (e.g., `Monday`).
   - `IsWeekend` - Boolean indicating if it's a weekend.

2. **DimProduct**
   - `ProductKey` (PK) - Surrogate key.
   - `ProductID` - Source system product ID.
   - `ProductName` - Name of the product.
   - `Category` - Product category.
   - `SupplierName` - Name of the supplier.
   - `UnitPrice` - Price per unit.

3. **DimCustomer**
   - `CustomerKey` (PK) - Surrogate key.
   - `CustomerID` - Source system customer ID.
   - `FullName` - Concatenation of first and last names.
   - `Email` - Customer email address.
   - `Phone` - Customer phone number.
   - `Address` - Customer address.

4. **DimEmployee**
   - `EmployeeKey` (PK) - Surrogate key.
   - `EmployeeID` - Source system employee ID.
   - `FullName` - Employee full name.
   - `Position` - Job title.
   - `HireDate` - Date of hiring.

5. **DimShift**
   - `ShiftKey` (PK) - Surrogate key.
   - `ShiftID` - Source system shift ID.
   - `ShiftDate` - Date of the shift.
   - `StartTime` - Start time of the shift.
   - `EndTime` - End time of the shift.

---

### **2. Fact Tables**

1. **FactSales**
   - `SalesKey` (PK) - Surrogate key.
   - `OrderID` - Source system order ID.
   - `DateKey` (FK) - Links to `DimDate`.
   - `CustomerKey` (FK) - Links to `DimCustomer`.
   - `ProductKey` (FK) - Links to `DimProduct`.
   - `Quantity` - Quantity sold.
   - `UnitPrice` - Price per unit.
   - `TotalAmount` - Calculated as `Quantity × UnitPrice`.

2. **FactInventory**
   - `InventoryKey` (PK) - Surrogate key.
   - `TransactionID` - Source system transaction ID.
   - `DateKey` (FK) - Links to `DimDate`.
   - `ProductKey` (FK) - Links to `DimProduct`.
   - `TransactionType` - `IN` for stock added, `OUT` for stock removed.
   - `Quantity` - Quantity involved in the transaction.

3. **FactAttendance**
   - `AttendanceKey` (PK) - Surrogate key.
   - `AttendanceID` - Source system attendance ID.
   - `DateKey` (FK) - Links to `DimDate`.
   - `EmployeeKey` (FK) - Links to `DimEmployee`.
   - `CheckInTime` - Time of check-in.
   - `CheckOutTime` - Time of check-out.
   - `ShiftKey` (FK) - Links to `DimShift`.

---

### **3. Relationships**

- **DimDate**:
  - Links to `FactSales` via `DateKey`.
  - Links to `FactInventory` via `DateKey`.
  - Links to `FactAttendance` via `DateKey`.

- **DimProduct**:
  - Links to `FactSales` via `ProductKey`.
  - Links to `FactInventory` via `ProductKey`.

- **DimCustomer**:
  - Links to `FactSales` via `CustomerKey`.

- **DimEmployee**:
  - Links to `FactAttendance` via `EmployeeKey`.

- **DimShift**:
  - Links to `FactAttendance` via `ShiftKey`.

---

### **4. Additional Considerations**

1. **Data Granularity**:
   - **FactSales**: One row per product per order.
   - **FactInventory**: One row per transaction.
   - **FactAttendance**: One row per employee per attendance entry.

2. **Surrogate Keys**:
   - Use surrogate keys for all dimensions to ensure uniformity and independence from source systems.

3. **Slowly Changing Dimensions (SCD)**:
   - For attributes like `UnitPrice` in `DimProduct`, consider using SCD Type 2 to track historical changes.

4. **Aggregation**:
   - Pre-aggregate measures (e.g., total sales, stock levels) for performance optimization.

