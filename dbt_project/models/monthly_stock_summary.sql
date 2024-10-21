WITH daily_data AS (
    SELECT 
        JSONExtractString(_airbyte_data, 'symbol') AS symbol,
        toMonth(parseDateTimeBestEffort(JSONExtractString(_airbyte_data, 'date'))) AS month,
        ROUND(AVG(CAST(JSONExtractString(_airbyte_data, 'open') AS Float64)), 2) AS avg_open,
        ROUND(AVG(CAST(JSONExtractString(_airbyte_data, 'close') AS Float64)), 2) AS avg_close,
        ROUND(AVG(CAST(JSONExtractString(_airbyte_data, 'volume') AS Float64)), 2) AS avg_volume
    FROM 
        dwh.dwh_raw__stream_daily_stock_prices
    GROUP BY 
        symbol, month
    ORDER BY 
        symbol, month
)

SELECT 
    symbol,
    month,
    avg_open,
    avg_close,
    avg_volume
FROM 
    daily_data
ORDER BY 
    month, symbol