"""Simple Debezium consumer example using Kafka and confluent-kafka-python.
This consumer reads change events and applies idempotent upserts to a Postgres ODS.
Note: credentials and connection strings must be configured before running.
"""

from confluent_kafka import Consumer
import json
import psycopg2

KAFKA_BOOTSTRAP = 'localhost:9092'
KAFKA_TOPIC = 'dbserver1.university.student'

PG_CONN = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'ods',
    'user': 'ods_user',
    'password': 'REPLACE_WITH_PASSWORD'
}

consumer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'group.id': 'ods-upsert-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])

def upsert_student(cur, payload):
    # payload is the Debezium change event after parsing
    after = payload.get('after')
    if not after:
        return
    # map fields accordingly
    student_id = after.get('student_id')
    sis_student_number = after.get('sis_student_number')
    first_name = after.get('first_name')
    last_name = after.get('last_name')
    dob = after.get('dob')
    primary_email = after.get('primary_email')

    cur.execute('''
    INSERT INTO canonical.student (student_id, sis_student_number, first_name, last_name, dob, primary_email, source_systems, created_at, updated_at)
    VALUES (%s,%s,%s,%s,%s,%s,%s,now(),now())
    ON CONFLICT (student_id) DO UPDATE SET
      sis_student_number = EXCLUDED.sis_student_number,
      first_name = EXCLUDED.first_name,
      last_name = EXCLUDED.last_name,
      dob = EXCLUDED.dob,
      primary_email = EXCLUDED.primary_email,
      source_systems = EXCLUDED.source_systems,
      updated_at = now();
    ''', (student_id, sis_student_number, first_name, last_name, dob, primary_email, json.dumps({'debezium_topic': KAFKA_TOPIC})))


try:
    conn = psycopg2.connect(**PG_CONN)
    conn.autocommit = False
    cur = conn.cursor()

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print('Error: %s' % msg.error())
            continue
        payload = json.loads(msg.value().decode('utf-8'))
        # depending on Debezium connector, payload structure may vary
        # here we pass the payload to simple upsert
        upsert_student(cur, payload)
        conn.commit()

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    if conn:
        conn.close()
