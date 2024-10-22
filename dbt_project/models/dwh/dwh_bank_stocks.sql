SELECT
    JSONExtract(_airbyte_data, 'symbol', 'String') AS symbol,
    JSONExtract(_airbyte_data, 'company_name', 'String') AS company_name,
    JSONExtract(_airbyte_data, 'last_price', 'Float64') AS last_price,
    JSONExtract(_airbyte_data, 'change', 'Float64') AS change,
    JSONExtract(_airbyte_data, '%_change', 'String') AS percentage_change,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'market_time', 'String')) AS market_time,
    JSONExtract(_airbyte_data, 'volume', 'String') AS volume,
    JSONExtract(_airbyte_data, 'avg_vol_3_month', 'String') AS avg_vol_3_month,
    JSONExtract(_airbyte_data, 'market_cap', 'String') AS market_cap,
    _airbyte_extracted_at
FROM stage.public_raw__stream_banks_stocks
