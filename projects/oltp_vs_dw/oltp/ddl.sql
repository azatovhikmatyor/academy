-- DDL Script for OLTP Database in PostgreSQL

-- Table: Users
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    FullName VARCHAR(100) NOT NULL,
    ContactNumber VARCHAR(15)
);

-- Table: Customers
CREATE TABLE Customers (
    CustomerID SERIAL PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    ContactNumber VARCHAR(15),
    LoyaltyPoints INT DEFAULT 0
);

-- Table: Categories
CREATE TABLE Categories (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL UNIQUE
);

-- Table: Products
CREATE TABLE Products (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    CategoryID INT REFERENCES Categories(CategoryID) ON DELETE SET NULL,
    Price DECIMAL(10, 2) NOT NULL,
    QuantityInStock INT NOT NULL,
    Description TEXT
);

-- Table: Suppliers
CREATE TABLE Suppliers (
    SupplierID SERIAL PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    ContactNumber VARCHAR(15),
    Address TEXT
);

-- Table: Orders
CREATE TABLE Orders (
    OrderID SERIAL PRIMARY KEY,
    OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UserID INT REFERENCES Users(UserID) ON DELETE SET NULL,
    CustomerID INT REFERENCES Customers(CustomerID) ON DELETE SET NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    PaymentMethod VARCHAR(50) NOT NULL
);

-- Table: OrderDetails
CREATE TABLE OrderDetails (
    OrderDetailID SERIAL PRIMARY KEY,
    OrderID INT REFERENCES Orders(OrderID) ON DELETE CASCADE,
    ProductID INT REFERENCES Products(ProductID) ON DELETE RESTRICT,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL,
    TotalPrice DECIMAL(10, 2) GENERATED ALWAYS AS (Quantity * UnitPrice) STORED
);

-- Table: Payments
CREATE TABLE Payments (
    PaymentID SERIAL PRIMARY KEY,
    OrderID INT REFERENCES Orders(OrderID) ON DELETE CASCADE,
    PaymentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    AmountPaid DECIMAL(10, 2) NOT NULL,
    ChangeGiven DECIMAL(10, 2) NOT NULL
);

-- Table: Inventory
CREATE TABLE Inventory (
    InventoryID SERIAL PRIMARY KEY,
    ProductID INT REFERENCES Products(ProductID) ON DELETE RESTRICT,
    TransactionType VARCHAR(50) NOT NULL,
    QuantityChanged INT NOT NULL,
    TransactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UserID INT REFERENCES Users(UserID) ON DELETE SET NULL
);
