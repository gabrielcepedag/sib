SELECT
    JSONExtract(_airbyte_data, 'symbol', 'String') AS symbol,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'date', 'String')) AS date,
    JSONExtract(_airbyte_data, 'open', 'Float64') AS open,
    JSONExtract(_airbyte_data, 'high', 'Float64') AS high,
    JSONExtract(_airbyte_data, 'low', 'Float64') AS low,
    JSONExtract(_airbyte_data, 'close', 'Float64') AS close,
    JSONExtract(_airbyte_data, 'volume', 'Float64') AS volume,
    JSONExtract(_airbyte_data, 'dividends', 'Float64') AS dividends,
    JSONExtract(_airbyte_data, 'stock_splits', 'Float64') AS stock_splits,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'created_at', 'String')) AS created_at,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'updated_at', 'String')) AS updated_at,
    _airbyte_extracted_at
FROM stage.public_raw__stream_daily_stocks_prices