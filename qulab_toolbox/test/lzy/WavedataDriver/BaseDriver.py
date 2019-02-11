# -*- coding: utf-8 -*-
#copy from rebuild branch qulab\_driver.py 2019.02.11
import copy
import importlib
import logging
import os
import re
import string

import numpy as np
import quantities as pq

log = logging.getLogger('qulab.driver')
log.addHandler(logging.NullHandler())

__all__ = [
    'QReal', 'QInteger', 'QString', 'QOption', 'QBool', 'QVector', 'QList',
    'BaseDriver',
]


class Quantity:
    def __init__(self,
                 name,
                 value=None,
                 type=None,
                 unit=None,
                 ch=None,
                 get_cmd='',
                 set_cmd=''):
        self.name = name
        self.value = value
        self.type = type
        self.unit = unit
        self.ch = ch
        self.driver = None
        self.set_cmd = set_cmd
        self.get_cmd = get_cmd
        self.default = dict(value = value,
                            unit = unit,
                            ch = ch)

    def __str__(self):
        return '%s' % self.value

    def setDriver(self, driver):
        self.driver = driver

    def getValue(self, **kw):
        # if self.driver is not None and self.get_cmd is not '':
        #     cmd = self._formatGetCmd(**kw)
        #     self.value = self.driver.query(cmd)
        return self.value

    def setValue(self, value, **kw):
        self.value = value
        if self.driver is not None and self.set_cmd is not '':
            cmd = self._formatSetCmd(value, **kw)
            self.driver.write(cmd)

    def _formatGetCmd(self, **kw):
        _kw = copy.deepcopy(self.default)
        _kw.update(**kw)
        return self.get_cmd % dict(**_kw)

    def _formatSetCmd(self, value, **kw):
        _kw = copy.deepcopy(self.default)
        _kw.update(value=value,**kw)
        return self.set_cmd % dict(**_kw)


class QReal(Quantity):
    def __init__(self,
                 name,
                 value=None,
                 unit=None,
                 ch=None,
                 get_cmd='',
                 set_cmd=''):
        super(QReal, self).__init__(
            name, value, 'Real', unit, ch, get_cmd=get_cmd, set_cmd=set_cmd)

    def getValue(self, **kw):
        if self.driver is not None and self.get_cmd is not '':
            cmd = self._formatGetCmd(**kw)
            res = self.driver.query_ascii_values(cmd)
            self.value = res[0]
        return self.value


class QInteger(QReal):
    def __init__(self,
                 name,
                 value=None,
                 unit=None,
                 ch=None,
                 get_cmd='',
                 set_cmd=''):
        Quantity.__init__(
            self,
            name,
            value,
            'Integer',
            unit,
            ch,
            get_cmd=get_cmd,
            set_cmd=set_cmd)

    def getValue(self, **kw):
        super(QInteger, self).getValue(**kw)
        return int(self.value)


class QString(Quantity):
    def __init__(self, name, value=None, ch=None, get_cmd='', set_cmd=''):
        super(QString, self).__init__(
            name, value, 'String', ch=ch, get_cmd=get_cmd, set_cmd=set_cmd)

    def getValue(self, **kw):
        if self.driver is not None and self.get_cmd is not '':
            cmd = self._formatGetCmd(**kw)
            res = self.driver.query(cmd)
            self.value = res.strip("\n\"' ")
        return self.value


