CREATE DATABASE RealEstateSalesSql;
USE RealEstateSalesSql;
CREATE TABLE real_estate_sales_2001_2020_gl (
  serial_number INT,
  list_year INT,
  Town VARCHAR(255),
  assessed_value FLOAT,
  sale_amount FLOAT,
  gain_loss FLOAT,
  sale_rankings VARCHAR(255),
  sales_ratio FLOAT,
  property_type VARCHAR(255),
  residential_type VARCHAR(255),
  longitude FLOAT,
  latitude FLOAT
);
-- load data into the table
LOAD DATA LOCAL INFILE 'D:/RWorkshop/Real_Estate_Sales_2001-2020_GL.csv'
INTO TABLE real_estate_sales_2001_2020_gl
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Show information about the real_estate_sales_2001-2020_gl table
describe `real_estate_sales_2001_2020_gl`;

-- Select the first 10 rows of the real_estate_sales_2001-2020_gl table
SELECT * FROM `real_estate_sales_2001_2020_gl` LIMIT 10;

-- Select all rows where Town is 'Greenwich'
SELECT * FROM `real_estate_sales_2001_2020_gl` WHERE Town = 'Greenwich';


-- Select all rows in descending order by Assessed Value
SELECT * FROM `real_estate_sales_2001_2020_gl` ORDER BY `Assessed Value` DESC;

-- Select the average Sale Amount of all rows
SELECT AVG(`Sale Amount`) FROM `real_estate_sales_2001_2020_gl`;


-- Select the count of rows where Residential Type is not null
SELECT COUNT(*) FROM `real_estate_sales_2001_2020_gl` WHERE `Residential Type` IS NOT NULL;

-- Select the count of rows for each Sale Rankings value
SELECT `Sale Rankings`, COUNT(*) as Count
FROM `real_estate_sales_2001_2020_gl`
GROUP BY `Sale Rankings`;


