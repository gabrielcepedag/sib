WITH daily_data AS (
    SELECT 
        symbol,
        toMonth(date) AS month,
        ROUND(AVG(open), 2) AS avg_open,
        ROUND(AVG(close), 2) AS avg_close,
        ROUND(AVG(volume), 2) AS avg_volume
    FROM 
         {{ ref('dwh_daily_stocks_prices') }}
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