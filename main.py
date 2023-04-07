import calendar
import bson
import json
from datetime import datetime, timedelta

from aiogram import types
from aiogram.utils import executor

from bot import dp

with open('sampleDB/sample_collection.bson', 'rb') as f:
    data = bson.decode_all(f.read())


@dp.message_handler()
async def start(message: types.Message):
    input_data = json.loads(message.text)
    if input_data.get("group_type") == "month":
        result = {
            "dataset": [],
            "labels": []
        }
        dt_from_year = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S").year
        dt_from_month = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S").month

        dt_upto_year = datetime.strptime(input_data.get("dt_upto"), "%Y-%m-%dT%H:%M:%S").year
        dt_upto_month = datetime.strptime(input_data.get("dt_upto"), "%Y-%m-%dT%H:%M:%S").month
        for y in range(dt_from_year, dt_upto_year + 1):
            for m in range(dt_from_month, dt_upto_month + 1):
                result_value = 0
                for i in data:
                    if i.get("dt").month == m and i.get("dt").year == y:
                        result_value += i.get("value")
                result.get("dataset").append(result_value)
                result.get("labels").append(datetime.strftime(datetime(year=y, month=m, day=1),
                                                              "%Y-%m-%dT%H:%M:%S"))
        await message.answer(str(result))
    if input_data.get("group_type") == "day":
        result = {
            "dataset": [],
            "labels": []
        }
        dt_from_year = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S").year
        dt_from_month = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S").month

        dt_upto_year = datetime.strptime(input_data.get("dt_upto"), "%Y-%m-%dT%H:%M:%S").year
        dt_upto_month = datetime.strptime(input_data.get("dt_upto"), "%Y-%m-%dT%H:%M:%S").month
        for y in range(dt_from_year, dt_upto_year + 1):
            for m in range(dt_from_month, dt_upto_month + 1):
                for d in range(1, calendar.monthrange(year=y, month=m)[1] + 1):
                    result_value = 0
                    for i in data:
                        if i.get("dt").month == m and i.get("dt").year == y and i.get("dt").day == d:
                            result_value += i.get("value")
                    result.get("dataset").append(result_value)
                    result.get("labels").append(datetime.strftime(datetime(year=y, month=m, day=d),
                                                                  "%Y-%m-%dT%H:%M:%S"))

        await message.answer(str(result))
    if input_data.get("group_type") == "hour":
        result = {
            "dataset": [],
            "labels": []
        }
        dt_from_year = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S").year
        dt_from_month = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S").month
        dt_from_day = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S").day
        dt_from_hour = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S").hour

        dt_upto_year = datetime.strptime(input_data.get("dt_upto"), "%Y-%m-%dT%H:%M:%S").year
        dt_upto_month = datetime.strptime(input_data.get("dt_upto"), "%Y-%m-%dT%H:%M:%S").month
        dt_upto_day = datetime.strptime(input_data.get("dt_upto"), "%Y-%m-%dT%H:%M:%S").day

        d1 = datetime.strptime(input_data.get("dt_from"), "%Y-%m-%dT%H:%M:%S") + timedelta()
        d2 = datetime.strptime(input_data.get("dt_upto"), "%Y-%m-%dT%H:%M:%S") + timedelta()

        hours = int((d2 - d1).total_seconds()/(60*60)) + 1
        check = 0
        for y in range(dt_from_year, dt_upto_year + 1):
            for m in range(dt_from_month, dt_upto_month + 1):
                for d in range(dt_from_day, dt_upto_day + 1):
                    if check == hours:
                        result.get("labels").append(datetime.strftime(datetime(year=y, month=m, day=d),
                                                                      "%Y-%m-%dT%H:%M:%S"))
                        break
                    for h in range(dt_from_hour, 24):
                        result_value = 0
                        for i in data:
                            if i.get("dt").month == m and \
                                    i.get("dt").year == y and \
                                    i.get("dt").day == d and i.get("dt").hour == h:
                                result_value += i.get("value")
                        result.get("dataset").append(result_value)
                        result.get("labels").append(datetime.strftime(datetime(year=y, month=m, day=d, hour=h),
                                                                      "%Y-%m-%dT%H:%M:%S"))
                        check += 1
                        if check == hours:
                            result.get("dataset")[-1] = 0
                            break
        await message.answer(str(result))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
