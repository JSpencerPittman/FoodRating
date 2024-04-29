CREATE TABLE customer (
    cust_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    fname VARCHAR(255),
    mname VARCHAR(255),
    lname VARCHAR(255)
);

CREATE TABLE company (
    company_no SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE site (
    site_id SERIAL PRIMARY KEY,
    company_no INTEGER REFERENCES company(company_no),
    state VARCHAR(255),
    street VARCHAR(255),
    address VARCHAR(255),
    zip VARCHAR(10)
);

CREATE TABLE food (
    food_no SERIAL PRIMARY KEY,
    company_no INTEGER REFERENCES company(company_no),
    name VARCHAR(255),
    cuisine VARCHAR(255)
);

CREATE TABLE rating (
    rating_id SERIAL PRIMARY KEY,
    food_no INTEGER REFERENCES food(food_no),
    site_id INTEGER REFERENCES site(site_id),
    cust_id INTEGER REFERENCES customer(cust_id),
    price DECIMAL,
    rating INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE OR REPLACE FUNCTION login(email VARCHAR, password VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    logged_in BOOLEAN;
    customer_record RECORD;
BEGIN
    SELECT INTO customer_record * FROM customer WHERE email = login.email;
    
    IF customer_record IS NOT NULL AND customer_record.password = login.password THEN
        logged_in := TRUE;
    ELSE
        logged_in := FALSE;
        RAISE NOTICE 'Failed login';
    END IF;
    
    RETURN logged_in;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION add_food(food_name VARCHAR, company_name VARCHAR, cuisine VARCHAR)
RETURNS VOID AS $$
DECLARE
    food_no INTEGER;
    company_no INTEGER;
BEGIN
    SELECT INTO food_no MAX(food_no) + 1 FROM food;
    SELECT INTO company_no company_no FROM company WHERE name = add_food.company_name;
    
    INSERT INTO food (food_no, company_no, name, cuisine) VALUES (food_no, company_no, food_name, cuisine);
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION add_company(company_name VARCHAR)
RETURNS VOID AS $$
DECLARE
    company_no INTEGER;
BEGIN
    SELECT INTO company_no MAX(company_no) + 1 FROM company;
    
    INSERT INTO company (company_no, name) VALUES (company_no, company_name);
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION add_site(company_name VARCHAR, state VARCHAR, street VARCHAR, address VARCHAR, zip VARCHAR)
RETURNS VOID AS $$
DECLARE
    company_no INTEGER;
    site_id INTEGER;
BEGIN
    SELECT INTO company_no company_no FROM company WHERE name = add_site.company_name;
    
    IF company_no IS NULL THEN
        RAISE EXCEPTION 'Company not found';
    END IF;
    
    SELECT INTO site_id MAX(site_id) + 1 FROM site;
    
    INSERT INTO site (site_id, company_no, state, street, address, zip) VALUES (site_id, company_no, state, street, address, zip);
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION add_rating(comp_name VARCHAR, food_name VARCHAR, price DECIMAL, rating INTEGER)
RETURNS VOID AS $$
DECLARE
    site_id INTEGER;
    comp_no INTEGER;
    food_no INTEGER;
    cust_id INTEGER;
    rating_id INTEGER;
BEGIN
    -- Check if user is logged in
    IF NOT logged_in() THEN
        RAISE EXCEPTION 'User not logged in';
    END IF;

    SELECT INTO comp_no company_no FROM company WHERE name = add_rating.comp_name;
    
    IF comp_no IS NULL THEN
        RAISE EXCEPTION 'Company not found';
    END IF;
    
    -- Select the site with the smallest ID
    SELECT INTO site_id MIN(site_id) FROM site WHERE company_no = comp_no;
    
    IF site_id IS NULL THEN
        RAISE EXCEPTION 'Site not found';
    END IF;
    
    SELECT INTO food_no food_no FROM food WHERE name = add_rating.food_name;
    
    IF food_no IS NULL THEN
        RAISE EXCEPTION 'Food not found';
    END IF;
    
    SELECT INTO cust_id cust_no FROM customer WHERE email = <retrieve from session>;
    
    SELECT INTO rating_id MAX(rating_id) + 1 FROM rating;
    
    INSERT INTO rating (rating_id, food_no, site_id, cust_id, price, rating) VALUES (rating_id, food_no, site_id, cust_id, price, rating);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION add_account(email VARCHAR, password VARCHAR, fname VARCHAR, mname VARCHAR, lname VARCHAR)
RETURNS VOID AS $$
DECLARE
    cust_id INTEGER;
BEGIN
    SELECT INTO cust_id MAX(cust_id) + 1 FROM customer;
    
    INSERT INTO customer (cust_id, email, password, fname, mname, lname) VALUES (cust_id, email, password, fname, mname, lname);
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION change_password(email VARCHAR, new_password VARCHAR)
RETURNS VOID AS $$
DECLARE
    user_record RECORD;
BEGIN
    SELECT INTO user_record * FROM customer WHERE email = change_password.email;
    
    IF user_record IS NULL THEN
        RAISE EXCEPTION 'User does not exist';
    END IF;
    
    IF new_password = user_record.password THEN
        RAISE EXCEPTION 'New password cannot be the same as the old password';
    END IF;
    
    UPDATE customer SET password = new_password WHERE email = change_password.email;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION average_rating(arg_type VARCHAR, arg_value VARCHAR)
RETURNS DECIMAL AS $$
DECLARE
    rating_sum DECIMAL;
    rating_count INTEGER;
BEGIN
    IF arg_type = 'company' THEN
        SELECT INTO rating_sum SUM(rating) FROM rating WHERE company = arg_value;
        SELECT INTO rating_count COUNT(rating) FROM rating WHERE company = arg_value;
        
        RETURN rating_sum / rating_count;
        
    ELSEIF arg_type = 'food' THEN
        SELECT INTO rating_sum SUM(rating) FROM rating WHERE food = arg_value;
        SELECT INTO rating_count COUNT(rating) FROM rating WHERE food = arg_value;
        
        RETURN rating_sum / rating_count;
        
    ELSE
        RAISE EXCEPTION 'Invalid argument type';
    END IF;
END;
$$ LANGUAGE plpgsql;


-- Path: back/foodrating/foodrating/foodrating/Rating.sql