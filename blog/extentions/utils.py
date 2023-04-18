from . import jalali

from django.utils import timezone

def persian_numbers_converter(mystr):
    numbers={
        "0":"0",
        "1":"1",
        "2":"2",
        "3":"3",
        "4":"4",
        "5":"5",
        "6":"6",
        "7":"7",
        "8":"8",
        "9":"9",
        "10":"10",
        }
        
    for e, p in numbers.items():
        mystr=mystr.replace(e,p)

        return mystr


def jalali_converter(time):

    time=timezone.localtime(time)

    jmonth=("فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند")
    time_to_str = "{},{}.{}".format(time.year,time.month,time.day)
    time_to_tuple= jalali.Gregorian('2014,03,31').persian_tuple()
    time_to_list=list(time_to_tuple)

    for index,month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] == month
            break
 
    output= "{}/{}/{} , ساعت {}:{}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute,)

    return  persian_numbers_converter(output)