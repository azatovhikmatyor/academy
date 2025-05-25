-- DDL Script for Data Warehouse (DW) in SQL Server

-- Table: DimDate (Date Dimension)
CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY, -- Format: YYYYMMDD
    FullDate DATE NOT NULL,
    Day INT NOT NULL,
    Month INT NOT NULL,
    Year INT NOT NULL,
    DayOfWeek INT NOT NULL,
    DayName NVARCHAR(20) NOT NULL,
    MonthName NVARCHAR(20) NOT NULL,
    Quarter INT NOT NULL,
    IsWeekend BIT NOT NULL
);

-- Table: DimCustomer (Customer Dimension)
CREATE TABLE DimCustomer (
    CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT NOT NULL UNIQUE,
    FullName NVARCHAR(100),
    Email NVARCHAR(100),
    ContactNumber NVARCHAR(15),
    LoyaltyPoints INT
);

-- Table: DimProduct (Product Dimension)
CREATE TABLE DimProduct (
    ProductKey INT IDENTITY(1,1) PRIMARY KEY,
    ProductID INT NOT NULL UNIQUE,
    ProductName NVARCHAR(100) NOT NULL,
    CategoryName NVARCHAR(100),
    SupplierName NVARCHAR(100),
    Price DECIMAL(10, 2) NOT NULL
);

-- Table: DimEmployee (Employee/User Dimension)
CREATE TABLE DimEmployee (
    EmployeeKey INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL UNIQUE,
    Username NVARCHAR(50),
    FullName NVARCHAR(100),
    Role NVARCHAR(50)
);

-- Table: FactSales (Fact Table for Sales)
CREATE TABLE FactSales (
    SalesKey INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL UNIQUE,
    OrderDateKey INT NOT NULL FOREIGN KEY REFERENCES DimDate(DateKey),
    CustomerKey INT FOREIGN KEY REFERENCES DimCustomer(CustomerKey),
    EmployeeKey INT FOREIGN KEY REFERENCES DimEmployee(EmployeeKey),
    TotalAmount DECIMAL(10, 2) NOT NULL,
    PaymentMethod NVARCHAR(50),
    Quantity INT NOT NULL,
    ProductKey INT FOREIGN KEY REFERENCES DimProduct(ProductKey),
    Revenue DECIMAL(10, 2) AS (Quantity * TotalAmount) PERSISTED
);

-- Table: FactInventory (Fact Table for Inventory Transactions)
CREATE TABLE FactInventory (
    InventoryKey INT IDENTITY(1,1) PRIMARY KEY,
    ProductKey INT NOT NULL FOREIGN KEY REFERENCES DimProduct(ProductKey),
    TransactionDateKey INT NOT NULL FOREIGN KEY REFERENCES DimDate(DateKey),
    TransactionType NVARCHAR(50),
    QuantityChanged INT NOT NULL,
    UserKey INT FOREIGN KEY REFERENCES DimEmployee(EmployeeKey)
);
