WITH daily_data AS (
    SELECT 
        JSONExtractString(_airbyte_data, 'symbol') AS symbol,
        toMonth(parseDateTimeBestEffort(JSONExtractString(_airbyte_data, 'Date'))) AS month,
        ROUND(AVG(CAST(JSONExtractString(_airbyte_data, 'Open') AS Float64)), 2) AS avg_open,
        ROUND(AVG(CAST(JSONExtractString(_airbyte_data, 'Close') AS Float64)), 2) AS avg_close,
        ROUND(AVG(CAST(JSONExtractString(_airbyte_data, 'Volume') AS Float64)), 2) AS avg_volume
    FROM 
        raw.stage_raw__stream_sa_daily_stock_prices
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