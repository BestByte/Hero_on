#coding=utf-8
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

#����ĳ��ĳ��ʱ�̵���Ӧ������
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

#��M������(�ȸ���)������N�����ظ�����
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

#��{k = prob}������ѡһ���������ʵ�k
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

#�Ӹ�ʽ"����id1,����1,����1,����id2,����2,����2,..."��������һ������id������
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
def prob(x):
	if x<=0:
		return False
	return random.random()<x
#x={0.2,0.3,0.5}���ܺ�1,���ذ����Ը��ʷ�������20%����1��30%����2,50%����3
def choice(x):
	d=random.random()
	sum=0
	for k,v in enumerate(x):
		if d<v+sum:
			return k
		sum=sum+v
	return sum
#��һ���б�������һ��ֵ
def choose_1(t):
	n=len(t)
	if n==0:
		return None
	return t[random.randint(1,n)]
#��һ���б�������һ��ֵ,���������б�Ҳ����һ��ֵ
def choose_2(t,t2):
	n=len(t)
	if n==0:
		return None
	idx=random.random(1,n)
	return[t[idx],t2[idx]]
#--�Ӳ��ȸ��ʵ�һ��ֵ��������ѡ����
#--table��ʽ�磺{[ֵ]=����}���������� ֵ������
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
		i=value.find(' ')
		str_data=value[1:i-1]
		str_time=value[i+1:]
		dd=value.split('-')
		tt=value.split('-')
		return [key2,time.struct_time(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minute=dd[4],second=dd[5])]
	elif prefix=='_m':
		tmp=value.split(',')
		tmp2=[]
		for _,v in enumerate(tmp):
			tp=v.split(':')
			id=int(tp[0]) or  (tp[0])
			num=int(tp[1]) or tp[1]
			tmp2[id]=num
		return [key2,tmp2]
	else:
		return key,value
def format_key_value(key,value):
	return _format_key_value(key,value)

#��ʽ��һ��table,��tableֻ��һ����ϵ
def _format_table(t):
	v2=[]
	for key,value in enumerate(t):
		key2=_format_key_value(key,value)[0]
		value2=_format_key_value(key,vlaue)[1]
		v2[key2]=value2
	return v2

#�����ֶ�����׺�ĺ����޸Ĵ�xml��ȡ����������
def format_xml_table(t):
	t2=[]
	for k,v in enumerate(t):
		v2=_format_table(v)
		if int(k)!=None:
			t2[int(k)]=v2
		else:
			t2[k]=v2
	return t2

def 












