import time
import math
import random
_ONEDAY_SECONDS = 24*60*60
#生成一个日期的整数，默认以凌晨4:00为界
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

#获得某日某个时刻点对应的秒数
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

#从M个数里(等概率)随机出N个不重复的数
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

#从{k = prob}表里挑选一个满足概率的k
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

#从格式"道具id1,数量1,概率1,道具id2,数量2,概率2,..."中随机出一个道具id和数量
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

#x=0.3 0.3概率发生
def prob(x):
	if x<=0:
		return False
	return random.random()<x
#x={0.2,0.3,0.5}，总和1,返回按各自概率返回索引20%返回1，30%返回2,50%返回3
def choice(x):
	d=random.random()
	sum=0
	for k,v in enumerate(x):
		if d<v+sum:
			return k
		sum=sum+v
	return sum
#从一个列表中随机一个值
def choose_1(t):
	n=len(t)
	if n==0:
		return None
	return t[random.randint(1,n)]
#从一个列表中随机一个值,从其关联列表也返回一个值
def choose_2(t,t2):
	n=len(t)
	if n==0:
		return None
	idx=random.random(1,n)
	return[t[idx],t2[idx]]
#--从不等概率的一组值里面随机选择个
#--table格式如：{[值]=概率}；函数返回 值，概率
def getrandomseed(a):
	if type(a)==dict:
		max=0
		for k,v in a:
			max=max+v
		seed=random.randint(1,max)
		sumvv=0
		for k,v in a:
			sumvv=sumvv+sumvv
			if seed<=sumvv:
				return {k:v}

def _format_key_value(key,value):
	nKeyLen=len(key)
	
	prefix=key[-2:]
	key2=key[:-3]
	if prefix=='_i' :
		return [key2,int(value)]
	elif prefix=='_f':
		return [key2,int(value)]
	elif prefix=='_s':
		return [key2,int(value)]
	elif prefix=='_l':
		return[key2,value.split(',')]
	elif prefix=='_k':
		tmp=value.split(',')
		tmp2=[]
		for _,k in enumerate(tmp):
			tmp2[k]=1
		return[key2,tmp2]
	elif prefix=='_t':
		tmp=value.split(":")
		sec=0
		for i,v in enumerate(tmp):
			t=int(v)
			if t:
				sec=t+sec*60
		return [key2,sec]
	elif prefix=='_y':








