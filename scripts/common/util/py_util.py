import time
import math
import random
_ONEDAY_SECONDS = 24*60*60
#����һ�����ڵ�������Ĭ�����賿4:00Ϊ��
def get_number_date(from_time,from_clock):
	now_time=from_time or time.time()
	_from_clock=from_clock or 4
	now_time_table=time.struct_time(now_time)
	if now_time_table==None:
		return 0
	if now_time_table[0]<from_clock :
		now_time_table_2=time.struct_time(now_time-_ONEDAY_SECONDS)
		return now_time_table_2[0]*1000+now_time_table_2[1]*100+now_time_table_2[2]
	else:
		return now_time_table[0]*1000+now_time_table[1]*100+now_time_table[2]

#���ĳ��ĳ��ʱ�̵��Ӧ������
def get_number_secs(from_time,from_clock):
	now_time=from_time or time.time()
	_from_clock=from_clock or 4
	now_time_table=time.struct_time(now_time)
	if now_time==None:
		return 0
	if now_time_table[0]<from_clock:
		now_time_table_2=time.struct_time(now_time-_ONEDAY_SECONDS)
		now_time_table_2[3]=from_clock
		now_time_table_2[4]=0
		now_time_table_2[5]=0
		return now_time_table_2
	else:
		now_time_table[3]=from_clock
		now_time_table[4]=0
		now_time_table[5]=0
		return now_time_table

#��M������(�ȸ���)�����N�����ظ�����
def choose_n_norepeated(t,n):
	m=t
	if m<=n:
		return t
	t2={}
	i=0
	while True:
		r=random.randint(1,m)
		if t2[r]==None:
			t2[r]=1
			i=i+1
			if i>=n:
				return t2

#��{k = prob}������ѡһ��������ʵ�k
def choose_prob(t,min_prob,max_prob):
	if min_prob and max_prob:
		ram=random.uniform(min_prob,max_prob)
	else:
		ram=random.random()
	prob=0
	for k,prob1 in t:
		prob=prob+prob1
		if ram<=prob:
			return k

#�Ӹ�ʽ"����id1,����1,����1,����id2,����2,����2,..."�������һ������id������
def choose_random_item(drop):
	if drop:
		ram=random.random()
		n=len(drop)
		prop=0
		for i in range(3,n,3):
			p=drop[i]
			if p:
				prop=prop+p
				if ram<prop:
					return [drop[i-2],drop[i-1]]

#x=0.3 0.3���ʷ���

