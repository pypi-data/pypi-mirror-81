import pandas as pd
from zla_utilities import \
    db_connector as dbcon, fcst_utils as fut
import warnings
warnings.filterwarnings("ignore")

def get_data(msql):
    db = 'partsdatabase'
    df = dbcon.opendata(msql, db)
    return df


def to_number(df, _by):
    _data = df[['deldate', 'qty']].groupby('deldate').sum()
    _data.index = pd.to_datetime(_data.index, format='%Y-%m-%d')
    _data = fut.full_range(_data, by=_by)
    return _data


def domestic_number(df, _by, _fill='all'):
    filter_1 = (df['sorg'] == 'DY10')
    if _fill == 'all':
        filter_2 = (df['distch'].notnull())
    elif _fill == 'nondist':
        filter_2 = (df['distch'] != '20')
    elif _fill == 'dist':
        filter_2 = (df['distch'] == '20')
    else:
        raise Exception("Sorry, your filter was wrong (allow only : 'all','nondist','dist')")

    _data = df[filter_1 & filter_2][['deldate', 'qty']].groupby('deldate').sum()
    _data.index = pd.to_datetime(_data.index, format='%Y-%m-%d')
    _data = fut.full_range(_data, by=_by)
    return _data


def export_number(df, _by, _fill='all'):
    filter_1 = (df['sorg'] == 'DY20')
    if _fill == 'all':
        filter_2 = (df['distch'].notnull())
    elif _fill == 'nonkbt':
        filter_2 = (df['distch'] != '30')
    elif _fill == 'kbt':
        filter_2 = (df['distch'] == '30')
    else:
        raise Exception("Sorry, your filter was wrong (allow only : 'all','nonkbt','kbt')")

    _data = df[filter_1 & filter_2][['deldate', 'qty']].groupby('deldate').sum()
    _data.index = pd.to_datetime(_data.index, format='%Y-%m-%d')
    _data = fut.full_range(_data, by=_by)
    return _data