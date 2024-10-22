SELECT
    JSONExtract(_airbyte_data, 'symbol', 'String') AS symbol,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'gradedate', 'String')) AS gradedate,
    JSONExtract(_airbyte_data, 'firm', 'String') AS firm,
    JSONExtract(_airbyte_data, 'tograde', 'String') AS tograde,
    JSONExtract(_airbyte_data, 'fromgrade', 'String') AS fromgrade,
    JSONExtract(_airbyte_data, 'action', 'String') AS action,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'created_at', 'String')) AS created_at,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'updated_at', 'String')) AS updated_at,
    _airbyte_extracted_at
FROM stage.public_raw__stream_stocks_calificadores
