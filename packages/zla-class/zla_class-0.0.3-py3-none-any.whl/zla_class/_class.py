from zla_material_class.master_script.master_sql import *
from zla_material_class.ws_script.wsdata_sql import *
from zla_material_class.ws_script.ws_method import *
from zla_mrpsetting.get_4yeardemand import generate_deldate as delg
from zla_backend.general import \
    vendor_finding_bymat as vmat, \
    header_ecnbysap_bymat as ecnmat

class get_ws(object):
    def __init__(self, partno, start=None, end=None, customer=None, parent=False, n_deldate=False):
        # Make character sentense
        self.partno = partno
        self.allcustomer = customer_parentable(customer, parent)
        self.dictchain = ecnmat.get_chaindictionary(partno)
        self.master = get_partsmaster(partno)
        self.character = get_partscharacter(partno)
        self.purchasing = get_partspurchasing(partno)
        self.vendor, self.cost, self.mapping = vmat.get_vendor_mat(partno, self.purchasing.get('spt'))

        # Make sql_sentense
        sql_nontapa = "orders.itemcat <> 'TAPA'"
        sql_partno = get_sql_1(self.dictchain.keys())
        sql_customer = get_sql_2(self.allcustomer)
        sql_timerange = get_sql_3([start, end])
        list_sql = [sql_nontapa, sql_partno, sql_customer, sql_timerange]
        where_sql = merge_wherecondition(list_sql)
        msql = finishing_sql(where_sql)
        self.rawdata = get_data(msql)
        if n_deldate == True:
            self.newdata = delg.generate_deldate(self.rawdata)
        else:
            self.newdata = self.rawdata.copy()
            self.newdata['deldate'] = self.newdata['del1stdate']

        # Generate dataframe of number
        self.to_daysnumber()

    def to_daysnumber(self, _by='days'):
        self.history = to_number(self.newdata, _by)
        self.dom_all = domestic_number(self.newdata, _by, _fill='all')
        self.dom_ndist = domestic_number(self.newdata, _by, _fill='nondist')
        self.dom_dist = domestic_number(self.newdata, _by, _fill='dist')
        self.exp_all = export_number(self.newdata, _by, _fill='all')
        self.exp_nkbt = export_number(self.newdata, _by, _fill='nonkbt')
        self.exp_kbt = export_number(self.newdata, _by, _fill='kbt')

    def to_weeksnumber(self, _by='weeks'):
        self.history = to_number(self.newdata, _by)
        self.dom_all = domestic_number(self.newdata, _by, _fill='all')
        self.dom_ndist = domestic_number(self.newdata, _by, _fill='nondist')
        self.dom_dist = domestic_number(self.newdata, _by, _fill='dist')
        self.exp_all = export_number(self.newdata, _by, _fill='all')
        self.exp_nkbt = export_number(self.newdata, _by, _fill='nonkbt')
        self.exp_kbt = export_number(self.newdata, _by, _fill='kbt')

    def to_monthsnumber(self, _by='months'):
        self.history = to_number(self.newdata, _by)
        self.dom_all = domestic_number(self.newdata, _by, _fill='all')
        self.dom_ndist = domestic_number(self.newdata, _by, _fill='nondist')
        self.dom_dist = domestic_number(self.newdata, _by, _fill='dist')
        self.exp_all = export_number(self.newdata, _by, _fill='all')
        self.exp_nkbt = export_number(self.newdata, _by, _fill='nonkbt')
        self.exp_kbt = export_number(self.newdata, _by, _fill='kbt')

    def to_yearsnumber(self, _by='years'):
        self.history = to_number(self.newdata, _by)
        self.dom_all = domestic_number(self.newdata, _by, _fill='all')
        self.dom_ndist = domestic_number(self.newdata, _by, _fill='nondist')
        self.dom_dist = domestic_number(self.newdata, _by, _fill='dist')
        self.exp_all = export_number(self.newdata, _by, _fill='all')
        self.exp_nkbt = export_number(self.newdata, _by, _fill='nonkbt')
        self.exp_kbt = export_number(self.newdata, _by, _fill='kbt')