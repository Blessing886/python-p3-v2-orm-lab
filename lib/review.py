from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        
        if self.id is None:
            sql = """
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            """
            CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
            CONN.commit()
            self.id = CURSOR.lastrowid
            Review.all[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review
   
    @classmethod
    def instance_from_db(cls, row):
        review_id = row["id"] 
        if review_id in cls.all:
            return cls.all[review_id] 

        review = cls(row["year"], row["summary"], row["employee_id"], review_id)
        cls.all[review_id] = review
        return review

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM reviews WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None


    def update(self):
        if self.id is not None:
            sql = """
                UPDATE reviews
                SET year = ?, summary = ?, employee_id = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
            CONN.commit()

    def delete(self):
        if self.id is not None:
            sql = """
                DELETE FROM reviews WHERE id = ?
            """
            CURSOR.execute(sql, (self.id,))
            CONN.commit()
            del Review.all[self.id]
            self.id = None

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM reviews
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]


