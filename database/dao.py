from database.DB_connect import DBConnect

class DAO:

    @staticmethod
    def get_cromosomi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True) #id funzione essenziale cromosoma
        query = """ SELECT distinct cromosoma FROM  gene WHERE cromosoma <> 0 """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_geni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)   # gene-cromosoma
        query = """ SELECT id as gene, cromosoma  from gene where cromosoma <> 0 group by id
"""

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_interazione():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True) # gene1 gene2 corr
        query = """SELECT t.id_gene1 as gene1, t.id_gene2 as gene2, sum(t.correlazione) as corr 
from (select  id_gene1, id_gene2, correlazione
from interazione i2
group by i2.id_gene1, i2.id_gene2, i2.correlazione) as t 
group by t.id_gene1 , t.id_gene2 
"""
        cursor.execute(query)

        for row in cursor:
            result[ (row['gene1'], row['gene2'] )] = row['corr']

        cursor.close()
        conn.close()
        return result
