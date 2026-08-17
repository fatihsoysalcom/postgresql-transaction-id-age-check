# postgresql-transaction-id-age-check
This example Python script connects to a PostgreSQL database and demonstrates how to check the age of transaction IDs (XIDs) at both the database and table levels. Monitoring XID age is crucial for preventing Transaction ID Wraparound, a critical issue that can halt your PostgreSQL database if the oldest unfrozen transaction ID approaches its 2-bil
