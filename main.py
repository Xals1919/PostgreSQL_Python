import psycopg2 

def create_table_client(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client_info(
        id_client SERIAL PRIMARY KEY,
        first_name VARCHAR(60) NOT NULL,
        second_name VARCHAR(60) NOT NULL,
        mail VARCHAR(60) NOT NULL UNIQUE
        );
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_info(
        id_phone SERIAL PRIMARY KEY,
        id_client INTEGER REFERENCES client_info(id_client),
        phone VARCHAR(12) UNIQUE
        );
    """)
    conn.commit()

def drop_table(cur):
    cur.execute("""
    DROP TABLE 
    phone_info,
    client_info;
    """)
    conn.commit()

def add_new_client(cur, first_name, second_name, mail):
    cur.execute("""
        INSERT INTO client_info(first_name, second_name, mail)
        VALUES (%s, %s, %s)
        RETURNING id_client, first_name, second_name, mail;
        """, (first_name, second_name, mail,))
    conn.commit()
    return cur.fetchone()
    
def add_new_phone(cur, id_client, phone):
    cur.execute("""
        INSERT INTO phone_info(id_client, phone)
        VALUES (%s, %s)
        RETURNING id_client, phone;
        """, (id_client, phone,))
    conn.commit()
    return cur.fetchone()

def change(cur, id_client, first_name=None, second_name=None, mail=None):
    cur.execute("""
        UPDATE client_info SET first_name=%s, second_name=%s, mail=%s 
        WHERE id_client=%s
        RETURNING id_client, first_name, second_name, mail;
        """, (first_name, second_name, mail, id_client,))
    conn.commit()
    return cur.fetchone()

def delete_client(cur, id_client):
    cur.execute("""
        DELETE FROM client_info WHERE id_client=%s;
        """, (id_client,))
    conn.commit()

def delete_phone(cur, id_phone):
    cur.execute("""
        DELETE FROM phone_info WHERE id_phone=%s;
        """, (id_phone,))
    conn.commit()

def find(cur, first_name=None, second_name=None, mail=None, phone=None):
    cur.execute("""
        SELECT first_name, second_name, mail, phone FROM client_info
        JOIN phone_info ON client_info.id_client = phone_info.id_client
        WHERE first_name=%s OR second_name=%s OR mail=%s OR phone=%s;
    """, (first_name, second_name, mail, phone,))
    return cur.fetchall()

conn = psycopg2.connect(database='netologydb', user='postgres', password='postgres')
with psycopg2.connect(database='netologydb', user='postgres', password='postgres').cursor() as cur:
    drop = drop_table(cur)
    new_table = create_table_client(cur)
    print(add_new_client(cur, 'Harry', 'Potter', 'grifindor@gmail.com'))
    print(add_new_client(cur, 'Hermione', 'Granger', 'topmagic@gmail.com'))
    print(add_new_phone(cur, '1', '79876543210'))
    print(add_new_phone(cur, '2', '79876543211'))
    print(change(cur, 1, 'Draco', 'Malfoy', 'slizerin@gmail.com'))
    delete_phone = delete_phone(cur, 1)
    delete_client = delete_client(cur, 1)
    print(find(cur, 'Hermione'))
conn.close()
