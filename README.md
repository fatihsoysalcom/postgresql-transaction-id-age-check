# PostgreSQL Transaction ID Age Check

This example Python script connects to a PostgreSQL database and demonstrates how to check the age of transaction IDs (XIDs) at both the database and table levels. Monitoring XID age is crucial for preventing Transaction ID Wraparound, a critical issue that can halt your PostgreSQL database if the oldest unfrozen transaction ID approaches its 2-billion limit.

## Language

`python`

## How to Run

1. Install the `psycopg2` library: `pip install psycopg2-binary`
2. Set your PostgreSQL connection details as environment variables:
   `export PG_HOST='localhost' PG_DBNAME='your_db' PG_USER='your_user' PG_PASSWORD='your_password'`
3. Run the script: `python main.py`

## Original Article

This example accompanies the Turkish article: [PostgreSQL İşlem ID'si Wraparound Nedir ve Veritabanınızı Nasıl Korursunuz?](https://fatihsoysal.com/blog/postgresql-islem-idsi-wraparound-nedir-ve-veritabaninizi-nasil-korursunuz/).

## License

MIT — see [LICENSE](LICENSE).
