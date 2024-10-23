SELECT
    JSONExtract(_airbyte_data, 'symbol', 'String') AS symbol,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'date_reported', 'String')) AS date_reported,
    JSONExtract(_airbyte_data, 'holder', 'String') AS holder,
    JSONExtract(_airbyte_data, 'shares', 'Int64') AS shares,
    JSONExtract(_airbyte_data, 'value', 'Float64') AS value,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'created_at', 'String')) AS created_at,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'updated_at', 'String')) AS updated_at,
    _airbyte_extracted_at
FROM stage.public_raw__stream_stock_holders
