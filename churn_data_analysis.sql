CREATE DATABASE churn_db;

USE churn_db;


SELECT * FROM churn_db.claned_telco_churn;


-- 1️⃣ Churn Rate (KPI)
SELECT 
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
    2) AS churn_rate_percentage
FROM churn_db.claned_telco_churn;

-- 2️⃣ Churn by Contract Type
SELECT 
    contract, 
    churn, 
    COUNT(*) AS total_customers
FROM churn_db.claned_telco_churn
GROUP BY contract, churn
ORDER BY contract;


-- 3️⃣ Monthly Charges vs Churn
SELECT 
    churn, 
    ROUND(AVG(monthlycharges), 2) AS avg_monthly_charges
FROM churn_db.claned_telco_churn
GROUP BY churn;


-- 4️⃣ Tenure Analysis (Customer Retention)
SELECT 
    CASE 
        WHEN tenure < 12 THEN '0-1 Year'
        WHEN tenure BETWEEN 12 AND 24 THEN '1-2 Years'
        ELSE '2+ Years'
    END AS tenure_group,
    churn,
    COUNT(*) AS total_customers
FROM churn_db.claned_telco_churn
GROUP BY tenure_group, churn
ORDER BY tenure_group;


-- 5️⃣ Payment Method Impact on Churn
SELECT 
    paymentmethod, 
    churn, 
    COUNT(*) AS total_customers
FROM churn_db.claned_telco_churn
GROUP BY paymentmethod, churn
ORDER BY paymentmethod;


-- 6️⃣ Internet Service Impact
SELECT 
    internetservice, 
    churn, 
    COUNT(*) AS total_customers
FROM churn_db.claned_telco_churn
GROUP BY internetservice, churn;

-- 7️⃣ High Revenue Customers Who Churned
SELECT 
    customerid, 
    monthlycharges, 
    totalcharges
FROM churn_db.claned_telco_churn
WHERE churn = 'Yes'
ORDER BY totalcharges DESC
LIMIT 10;


-- 8️⃣ Window Function (Ranking High Paying Customers)
SELECT 
    customerid,
    monthlycharges,
    RANK() OVER (ORDER BY monthlycharges DESC) AS rank_highest_charges
FROM churn_db.claned_telco_churn;


-- 7. KPI Metrics (Important for Dashboard)

-- 1. Total Customers
SELECT COUNT(*) AS total_customers
FROM churn_db.claned_telco_churn;

-- 2. Total of churned_customers
SELECT SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers
FROM churn_db.claned_telco_churn;

-- 3. avg_monthly_charges
SELECT ROUND(AVG(monthlycharges), 2) AS avg_monthly_charges
FROM churn_db.claned_telco_churn;

-- 4. avg_total_charges
SELECT ROUND(AVG(totalcharges), 2) AS avg_total_charges
FROM churn_db.claned_telco_churn;

