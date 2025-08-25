CREATE TABLE IF NOT EXISTS booking_competitor_data (
    id SERIAL PRIMARY KEY,
    hotel_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    price_display VARCHAR(50),
    price_numeric NUMERIC(10,2) CHECK (price_numeric >= 0),
    rating NUMERIC(2,1) CHECK (rating >= 0 AND rating <= 10),
    review_count TEXT,
    review_count_numeric INTEGER CHECK (review_count_numeric >= 0),
    scrape_time TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_location ON booking_competitor_data(location);
CREATE INDEX IF NOT EXISTS idx_price ON booking_competitor_data(price_numeric);

