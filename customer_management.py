import psycopg2


class DB:
    def __init__(self):
        self.connection = psycopg2.connect(database="clients", user="postgres", password="netology")

    def create_db(self):
        with self.connection.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS client(
                        id_client SERIAL PRIMARY KEY,
                        first_name VARCHAR(255) NOT NULL,
                        surname VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL
                    );
            """)
            self.connection.commit()

            cur.execute("""
                    CREATE TABLE IF NOT EXISTS phone_number(
                       id_phone_number SERIAL PRIMARY KEY,
                       id_client INTEGER REFERENCES client(id_client),
                       phone_number CHAR(255)
                    );
            """)
            self.connection.commit()

    def add_new_client(self, first_name, surname, email, phone_numbers=None):
        with self.connection.cursor() as cur:
            cur.execute("""
                    INSERT INTO client (first_name, surname, email)
                    VALUES(%s, %s, %s)
                    RETURNING id_client;
            """, (first_name, surname, email))

            id_client = cur.fetchone()[0]
            self.connection.commit()

        if phone_numbers is not None:
            if type(phone_numbers) is list:
                for number in phone_numbers:
                    with self.connection.cursor() as cur:
                        cur.execute("""
                                INSERT INTO phone_number (id_client, phone_number)
                                VALUES(%s, %s);
                        """, (id_client, number))
                        self.connection.commit()
            else:
                with self.connection.cursor() as cur:
                    cur.execute("""
                            INSERT INTO phone_number (id_client, phone_number)
                            VALUES(%s, %s);
                    """, (id_client, phone_numbers))
                    self.connection.commit()

    def add_phone_to_client(self, id_client, phone_numbers):
        with self.connection.cursor() as cur:
            cur.execute("""
                    INSERT INTO phone_number (id_client, phone_number)
                    VALUES(%s, %s);
            """, (id_client, phone_numbers))
            self.connection.commit()

    def set_data_client(self, id_client, first_name=None, surname=None, email=None, phone_numbers=None):
        if phone_numbers is not None:
            with self.connection.cursor() as cur:
                cur.execute("""
                        UPDATE phone_number
                        SET phone_number = %s
                        WHERE id_client = %s
                """, (phone_numbers, id_client))
                self.connection.commit()

        if email is not None:
            with self.connection.cursor() as cur:
                cur.execute("""
                        UPDATE client
                        SET email = %s
                        WHERE id_client = %s
                """, (email, id_client))
                self.connection.commit()

        if surname is not None:
            with self.connection.cursor() as cur:
                cur.execute("""
                        UPDATE client
                        SET surname = %s
                        WHERE id_client = %s
                """, (surname, id_client))
                self.connection.commit()

        if first_name is not None:
            with self.connection.cursor() as cur:
                cur.execute("""
                        UPDATE client
                        SET first_name = %s
                        WHERE id_client = %s
                """, (first_name, id_client))
                self.connection.commit()

    def delete_phone_client(self, id_client, phone_number):
        with self.connection.cursor() as cur:
            cur.execute("""
                    DELETE FROM phone_number
                    WHERE id_client = %s AND phone_number = %s;
            """, (id_client, phone_number))
            self.connection.commit()

    def delete_client(self, id_client):
        with self.connection.cursor() as cur:
            cur.execute("""
                    DELETE FROM phone_number
                    WHERE id_client = %s;
            """, (id_client, ))
            self.connection.commit()

        with self.connection.cursor() as cur:
            cur.execute("""
                    DELETE FROM client
                    WHERE id_client = %s;
            """, (id_client, ))
            self.connection.commit()

    def find_client(self, first_name=None, last_name=None, email=None, phone_numbers=None):
        if phone_numbers is not None:
            with self.connection.cursor() as cur:
                cur.execute("""
                        SELECT first_name, surname, email, phone_number
                        FROM phone_number pn 
                        JOIN client c on pn.id_client = c.id_client
                        WHERE c.id_client = %s;
                """, (phone_numbers, ))
                print(cur.fetchall())
                self.connection.commit()


if __name__ == '__main__':
    ClientDB = DB()
    ClientDB.create_db()
    #ClientDB.add_new_client('Борис', 'Пупкин', 'borispupkin@ya.ru', ['89998887766', '81234445566', '80009998877'])
    #ClientDB.delete_client(11)
    #ClientDB.delete_phone_client(12, '81234445566')
    #ClientDB.add_phone_to_client(12, '81234445566')
    #ClientDB.set_data_client(12, first_name='Евгений', surname=None, email='evgeniypupkin@ya.ru', phone_numbers='80000000000')
    ClientDB.find_client(first_name=None, last_name=None, email=None, phone_numbers='80000000000')
    ClientDB.connection.close()
