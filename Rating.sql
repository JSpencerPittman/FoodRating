CREATE TABLE customer (
    cust_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    psswd VARCHAR(255) NOT NULL,
    fname VARCHAR(255) NOT NULL,
    mname VARCHAR(255),
    lname VARCHAR(255) NOT NULL
);

CREATE TABLE company (
    company_id SERIAL PRIMARY KEY,
    comp_name VARCHAR(255) UNIQUE,
    comp_type VARCHAR(255),
    CHECK (comp_type IS NULL OR comp_type IN ('Restaurant','Fast Food'))
);

CREATE TABLE site (
    site_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES company(company_id),
    state VARCHAR(255) NOT NULL,
    street VARCHAR(255),
    addr_num INT,
    zip INT NOT NULL
);

CREATE TABLE food (
    food_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES company(company_id),
    food_name VARCHAR(255) NOT NULL,
    cuisine VARCHAR(255)
	CHECK (cuisine IS NULL OR cuisine IN ('American','Italian','Mexican','Ice Cream'))
);


CREATE TABLE rating (
    rating_id SERIAL PRIMARY KEY,
    food_id INTEGER REFERENCES food(food_id),
    site_id INTEGER REFERENCES site(site_id),
    cust_id INTEGER REFERENCES customer(cust_id),
    price DECIMAL,
    rating INTEGER NOT NULL,
    date DATE DEFAULT CURRENT_DATE
);

-- Validation Operations

CREATE OR REPLACE FUNCTION valid_user(inp_email VARCHAR, inp_password VARCHAR)
	RETURNS int
	LANGUAGE plpgsql
AS $$
DECLARE
	val_cust_id int;
BEGIN
	SELECT cust_id
	INTO val_cust_id
	FROM customer
	WHERE psswd=inp_password AND email=inp_email;
	
	IF (val_cust_id IS NULL) THEN
		val_cust_id = -1;
	END IF;
	
	RETURN val_cust_id;
END; 
$$;

-- Existence Operations

CREATE OR REPLACE FUNCTION user_exists(inp_email VARCHAR)
	RETURNS bool
	LANGUAGE plpgsql
AS $$
DECLARE
	matches int;
BEGIN
	SELECT COUNT(*)
	INTO matches
	FROM customer
	WHERE email=inp_email;
	
	RETURN matches > 0;
END;
$$;


CREATE OR REPLACE FUNCTION company_exists(inp_comp_name VARCHAR)
	RETURNS bool
	LANGUAGE plpgsql
AS $$
DECLARE
	matches int;
BEGIN
	SELECT COUNT(*)
	INTO matches
	FROM company
	WHERE comp_name=inp_comp_name;
	
	RETURN matches > 0;
END;
$$;

CREATE OR REPLACE FUNCTION site_exists(inp_comp_id INT, inp_state VARCHAR, inp_street VARCHAR, inp_addr_num INT, inp_zip INT)
	RETURNS bool
	LANGUAGE plpgsql
AS $$
DECLARE
	matches int;
BEGIN
	SELECT COUNT(*)
	INTO matches
	FROM site
	WHERE company_id=inp_comp_id AND
		  state=inp_state AND
		  street IS NOT DISTINCT FROM inp_street AND
		  addr_num IS NOT DISTINCT FROM inp_addr_num AND
		  zip=inp_zip;
	
	RETURN matches > 0;
END;
$$;

CREATE OR REPLACE FUNCTION food_exists(inp_comp_id INT, inp_food_name VARCHAR)
	RETURNS bool
	LANGUAGE plpgsql
AS $$
DECLARE
	matches int;
BEGIN	  
	SELECT COUNT(*)
	INTO matches
	FROM food
	WHERE company_id=inp_comp_id AND
		food_name=inp_food_name;
	
	RETURN matches > 0;
END;
$$;

CREATE OR REPLACE FUNCTION rating_exists(inp_food_id INT, inp_site_id INT, inp_cust_id INT)
	RETURNS bool
	LANGUAGE plpgsql
AS $$
DECLARE
	matches int;
BEGIN	  
	SELECT COUNT(*)
	INTO matches
	FROM rating
	WHERE food_id=inp_food_id AND
		site_id=inp_site_id AND
		cust_id=inp_cust_id;
	
	RETURN matches > 0;
END;
$$;

-- Insertion Operations

DROP FUNCTION add_user;

CREATE OR REPLACE FUNCTION add_user(inp_email VARCHAR, inp_psswd VARCHAR, inp_fname VARCHAR, inp_mname VARCHAR, inp_lname VARCHAR)
	RETURNS INT 
	LANGUAGE plpgsql
AS $$
DECLARE
	new_cust_id INT;
