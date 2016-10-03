import time
_ONEDAY_SECONDS = 24*60*60
#生成一个日期的整数，默认以凌晨4:00为界
def get_number_date(frome_time,from_clock):
	now_time=time.time()
	_from_clock=from_clock or 4
	now_time_table=time.struct_time(now_time)
	if now_time_table==None:
		return 0
	if now_time_table[0]<from_clock :
		now_time_table_2=time.struct_time(now_time-_ONEDAY_SECONDS)
		return now_time_table_2[0]*1000+now_time_table_2[1]*100+now_time_table_2[2]
	else:
		return now_time_table[0]*1000+now_time_table[1]*100+now_time_table[2]

#获得某日某个时刻点对应的秒数

