from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getAllCountries():
        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        query="""select DISTINCT(country)
                from go_retailers """

        res=[]
        cursor.execute(query)

        for row in cursor:
            res.append(row['country'])

        return res

    @staticmethod
    def getAllRetailers(country):
        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        query="""select *
                    from go_retailers gr 
                    where country=%s """

        res=[]
        cursor.execute(query, (country,))

        for row in cursor:
            res.append(Retailer(**row))

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getAllArchi (r1, r2, anno):
        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        query="""select COUNT(DISTINCT gds.Product_number) as n
            from go_daily_sales gds,go_daily_sales gds1
            where gds.Product_number=gds1.Product_number and year(gds.Date)= %s and year(gds1.Date)=%s and gds.Retailer_code=%s and gds1.Retailer_code=%s
            group by gds.Retailer_code,gds1.Retailer_code"""

        res=None
        cursor.execute(query, (anno, anno, r1, r2))

        for row in cursor:
            if row['n']!=0:
                res=row['n']

        cursor.close()
        conn.close()

        return res

if __name__=="__main__":
    print(DAO.getAllRetailers("Spain"))


