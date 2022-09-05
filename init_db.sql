CREATE TABLE bds_data (title varchar, price varchar, price_per_m2 varchar, area varchar, scraped_date varchar, url varchar );
CREATE TABLE bds_data_details (url varchar, details varchar);
CREATE TABLE bds_data_tasks (name varchar, status varchar, page integer);
CREATE TABLE bds_data_queues (task_name varchar, url varchar, queue_id varchar);