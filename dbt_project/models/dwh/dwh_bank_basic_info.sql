SELECT
    JSONExtract(_airbyte_data, 'symbol', 'String') AS symbol,
    JSONExtract(_airbyte_data, 'company_name', 'String') AS company_name,
    JSONExtract(_airbyte_data, 'industry', 'String') AS industry,
    JSONExtract(_airbyte_data, 'sector', 'String') AS sector,
    JSONExtract(_airbyte_data, 'employee_count', 'Int32') AS employee_count,
    JSONExtract(_airbyte_data, 'city', 'String') AS city,
    JSONExtract(_airbyte_data, 'phone', 'String') AS phone,
    JSONExtract(_airbyte_data, 'state', 'String') AS state,
    JSONExtract(_airbyte_data, 'country', 'String') AS country,
    JSONExtract(_airbyte_data, 'website', 'String') AS website,
    JSONExtract(_airbyte_data, 'address', 'String') AS address,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'created_at', 'String')) AS created_at,
    parseDateTimeBestEffort(JSONExtract(_airbyte_data, 'updated_at', 'String')) AS updated_at,
    _airbyte_extracted_at
FROM stage.public_raw__stream_bank_basic_info