class QOption(QString):
    def __init__(self,
                 name,
                 value=None,
                 options=[],
                 ch=None,
                 get_cmd='',
                 set_cmd=''):
        Quantity.__init__(
            self,
            name,
            value,
            'Option',
            ch=ch,
            get_cmd=get_cmd,
            set_cmd=set_cmd)
        self.options = options
        self._opts = {}
        for k, v in self.options:
            self._opts[k] = v
            self._opts[v] = k

    def setValue(self, value, **kw):
        self.value = value
        if self.driver is not None and self.set_cmd is not '':
            options = dict(self.options)
            if value not in options.keys():
                #logger.error('%s not in %s options' % (value, self.name))
                return
            cmd = self._formatSetCmd(value, option=options[value], **kw)
            # cmd = self.set_cmd % dict(option=options[value], **kw)
            self.driver.write(cmd)

    def getValue(self, **kw):
        if self.driver is not None and self.get_cmd is not '':
            cmd = self._formatGetCmd(**kw)
            res = self.driver.query(cmd)
            res_value = res.strip("\n\"' ")
            self.value = self._opts[res_value]
        return self.value

    def getIndex(self, **kw):
        value = self.getValue(**kw)
        if value is None:
            return None

        for i, pair in enumerate(self.options):
            if pair[0] == value:
                return i
        return None

    def getCmdOption(self, **kw):
        value = self.getValue(**kw)
        if value is None:
            return None
        return dict(self.options)[value]


class QBool(QInteger):
    def __init__(self, name, value=None, ch=None, get_cmd='', set_cmd=''):
        Quantity.__init__(
            self, name, value, 'Bool', ch=ch, get_cmd=get_cmd, set_cmd=set_cmd)

    def getValue(self, **kw):
        return bool(super(QBool, self).getValue(**kw))


class QVector(Quantity):
    def __init__(self,
                 name,
                 value=None,
                 unit=None,
                 ch=None,
                 get_cmd='',
                 set_cmd=''):
        super(QVector, self).__init__(
            name, value, 'Vector', unit, ch, get_cmd=get_cmd, set_cmd=set_cmd)

    def getValue(self, **kw):
        if self.driver is not None and self.get_cmd is not '':
            cmd = self._formatGetCmd(**kw)
            if kw.get('binary'):
                res = self.driver.query_binary_values(cmd)
            else:
                res = self.driver.query_ascii_values(cmd)
            self.value = np.asarray(res)
        return self.value


class QList(Quantity):
    def __init__(self,
                 name,
                 value=None,
                 unit=None,
                 ch=None,
                 get_cmd='',
                 set_cmd=''):
        super(QList, self).__init__(
            name, value, 'List', unit, ch, get_cmd=get_cmd, set_cmd=set_cmd)


class BaseDriver(object):

    quants = []

    config = {}

    def __init__(self, addr=None, **kw):
        self.addr = addr
        self.handle = None
        self.model = None

        self.quantities = {}
        for quant in self.quants:
            self.quantities[quant.name] = copy.deepcopy(quant)
            self.quantities[quant.name].driver = self

    def __repr__(self):
        return 'Driver(addr=%s)' % (self.addr)

    def init(self,cfg=None):
        if cfg == None:
            cfg = self.config
        for key in cfg.keys():
            if isinstance(cfg[key],dict):
                self.setValue(key, **cfg[key])
            else:
                self.setValue(key, cfg[key])
        return self

    def performOpen(self):
        pass

    def performClose(self):
        pass

    def performSetValue(self, quant, value, **kw):
        quant.setValue(value, **kw)

    def performGetValue(self, quant, value, **kw):
        return quant.getValue(**kw)

    def getValue(self, name, **kw):
        if name in self.quantities:
            return self.performGetValue(self.quantities[name], **kw)
        else:
            return None

    def getIndex(self, name, **kw):
        if name in self.quantities:
            return self.quantities[name].getIndex(**kw)

    def getCmdOption(self, name, **kw):
        if name in self.quantities:
            return self.quantities[name].getCmdOption(**kw)

    def setValue(self, name, value, **kw):
        if name in self.quantities:
            self.performSetValue(self.quantities[name], value, **kw)
        return self

    def errors(self):
        """返回错误列表"""
        errs = []
        return errs

    def check_errors_and_log(self, message):
        errs = self.errors()
        for e in errs:
            log.error("%s << %s", str(self.handle), message)
            log.error("%s >> %s", str(self.handle), ("%d : %s" % e))

    def query(self, message, check_errors=False):
        if check_errors:
            self.check_errors_and_log(message)
        pass

    def write(self, message, check_errors=False):
        if check_errors:
            self.check_errors_and_log(message)
        pass

    def read(self, message, check_errors=False):
        if check_errors:
            self.check_errors_and_log(message)
        pass
