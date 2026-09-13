-- ================================================================
-- MySQL SCHEMA — company database
-- ================================================================
-- MySQL install karne ke baad ye chalao:
--
--   mysql -u root -p < phase3_database/schema_mysql.sql
--
-- Ya MySQL Workbench me poora file paste karke run karo.
--
-- Ye wahi structure hai jo SQLite practice.db me hai.
-- EMS project isi schema pe chalta hai.
-- ================================================================

DROP DATABASE IF EXISTS company;
CREATE DATABASE company CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE company;


-- ================================================================
-- TABLE: departments
-- ================================================================
CREATE TABLE departments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    location        VARCHAR(100),
    budget          DECIMAL(12,2),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


-- ================================================================
-- TABLE: employees
--   - 1:N with departments  (ek dept me kai employees)
--   - SELF reference for manager (employee -> manager)
-- ================================================================
CREATE TABLE employees (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(120) UNIQUE,
    salary        DECIMAL(10,2) CHECK (salary >= 0),
    department_id INT,
    manager_id    INT,
    hire_date     DATE,
    city          VARCHAR(50),
    status        VARCHAR(20) DEFAULT 'Active',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_emp_dept
        FOREIGN KEY (department_id) REFERENCES departments(id)
        ON DELETE SET NULL ON UPDATE CASCADE,

    CONSTRAINT fk_emp_manager
        FOREIGN KEY (manager_id) REFERENCES employees(id)
        ON DELETE SET NULL,

    INDEX idx_emp_salary (salary),
    INDEX idx_emp_dept   (department_id),
    INDEX idx_emp_city   (city),
    INDEX idx_emp_name   (name)
) ENGINE=InnoDB;


-- ================================================================
-- TABLE: projects
-- ================================================================
CREATE TABLE projects (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    budget       DECIMAL(12,2),
    start_date   DATE,
    end_date     DATE,
    status       ENUM('Planning','Active','On Hold','Completed') DEFAULT 'Planning'
) ENGINE=InnoDB;


-- ================================================================
-- TABLE: assignments  (M:N junction table)
--   Ek employee kai projects me, ek project me kai employees
--   COMPOSITE PRIMARY KEY se duplicate assignment nahi ho sakti
-- ================================================================
CREATE TABLE assignments (
    employee_id INT NOT NULL,
    project_id  INT NOT NULL,
    hours       INT DEFAULT 0,
    role        VARCHAR(60),
    assigned_on DATE DEFAULT (CURRENT_DATE),

    PRIMARY KEY (employee_id, project_id),

    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id)  REFERENCES projects(id)  ON DELETE CASCADE
) ENGINE=InnoDB;


-- ================================================================
-- TABLE: customers / products / orders
-- ================================================================
CREATE TABLE customers (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(120) NOT NULL,
    email   VARCHAR(120),
    city    VARCHAR(60),
    country VARCHAR(60) DEFAULT 'India'
) ENGINE=InnoDB;

CREATE TABLE products (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(120) NOT NULL,
    category VARCHAR(60),
    price    DECIMAL(10,2) CHECK (price >= 0),
    stock    INT DEFAULT 0,
    INDEX idx_prod_category (category)
) ENGINE=InnoDB;

CREATE TABLE orders (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id  INT,
    quantity    INT DEFAULT 1,
    order_date  DATE,
    amount      DECIMAL(12,2),

    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id)  REFERENCES products(id)  ON DELETE RESTRICT,

    INDEX idx_order_date (order_date),
    INDEX idx_order_cust (customer_id)
) ENGINE=InnoDB;


-- ================================================================
-- SAMPLE DATA
-- ================================================================

INSERT INTO departments (id, department_name, location, budget) VALUES
 (1, 'IT',        'Hyderabad', 5000000),
 (2, 'HR',        'Mumbai',    1500000),
 (3, 'Sales',     'Delhi',     3000000),
 (4, 'Finance',   'Mumbai',    2500000),
 (5, 'Marketing', 'Bangalore', 2000000);

INSERT INTO employees (id, name, email, salary, department_id, manager_id, hire_date, city) VALUES
 (1,  'Rajesh Kumar',  'rajesh@techcorp.com',  120000, 1,    NULL, '2018-01-15', 'Hyderabad'),
 (2,  'Priya Sharma',  'priya@techcorp.com',   110000, 2,    NULL, '2018-03-20', 'Mumbai'),
 (3,  'Noman Syed',    'noman@techcorp.com',    30000, 1,    1,    '2026-01-10', 'Hyderabad'),
 (4,  'Zoya Khan',     'zoya@techcorp.com',     38000, NULL, NULL, '2025-06-01', 'Delhi'),
 (5,  'Ali Ahmed',     'ali@techcorp.com',      45000, 2,    2,    '2023-04-12', 'Mumbai'),
 (6,  'Sara Fatima',   'sara@techcorp.com',     52000, 1,    1,    '2022-08-05', 'Hyderabad'),
 (7,  'Vikram Singh',  'vikram@techcorp.com',   67000, 3,    NULL, '2020-02-18', 'Delhi'),
 (8,  'Anjali Rao',    'anjali@techcorp.com',   48000, 3,    7,    '2023-11-30', 'Delhi'),
 (9,  'Imran Ali',     'imran@techcorp.com',    41000, 3,    7,    '2024-01-22', 'Mumbai'),
 (10, 'Deepak Verma',  'deepak@techcorp.com',   95000, 4,    NULL, '2019-05-14', 'Mumbai'),
 (11, 'Sneha Patel',   'sneha@techcorp.com',    58000, 4,    10,   '2022-09-01', 'Mumbai'),
 (12, 'Arjun Nair',    'arjun@techcorp.com',    72000, 1,    1,    '2021-03-08', 'Bangalore'),
 (13, 'Kavya Reddy',   'kavya@techcorp.com',    64000, 5,    NULL, '2021-07-19', 'Bangalore'),
 (14, 'Rohit Mehta',   'rohit@techcorp.com',    39000, 5,    13,   '2024-05-25', 'Bangalore'),
 (15, 'Fatima Sheikh', 'fatima@techcorp.com',   55000, 1,    1,    '2022-12-11', 'Hyderabad'),
 (16, 'Suresh Babu',   'suresh@techcorp.com',   43000, 3,    7,    '2023-06-17', 'Hyderabad'),
 (17, 'Meera Joshi',   'meera@techcorp.com',    88000, 4,    10,   '2020-10-03', 'Delhi'),
 (18, 'Karan Malhotra','karan@techcorp.com',    35000, 5,    13,   '2025-02-14', 'Delhi'),
 (19, 'Aisha Begum',   'aisha@techcorp.com',      NULL, 1,   1,    '2026-02-01', 'Hyderabad'),
 (20, 'Rahul Gupta',   'rahul@techcorp.com',      NULL, NULL, NULL, '2026-03-01', 'Pune');

INSERT INTO projects (id, project_name, budget, start_date, end_date, status) VALUES
 (1, 'E-Commerce Platform', 1500000, '2025-01-01', '2026-06-30', 'Active'),
 (2, 'Mobile Banking App',  2000000, '2025-03-15', '2026-09-30', 'Active'),
 (3, 'HR Portal',            500000, '2024-06-01', '2025-03-31', 'Completed'),
 (4, 'Data Warehouse',      1800000, '2025-08-01', '2026-12-31', 'Active'),
 (5, 'CRM System',           900000, '2024-01-10', '2024-12-20', 'Completed'),
 (6, 'AI Chatbot',           750000, '2026-01-05', '2026-08-31', 'Active'),
 (7, 'Legacy Migration',     600000, '2025-05-01', NULL,         'On Hold'),
 (8, 'Analytics Dashboard',  450000, '2026-02-01', NULL,         'Planning');

