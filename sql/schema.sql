CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;
CREATE TABLE IF NOT EXISTS sessions (
 session_id VARCHAR(16) PRIMARY KEY,
 session_date DATE NOT NULL,
 device VARCHAR(30) NOT NULL,
 channel VARCHAR(40) NOT NULL,
 country VARCHAR(60) NOT NULL,
 landing_page VARCHAR(30) NOT NULL,
 page_views INT NOT NULL DEFAULT 0,
 session_seconds DECIMAL(10,1) NOT NULL DEFAULT 0,
 cart_adds INT NOT NULL DEFAULT 0,
 converted TINYINT NOT NULL DEFAULT 0,
 order_value DECIMAL(10,2) NOT NULL DEFAULT 0
);

-- Overall conversion rate
SELECT COUNT(*) sessions, SUM(converted) conversions,
 ROUND(100*SUM(converted)/NULLIF(COUNT(*),0),2) conversion_rate_pct,
 ROUND(SUM(order_value),2) revenue FROM sessions;

-- By marketing channel
SELECT channel, COUNT(*) sessions, SUM(converted) conversions,
 ROUND(100*SUM(converted)/NULLIF(COUNT(*),0),2) conversion_rate_pct,
 ROUND(SUM(order_value),2) revenue
FROM sessions GROUP BY channel ORDER BY conversion_rate_pct DESC;

-- By device
SELECT device, COUNT(*) sessions, SUM(converted) conversions,
 ROUND(100*SUM(converted)/NULLIF(COUNT(*),0),2) conversion_rate_pct
FROM sessions GROUP BY device ORDER BY conversion_rate_pct DESC;

-- Daily trend
SELECT session_date, COUNT(*) sessions, SUM(converted) conversions,
 ROUND(100*SUM(converted)/NULLIF(COUNT(*),0),2) conversion_rate_pct,
 ROUND(SUM(order_value),2) revenue
FROM sessions GROUP BY session_date ORDER BY session_date;
