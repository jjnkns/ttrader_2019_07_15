import sqlite3
import os
class ORM:
    dir = ""
    #dir = os.path.dirname(__file__)
   
    dbfilename = ""
    dbpath = os.path.join(dir, dbfilename)
    print(dbpath)

    tablename = "" 
    fields = []

    createsql = """ """

    def __init__(self, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        pattern = "<{} ORM: pk={}>"
        return pattern.format(self.tablename, self.values['pk'])

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def save(self):
        if self.values['pk']:
            self.update_row()
        else:
            self.insert_row()
    
    def insert_row(self):
        """insert the values from this istance into the db, then
        return cursor.lastrowid"""
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            fieldlist = ", ".join(self.fields)
            qmarks = ", ".join(['?' for _ in self.fields])
            SQL = """ INSERT INTO {} ({}) VALUES ({}); """.format(
                self.tablename,fieldlist,qmarks)
            values = [self.values[field] for field in self.fields]
            curs.execute(SQL, values)
            pk = curs.lastrowid
            self.values['pk'] = pk

    def update_row(self):
        """update the row with this instance's pk value to the current
        values of this instance"""
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            # TODO better curly brackets
            # join a list of "column_name = ?" pairs
            set_equals = ", ".join(["{}=?".format(field) for field in self.fields])
            SQL = """ UPDATE {} SET {} WHERE pk=?; """.format(self.tablename,set_equals)
            values = [self.values[field] for field in self.fields] + [self.values['pk']]
            curs.execute(SQL, values)

    def delete(self):
        if self.values['pk'] is None:
            raise KeyError(self.__repr__() + " is not a row in " +
                            self.tablename)
        
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            SQL = """ DELETE FROM {} WHERE pk = ?; """.format(self.tablename)
            curs.execute(SQL, (self.pk,))

    @classmethod
    def create_table(cls):
        """run the cls.createsql SQL command"""
        with sqlite3.connect(cls.dbpath) as conn:
            curs = conn.cursor()
            curs.execute(cls.createsql)

    @classmethod
    def one_from_where_clause(cls, where_clause="", values=tuple()):
        SQL = "SELECT * FROM {} {};".format(cls.tablename, where_clause)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, values)

            row = cur.fetchone()
            if not row:
                return None
            return cls(**row)

    @classmethod
    def all_from_where_clause(cls, where_clause="", values=tuple()):
        SQL = "SELECT * FROM {} {};".format(cls.tablename, where_clause)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, values)

            rows = cur.fetchall()

            return [cls(**row) for row in rows]

    @classmethod
    def one_from_pk(cls, pk):
        return cls.one_from_where_clause("WHERE pk=?", (pk,))

    @classmethod
    def many_where(cls, whereclause="TRUE", values=tuple()):
        """ equivalent of one_where but with fetchall, returns a list of objects or an
        empty list """
        SQL = "SELECT * FROM {tablename} WHERE " + whereclause
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute(SQL.format(tablename=cls.tablename), values)
            rows = cur.fetchall()
            return [cls(**row) for row in rows]