BEGIN
    INSERT INTO customer (email, psswd, fname, mname, lname) VALUES (inp_email, inp_psswd, inp_fname, inp_mname, inp_lname);
	
	SELECT cust_id
	INTO new_cust_id
	FROM customer
	WHERE email=inp_email;
	
	RETURN new_cust_id;
END;
$$;

CREATE OR REPLACE FUNCTION add_company(inp_comp_name VARCHAR, inp_comp_type VARCHAR)
    RETURNS INT
    LANGUAGE 'plpgsql'
AS $$
DECLARE 
	actual_comp_type VARCHAR;
	new_comp_id INT;
BEGIN
	IF inp_comp_type = 'Other' THEN
		actual_comp_type = NULL;
	ELSE
		actual_comp_type = inp_comp_type;
	END IF;
    
	INSERT INTO company (comp_name, comp_type) VALUES
	(inp_comp_name, actual_comp_type);
	
	SELECT company_id
	INTO new_comp_id
	FROM company
	WHERE comp_name=inp_comp_name;
	
	RETURN new_comp_id;
END $$;

CREATE OR REPLACE FUNCTION add_site(inp_comp_id INT, inp_state VARCHAR, inp_street VARCHAR, inp_addr_num INT, inp_zip INT)
    RETURNS INT
    LANGUAGE 'plpgsql'
AS $$
DECLARE 
	new_site_id INT;
BEGIN
	INSERT INTO site (company_id, state, street, addr_num, zip) VALUES
	(inp_comp_id, inp_state, inp_street, inp_addr_num, inp_zip);
	
	SELECT site_id
	INTO new_site_id
	FROM site
	WHERE company_id=inp_comp_id AND
		  state=inp_state AND
		  street IS NOT DISTINCT FROM inp_street AND
		  addr_num IS NOT DISTINCT FROM inp_addr_num AND
		  zip=inp_zip;
	
	RETURN new_site_id;
END $$;


CREATE OR REPLACE FUNCTION add_food(inp_comp_id INT, inp_food_name VARCHAR, inp_cuisine VARCHAR)
    RETURNS INT
    LANGUAGE 'plpgsql'
AS $$
DECLARE 
	actual_cusine VARCHAR;
	new_food_id INT;
BEGIN
	IF inp_cuisine = 'Other' THEN
		actual_cusine = NULL;
	ELSE
		actual_cusine = inp_cuisine;
	END IF;
    
	INSERT INTO food (company_id, food_name, cuisine) VALUES
	(inp_comp_id, inp_food_name, inp_cuisine);
	
	SELECT food_id
	INTO new_food_id
	FROM food
	WHERE company_id=inp_comp_id AND
		food_name=inp_food_name AND
		cuisine IS NOT DISTINCT FROM inp_cuisine;
	
	RETURN new_food_id;
END $$;

CREATE OR REPLACE FUNCTION add_rating(inp_food_id INT, inp_site_id INT, inp_cust_id INT, price DECIMAL, rating INT)
    RETURNS VOID
    LANGUAGE 'plpgsql'
AS $$
BEGIN
	INSERT INTO rating (food_id, site_id, cust_id, price, rating) VALUES
	(inp_food_id, inp_site_id, inp_cust_id, price, rating);
END $$;


-- Select Operations

CREATE OR REPLACE FUNCTION top_food_items(cnt int)
	RETURNS TABLE(food_name VARCHAR, avg_rating DECIMAL)
	LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	SELECT F.food_name, AVG(rating) AS avg_rating
	FROM food F
	INNER JOIN rating R USING(food_id)
	GROUP BY food_id
	ORDER BY avg_rating DESC
	LIMIT cnt;
END;
$$;

CREATE OR REPLACE FUNCTION top_companies(cnt int)
	RETURNS TABLE(comp_name VARCHAR, avg_rating DECIMAL)
	LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	SELECT tC.comp_name, AVG(rating) AS avg_rating
	FROM company tC
	INNER JOIN site tS USING(company_id)
	INNER JOIN rating tR using(site_id)
	GROUP BY company_id
	ORDER BY avg_rating DESC
	LIMIT cnt;
END;
$$;

CREATE OR REPLACE FUNCTION food_entries()
	RETURNS TABLE(food_name VARCHAR, comp_name VARCHAR, num_ratings BIGINT, avg_rating DECIMAL)
	LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	SELECT tF.food_name, tC.comp_name, COUNT(*) AS num_ratings, AVG(rating) AS avg_rating 
	FROM food tF
	INNER JOIN company tC USING(company_id)
	INNER JOIN rating USING(food_id)
	GROUP BY food_id, tF.food_name, tC.comp_name
	ORDER BY tF.food_name;
END;
$$;