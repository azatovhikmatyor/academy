### **ETL Processes for Data Warehouse**

An effective ETL (Extract, Transform, Load) pipeline ensures seamless integration of data from your OLTP systems (`InventoryDB`, `SalesDB`, `HRDB`) into the Data Warehouse (`RetailDW`). Here’s a step-by-step guide for implementing the ETL processes:

---

### **1. Extract Phase**

#### **Purpose**: Fetch data from the OLTP systems.

1. **Source Systems**:
   - Inventory data from `InventoryDB`.
   - Sales data from `SalesDB`.
   - Employee and attendance data from `HRDB`.

2. **Tools**:
   - Use **SQL Server Integration Services (SSIS)** or equivalent ETL tools (e.g., Talend, Pentaho, Apache NiFi).

3. **Steps**:
   - **Full Extraction for Initial Load**:
     - Extract entire datasets (e.g., all products, orders, customers).
   - **Incremental Extraction for Updates**:
     - Use timestamps or version numbers to identify new or updated rows.
     - Example SQL for Incremental Extract:
       ```sql
       SELECT * 
       FROM Orders 
       WHERE LastModifiedDate > @LastExtractDate;
       ```

4. **Output**:
   - Store extracted data in staging tables within the Data Warehouse.

---

### **2. Transform Phase**

#### **Purpose**: Cleanse, validate, and reshape data for the Data Warehouse.

1. **Data Cleansing**:
   - Handle nulls, duplicates, and incorrect values.
   - Standardize formats (e.g., date, phone numbers, addresses).
   - Example SQL for Deduplication:
     ```sql
     DELETE FROM Staging.Customers 
     WHERE CustomerID IN (
       SELECT CustomerID 
       FROM Staging.Customers
       GROUP BY CustomerID
       HAVING COUNT(*) > 1
     );
     ```

2. **Data Validation**:
   - Check foreign key constraints.
   - Validate data types and ranges (e.g., non-negative quantities).

3. **Dimension Table Preparation**:
   - Assign surrogate keys to dimension records.
   - Implement Slowly Changing Dimensions (SCD):
     - **Type 1**: Overwrite old values.
     - **Type 2**: Maintain history by adding a new row with start and end dates.

   - Example SCD Type 2 for `DimProduct`:
     ```sql
     UPDATE DimProduct
     SET EndDate = GETDATE()
     WHERE ProductID = @ProductID
       AND EndDate IS NULL;

     INSERT INTO DimProduct (ProductKey, ProductID, ProductName, StartDate, EndDate)
     VALUES (@NewProductKey, @ProductID, @ProductName, GETDATE(), NULL);
     ```

4. **Fact Table Preparation**:
   - Aggregate transactional data for the fact tables.
   - Replace source system IDs with surrogate keys from dimensions.

   - Example Fact Table Transformation:
     ```sql
     INSERT INTO FactSales (SalesKey, DateKey, CustomerKey, ProductKey, Quantity, UnitPrice, TotalAmount)
     SELECT
       NEWID(), -- Generate new surrogate key
       d.DateKey,
       c.CustomerKey,
       p.ProductKey,
       s.Quantity,
       s.UnitPrice,
       s.Quantity * s.UnitPrice AS TotalAmount
     FROM Staging.Sales s
     JOIN DimDate d ON s.OrderDate = d.Date
     JOIN DimCustomer c ON s.CustomerID = c.CustomerID
     JOIN DimProduct p ON s.ProductID = p.ProductID;
     ```

---

### **3. Load Phase**

#### **Purpose**: Populate the Data Warehouse with transformed data.

1. **Staging Area**:
   - Load raw data from source systems into staging tables for intermediate processing.

2. **Dimension Tables**:
   - Insert new dimension records.
   - Update existing records based on SCD logic.

3. **Fact Tables**:
   - Insert transformed fact data.
   - Use bulk loading techniques for performance.

4. **Validation**:
   - Verify row counts and key mappings between staging, dimensions, and facts.

---

### **4. Incremental Data Load**

#### **Key Steps**:
1. Identify new or updated records in source systems.
   - Use `LastModifiedDate`, `ChangeFlag`, or equivalent fields.
2. Extract only the changed records.
3. Apply transformations and update dimensions and facts.
4. Archive processed records from staging tables.

---

### **5. Scheduling and Automation**

#### **Tools**:
- **SSIS** for ETL workflows.
- **SQL Server Agent** for scheduling.
- **Python or PowerShell Scripts** for custom automation.

#### **Typical Schedule**:
- **Daily ETL**:
  - Load daily transactions and attendance.
- **Weekly ETL**:
  - Rebuild aggregated tables or refresh SCDs.
- **Monthly ETL**:
  - Perform full audits and data validation.

---

### **6. Monitoring and Logging**

1. Log ETL process status (success, failure, row counts).
2. Capture errors in a dedicated `ETLLog` table.
   - Example Log Table:
     ```sql
     CREATE TABLE ETLLog (
       LogID INT IDENTITY(1,1) PRIMARY KEY,
       ProcessName VARCHAR(100),
       StartTime DATETIME,
       EndTime DATETIME,
       Status VARCHAR(50),
       ErrorMessage VARCHAR(MAX)
     );
     ```
3. Notify stakeholders via email or dashboard for failures.

---

### **7. Example ETL Workflow**

1. Extract:
   - Query `SalesDB.Orders` for records with `LastModifiedDate > @LastRunDate`.
2. Transform:
   - Replace `CustomerID` with surrogate keys from `DimCustomer`.
3. Load:
   - Insert rows into `FactSales`.

