from django.shortcuts import render
from submitdays.models import Profile
#from .models import Shift
from django.db.models import Q

import itertools
import collections
import statistics
import random
import calender
import datetime

# マイページ
def mypage(request):
	loginuser = request.user
	user_obj = request.user.profile
	groupID = user_obj.group
	date = datetime.datetime.now()
	# 今月中にシフト提出があった、同じグループメンバーのデータ
	group_users = Profile.objects.filter(Q(days__isnull = False) & Q(group = groupID) 
			& Q(update_at__year = date.year) & Q(update_at__month= date.month))

	context = { 
		"loginuser": loginuser,
		"groupID": groupID,
		"group_users": group_users,
	}
	return render(request, 'makeshift/mypage.html', context)


# マイページからのpostでシフトを組む。
# postでは休業日が渡される。
def shift(request):
	loginuser = request.user
	user_obj = request.user.profile
	groupID = user_obj.group
	date = datetime.datetime.now()

	next_month = 1 if (date.month == 12) else date.month + 1
	next_month_year = date.year + 1 if (date.month == 12) else date.year
	next_month_days = calendar.monthrange(next_month_year, next_month)

	group_users = Profile.objects.filter(Q(days__isnull = False) & Q(group = groupID) 
			& Q(update_at__year = date.year) & Q(update_at__month= date.month))

	r = request.POST.get('rest_days') #休業日 "[1,8,15,..]" 
	# "[1,8,15,..]" -> [1,8,15,..]
	if (not r):
		rest_days = []
	else:
		rest_days = r.lstrip('[').rstrip(']').split(',')

	#role_dict はkeyがメンバーの名前、
	#valueが仕事内容(1、2、3)のハッシュ(それぞれキッチン、ホール、両方)
	role_dic = {}
	#morethan_listはシフト多めを希望しているメンバーのリスト
	morethan_list = []
	#lls は誰が何日に入れるかをリストで表したもの。
	# 1日は a,b,c 2日は b,d,e が入れる -> [[], [a,b,c], [b,d,e], ...]
	lls = [[]] * (next_month_days + 1)
	#role_dictとllsをデータから組み立てる
	for member in group_users:
		#応急処置 日付選択せずにシフト送信した人がいた場合
		if member.days == '[]':
			continue

		name = member.name
		role_dic[name] = int(member.role)
		if member.morethan:
			morethan_list.append(name)
		itr = member.days.lstrip('[').rstrip(']').split(',')

		for day in itr:
			ls = lls[int(day)].copy()
			ls.append(name)
			lls[int(day)] = ls
	#llsから休業日を除く
	for d in rest_days:
		lls[int(d)] = []

	#makeshiftでシフトを組んで javascriptで表示しやすいよう整形
	shift = makeshift(lls, role_dic, morethan_list, next_month_year, next_month)
	shift = [i if type(i) == 'str' else " ".join(i) for i in shift]
	shift = str(shift).lstrip('[').rstrip(']')

	lls = [i if type(i) == 'str' else " ".join(i) for i in lls]
	lls = str(lls).lstrip('[').rstrip(']')
	
	context = {
		"shift": shift,
		"group_users": group_users,
		"candidate": lls,
		"rest_days": r
	}
	return render(request, 'makeshift/shift.html', context)


def is_weekend (year, month, day):
	weekday = datetime.datetime(year = year, month=month, day=day).weekday()

	return weekday == 4 or weekday == 5



#シフトを組むmain
def makeshift(lls, role_dic, morethan_list, year, month):
	lls = list(map(lambda i, ls: 
		makepairs(ls, role_dic, is_weekend(year, month, i)),
		 enumerate(lls)))

	num_of_member = len(role_dic)
	minimum = float('inf')
	shift = []

	#仮のシフトをランダムに組んで、最も評価の高いシフトに決定する。
	for i in range(40000):
		shift0 = [[] if k==[] else random.choice(k) for k in lls]

		variance, n = eval(shift0, morethan_list)
		if n == num_of_member and minimum > variance:
			minimum = variance
			shift = shift0

	return shift


# ある1日に[a,b,c]が入れるとした時、[a,b,c]を可能なペアにする。
# [a,b,c] -> [[a,b],[a,c],[b,c]]
# ただし、,キッチン+ホールまたは両方+(両方orキッチンorホール)に限定する。
# キッチン+キッチン　または ホール+ホールしかなければ。それを返す。
def makepairs(ls, role_dic, is_weekend):
	if (len(ls) < 2):
		return ls

	combs = list(map (lambda tup: list(tup), list(itertools.combinations(ls, 2))))
	ret = list(filter(lambda ls: role_dic[ls[0]] == 3 
		or role_dic[ls[1]] == 3 or (role_dic[ls[0]]+role_dic[ls[1]]) == 3, combs))

	if is_weekend and ret:
		return ret 

	else:
		return combs


# シフトの評価関数 (分散の計算) 
# 分散が小さいシフト->全員均等に入れている。
def eval(shift, morethan_list):
	ls = list(itertools.chain.from_iterable(shift))
	c = collections.Counter(ls)

	#シフト多め希望者には2日分引いた値で評価する
	for member in morethan_list:
		c[member] -= 2

	return statistics.pvariance(c.values()), len(c)


"""
def keepshift(request):
	loginuser = request.user
	user_obj = request.user.profile
	groupID = user_obj.group
	date = datetime.datetime.now()
	keepshift = request.POST.get('keepshift')
	candidate = request.POST.get('candidate')
	print(keepshift)
	print(candidate)
"""







