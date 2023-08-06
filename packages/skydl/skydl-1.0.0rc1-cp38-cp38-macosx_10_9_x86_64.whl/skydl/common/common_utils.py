# -*- coding:utf-8 -*-
import csv
import copy
import math
from pathlib import Path
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP


class CommonUtils:

    @staticmethod
    def write_csv(file_name, mode='w', write_fn=None):
        """
        write record to csv file
        :param file:
        :param mode: 'r','w'
        :param csvwrite_fn:
        :return:
        """
        with open(file_name, mode) as stream:
            csvwriter = csv.writer(stream)
            write_fn(csvwriter)

    @staticmethod
    def write_h5(file_name, mode='w', db_name='', shape=(1,), dtype='f', data=None):
        import h5py
        h5_file = h5py.File(file_name, mode)
        h5_dataset = h5_file.create_dataset(db_name, shape, data)
        return h5_file

    @staticmethod
    def cycle(iterable=[None]):
        """
        e.g.
        from skydl.common.common_utils import CommonUtils
        ...
        iter = CommonUtils.cycle([0,2,3,1])
        next(iter)->0,next(iter)->2,...,next(iter)->0,next(iter)->2,...
        :param iterable: e.g. [0,2,3,1]
        :return:
        """
        from itertools import cycle
        return cycle(iterable)

    @staticmethod
    def datetime_to_int(datetime):
        import time
        return int(time.mktime(datetime.timetuple()))

    @staticmethod
    def int_to_datetime(datetime_int):
        from datetime import datetime
        return datetime.fromtimestamp(datetime_int)

    @staticmethod
    def str_to_datetime(datetime_str, format="%Y%m%d%H%M%S"):
        from datetime import datetime
        return datetime.strptime(datetime_str, format)

    @staticmethod
    def datetime_to_str(date_time, format="%Y%m%d%H%M%S"):
        from datetime import datetime
        return datetime.strftime(date_time, format)  # 将日期转成字面整型字符串, e.g. date: 2009-12-08 16:34:00 -> '20091208163400'

    @staticmethod
    def datetime_now():
        from datetime import datetime
        return datetime.now()

    @staticmethod
    def camelcase_to_snakecase(class_name):
        """
        Convert camel-case string to snake-case.
        e.g. SuperDatasetBuilder.camelcase_to_snakecase(RecommendDatasetBuilder().__class__.__name__)
        -> "recommend_dataset_builder"
        or SuperDatasetBuilder.camelcase_to_snakecase("RecommendDatasetBuilder")
        -> "recommend_dataset_builder"
        """
        # @see tensorflow_datasets.core.naming#camelcase_to_snakecase
        import re
        _first_cap_re = re.compile("(.)([A-Z][a-z0-9]+)")
        _all_cap_re = re.compile("([a-z0-9])([A-Z])")
        s1 = _first_cap_re.sub(r"\1_\2", class_name)
        return _all_cap_re.sub(r"\1_\2", s1).lower()

    @staticmethod
    def deepcopy(x, memo=None, _nil=[]):
        """深拷贝，该方法执行比较耗时间"""
        return copy.deepcopy(x, memo, _nil)

    @staticmethod
    def format_number(x, times=1, format_args="0.2f", use_round_down=True):
        """
        格式化数字输出, e.g. 12.3456->"12.34"
        :param x: 数字 e.g. 12.3456
        :param times: 乘以的倍数，方便%输出
        :param format_args: e.g. "0.2f" 保留小数点后2位输出 e.g. 123.465->"123.47"
        :param use_round_down True直接截取, False四舍五入 e.g. False: 99.999989->'100.00', 99.11789->'99.12'
        :return: "12.34" 如果要to float类型就用: float(format_number(12.3456, 100)), 注意float("100.0000")->100.0
        """
        if x is None or math.isnan(x):
            return "0.00"
        try:
            # 最原始的四舍五入的方法：return format(float(x)*times, format_args)
            # 用Decimal精确截取小数点后2位小数，也可以四舍五入。e.g. 123.465->"123.46"
            rounding = ROUND_DOWN if use_round_down else ROUND_HALF_UP
            return str(Decimal(float(x) * times).quantize(Decimal(format(0, format_args)), rounding=rounding))
        except:
            return str(x)

    @staticmethod
    def get_user_home_path():
        return str(Path.home())


