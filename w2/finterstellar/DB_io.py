import finterstellar as fs
import pandas as pd
import sqlite3

    
################################################
#
# Read data from DB
# for Financial Engineering Recipe lecture
#
################################################
class DB_read:


    def make_daily_price_volume_df(self, cd, start_date=fs.present_date()):

        con = sqlite3.connect('db/fsdb01.db3')

        sql = 'SELECT trade_date, price_close, trade_volume '
        sql += 'FROM price_daily '
        sql += 'WHERE issue_code = ? '
        sql += 'AND trade_date >= ?;'

        with con:
            cur = con.cursor()
            cur.execute(sql, [cd, start_date])
            rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=['trade_time', cd, 'volume'])
        df.set_index('trade_time', inplace=True)

        con.close()

        return df


    def issue_list_by_avg_volume(self, instrument_type='', \
                                 sector_1='', sector_2='', sector_3='', sector_4='', \
                                 start_date=fs.a_month_ago(), volume=0):

        instrument_type = '%'+instrument_type+'%'
        sector_1 = '%'+sector_1+'%'

        con = sqlite3.connect('db/fsdb01.db3')

        sql = 'SELECT issue_code_master.issue_code, issue_name, instrument_type, sector_1, avg(price_daily.trade_volume) '
        sql += 'FROM price_daily, issue_code_master '
        sql += 'WHERE trade_date >= ? '
        sql += 'AND instrument_type like ? '
        sql += 'AND sector_1 like ? '
        sql += 'AND price_daily.issue_code = issue_code_master.issue_code '
        sql += 'GROUP BY issue_name, instrument_type, sector_1 '
        sql += 'HAVING avg(price_daily.trade_volume) >= ? '
        sql += 'ORDER BY 4 desc; '

        with con:
            cur = con.cursor()
            cur.execute(sql, [start_date, instrument_type, sector_1, volume])
            rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=['issue_code', 'issue_name', 'instrument_type', 'sector_1', 'average_volume'])
        df.set_index('issue_code', inplace=True)

        con.close()

        return df


    def make_daily_price_df(self, s_cd):
    
        if type(s_cd) == str:
            cds = []
            cds.append(s_cd)
        else:
            cds = s_cd    
        
        con = sqlite3.connect('db/fsdb01.db3')
            
        price_df = pd.DataFrame()
        for cd in cds:
            tmp = dict()
            sql = 'SELECT trade_date, price_close '
            sql += 'FROM price_daily WHERE issue_code=?'
            with con:
                cur = con.cursor()
                cur.execute(sql, [cd])
                rows = cur.fetchall()
                for r in rows:
                    tmp[r[0]] = r[1]
            sr = pd.Series(tmp)
            sr.name = cd
            price_df = pd.concat([price_df, sr], axis=1, sort=True)
        price_df.index = pd.to_datetime(price_df.index)
        
        con.close()
            
        return(price_df)    
    
    
    def read_pair_strategy_params(self, sid):
        
        con = sqlite3.connect('db/fsdb01.db3')

        sql = 'SELECT * '
        sql += 'FROM pair_strategy_daily '
        sql += 'WHERE strategy_id=? '
        sql += 'ORDER BY create_date DESC LIMIT 1'
        with con:
            cur = con.cursor()
            cur.execute(sql, [sid])
            result = cur.fetchall()[0]
        
        con.close()
            
        return(result)    
    
    
    
    def read_issue_code_master(self, instrument_type='%', issue_name='%', sector_1='%', sector_2='%', sector_3='%', sector_4='%', \
                               trade_volume=0, limit=100):

        con = sqlite3.connect('db/fsdb01.db3')

        df = pd.DataFrame()
        sql = 'SELECT * FROM issue_code_master '
        sql += 'WHERE instrument_type like ? '
        sql += 'AND issue_name like ? '
        sql += 'AND sector_1 like ? '
        sql += 'AND sector_2 like ? '
        sql += 'AND sector_3 like ? '
        sql += 'AND sector_4 like ? '
        sql += 'AND trade_volume >= ? '
        sql += ' ORDER BY trade_volume DESC LIMIT ?;'

        with con:
            cur = con.cursor()
            cur.execute(sql, [instrument_type, issue_name, sector_1, sector_2, sector_3, sector_4, trade_volume, limit])
            rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=['issue_code', 'issue_name', 'instrument_type',\
                                         'sector_1', 'sector_2', 'sector_3', 'sector_4',\
                                         'price_present', 'trade_volume', 'trade_amount', 'market_cap'])
        df.set_index('issue_code', inplace=True)

        con.close()

        return(df)       

    
    
    ################################################
    #   코인 관련 코드 
    #   by finterstellar
    #   initiated on 2019-05-01
    #   last modified on 2019-05-26
    ################################################
    
    def read_coin_code_master(self):

        con = sqlite3.connect('db/fsdb01.db3')

        df = pd.DataFrame()
        sql = 'SELECT issue_code, issue_name FROM coin_code_master'

        with con:
            cur = con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=['issue_code', 'issue_name'])
        df.set_index('issue_code', inplace=True)

        con.close()

        return(df)       
    
    
      
    def make_daily_coin_price_df(self, s_cd):
    
        if type(s_cd) == str:
            cds = []
            cds.append(s_cd)
        else:
            cds = s_cd    
        
        con = sqlite3.connect('db/fsdb01.db3')
            
        price_df = pd.DataFrame()
        for cd in cds:
            tmp = dict()
            sql = 'SELECT trade_date, price_close FROM coin_price_daily WHERE issue_code=?'
            with con:
                cur = con.cursor()
                cur.execute(sql, [cd])
                rows = cur.fetchall()
                for r in rows:
                    tmp[r[0]] = r[1]
            sr = pd.Series(tmp)
            sr.name = cd
            price_df = pd.concat([price_df, sr], axis=1, sort=True)
        price_df.index = pd.to_datetime(price_df.index)
        
        con.close()
            
        return(price_df)    

      
    def make_intraday_coin_price_df(self, s_cd):
    
        if type(s_cd) == str:
            cds = []
            cds.append(s_cd)
        else:
            cds = s_cd    
        
        con = sqlite3.connect('db/fsdb01.db3')
            
        price_df = pd.DataFrame()
        for cd in cds:
            tmp = dict()
            sql = 'SELECT trade_time, price_close FROM coin_price_intraday WHERE issue_code=?'
            with con:
                cur = con.cursor()
                cur.execute(sql, [cd])
                rows = cur.fetchall()
                for r in rows:
                    tmp[r[0]] = r[1]
            sr = pd.Series(tmp)
            sr.name = cd
            price_df = pd.concat([price_df, sr], axis=1, sort=True)
        price_df.index = pd.to_datetime(price_df.index)
        
        con.close()
            
        return(price_df)


    def make_intraday_coin_price_volume_df(self, cd):

        con = sqlite3.connect('db/fsdb01.db3')

        sql = 'SELECT trade_time, price_close, trade_volume '
        sql += 'FROM coin_price_intraday WHERE issue_code=?'

        with con:
            cur = con.cursor()
            cur.execute(sql, [cd])
            rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=['trade_time', cd, 'volume'])
        df.set_index('trade_time', inplace=True)

        con.close()

        return df