INSERT INTO assignments (employee_id, project_id, hours, role) VALUES
 (3, 1, 160, 'Developer'),        (6, 1, 180, 'Senior Developer'),
 (12, 1, 200, 'Tech Lead'),       (15, 2, 170, 'Developer'),
 (1, 2, 120, 'Architect'),        (6, 2, 140, 'Senior Developer'),
 (5, 3, 100, 'HR Analyst'),       (2, 3, 80,  'Project Manager'),
 (12, 4, 190, 'Tech Lead'),       (3, 4, 150, 'Developer'),
 (17, 4, 110, 'Data Analyst'),    (13, 5, 130, 'Marketing Lead'),
 (14, 5, 90,  'Associate'),       (15, 6, 160, 'Developer'),
 (1, 6, 100, 'Architect');

INSERT INTO customers (id, name, email, city, country) VALUES
 (1, 'Amit Traders',    'amit@trade.com',    'Hyderabad', 'India'),
 (2, 'Beta Retail',     'info@beta.com',     'Mumbai',    'India'),
 (3, 'Global Supplies', 'sales@global.com',  'Delhi',     'India'),
 (4, 'Kiran Stores',    'kiran@stores.com',  'Chennai',   'India'),
 (5, 'Modern Mart',     NULL,                'Bangalore', 'India'),
 (6, 'Nova Enterprise', 'nova@ent.com',      'Pune',      'India'),
 (7, 'Star Wholesale',  'star@whole.com',    'Kolkata',   'India'),
 (8, 'Zenith Corp',     'zenith@corp.com',   'Dubai',     'UAE');

INSERT INTO products (id, name, category, price, stock) VALUES
 (1,'Laptop','Electronics',55000,25),      (2,'Mouse','Electronics',700,200),
 (3,'Keyboard','Electronics',1500,150),    (4,'Monitor','Electronics',12000,40),
 (5,'Office Chair','Furniture',8500,30),   (6,'Desk','Furniture',15000,20),
 (7,'Notebook','Stationery',60,500),       (8,'Pen Set','Stationery',250,300),
 (9,'Headphones','Electronics',3200,80),   (10,'Webcam','Electronics',2800,0);

INSERT INTO orders (id, customer_id, product_id, quantity, order_date, amount) VALUES
 (1,1,1,2,'2026-01-05',110000),   (2,1,2,5,'2026-01-05',3500),
 (3,2,4,3,'2026-01-12',36000),    (4,3,1,1,'2026-01-20',55000),
 (5,2,5,4,'2026-02-02',34000),    (6,6,9,2,'2026-02-14',6400),
 (7,1,6,1,'2026-02-18',15000),    (8,7,3,10,'2026-03-01',15000),
 (9,3,7,50,'2026-03-07',3000),    (10,2,1,1,'2026-03-15',55000),
 (11,6,8,20,'2026-04-02',5000),   (12,7,4,2,'2026-04-10',24000);


-- ================================================================
-- VERIFY
-- ================================================================
SELECT 'departments' AS table_name, COUNT(*) AS rows_count FROM departments
UNION ALL SELECT 'employees',  COUNT(*) FROM employees
UNION ALL SELECT 'projects',   COUNT(*) FROM projects
UNION ALL SELECT 'assignments',COUNT(*) FROM assignments
UNION ALL SELECT 'customers',  COUNT(*) FROM customers
UNION ALL SELECT 'products',   COUNT(*) FROM products
UNION ALL SELECT 'orders',     COUNT(*) FROM orders;

SHOW TABLES;
DESCRIBE employees;
SHOW INDEX FROM employees;


-- ================================================================
-- FOREIGN KEY TEST — ye fail hona CHAHIYE
-- ================================================================
-- Uncomment karke try karo, error aayega (yahi sahi hai):
--
--   INSERT INTO employees (name, department_id) VALUES ('Test', 999);
--   -- ERROR 1452: Cannot add or update a child row: FK constraint fails
--
-- Aur ye CHECK constraint todega:
--   INSERT INTO employees (name, salary) VALUES ('Test', -5000);
--   -- ERROR 3819: Check constraint violated
