SELECT
    JSONExtract(_airbyte_data, 'symbol', 'String') AS symbol,
    JSONExtract(_airbyte_data, 'assets', 'Float64') AS assets,
    JSONExtract(_airbyte_data, 'debt', 'Float64') AS debt,
    JSONExtract(_airbyte_data, 'invested_capital', 'Float64') AS invested_capital,
    JSONExtract(_airbyte_data, 'shares_issued', 'Float64') AS shares_issued,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'created_at', 'String')) AS created_at,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'updated_at', 'String')) AS updated_at,
    _airbyte_extracted_at
FROM stage.public_raw__stream_bank_fundamentals