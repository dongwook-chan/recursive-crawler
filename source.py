# This program uses DFS to recursively visit web pages
# Thus the following analogy will be used throughout program
# 	vertex 		: web page
#	visited verteces: visited pages


import requests
from bs4 import BeautifulSoup


# validate url and if valid, return 1, else, 0
def validate(url):
	# 접속한 사이트가 옳지 않은 사이트거나 요청이 거부되었을 때, 0 반환
	try:
		r = requests.get(url)
	except requests.exceptions.ConnectionError:
		return 0

	r = requests.get(url)

	# 정상적으로 문서를 받아왔는지 확인 후, 비정상일 경우 0 반환
	if r.ok == False:
		return 0

	# http 프로토콜의 상태가 '성공'이 아닐 경우 0 반환
	if r.status_code != 200:
		return 0
	
	# 모든 예외 검사를 통과했으면 1 반환
	return 1


# dfs index page
def dfs(visited):
	# variable usage
	# - url	: full url(host name + path name) of current page
	# - path: path name of url

	# A. get URL of this page
	url = visited[-1]

	# B. get host name(src) for homepage
	host_url = visited[0]

	# C. use library function to parse
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	results = soup.find_all('a')

	# D. frwite page
	file_name = 'Output_%04d.txt' % (len(visited) - 1)
	file = open(file_name, 'w')
	file.write(soup.text)
	file.close

	# E. recursively get child url
	for link in results:
		# a. get URL of child page
		child_url = link.get('href')

		# b. if URL consists of path name only, append host name
		if child_url.find(host_url) == -1:
			child_url = host_url + child_url

		# c. if URL has '#' or '?', rsplit and take the fist element
		child_url = child_url.rsplit('#')[0]
		child_url = child_url.rsplit('?')[0]

		# d. if visited, continue
		if visited.count(child_url) != 0:
			continue

		# e. validate URL
		if validate(child_url) == 0:
			continue

		# f. append URL
		visited.append(child_url)

		# g. recursive function call
		dfs(visited)


# main routine
# A. initialize visited list
visited = []

# B. get host name
host_url = 'http://cspro.sogang.ac.kr/~gr120170213/'

# C. validate host name
if validate(host_url) == 0:
	print('invalid host name')
	exit()

# D. mark host page as visited
visited.append(host_url)

# E. get index url
index = host_url + 'index.html'

# F. validate index url
if validate(index) == 0:
	print('invalid index url')
	exit()

# G. mark index page as visited
visited.append(index)

# H. call dfs subroutine
dfs(visited)

# I. pop the last url and write every url to file
file = open('URL.txt', 'w')

visited.remove(host_url)
last_url = visited.pop()

for url in visited:
	file.write(url + '\n')
file.write(last_url)

file.close
