# 파이썬에서 무언가를 요청하는 requests라는 라이브러리를 설치할 것임!
# https://2.python-requests.org/en/master/

# 맨 밑에 페이지 숫자를 추출하기 위해 Beautiful Soub 라이브러리를 사용할 것임.
# 쉽게 말해서 데이터를 추출하는데 도와줌
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?l=%EC%84%9C%EC%9A%B8&limit={LIMIT}&radius=25"

def get_last_page(): #html정보를 얻는데, 여기서 page별로 필요한 정보를 얻는다.
  result = requests.get(URL) # 해당 URL의  html 정보들을 모두 가져온다
  soup = BeautifulSoup(result.text, "html.parser") # indeed_result에서 BeautifulSoup로 html코드를 객체구조로 변환하는 parsing을 수행해준다.
  pagination = soup.find("div", {"class":"pagination"}) # 위 사이트에서 페이지 숫자의 요소들을 추출해본 결과 "div" 태그가 가장 큰 틀이고 클래느는 pagination이기 때문에 이 둘을 찾는다
  links = pagination.find_all('a') # 'a' 링크 태그가 들어간 것을 모두 찾는다.
  
  pages = []
  for link in links[:-1]: # links에 있는 각 link마다 span을 찾아주도록 해서 span 찾은걸 pages라는 array에 넣어준다. [:-1]을 넣어준 이유는 맨 마지막에 '다음'이라는 문자열이 나오기 때문이다. [:-1]은 [0:-1]과 같으며 -1은 마지막에서 한 단계전 배열까지 출력한다는 의미이다.
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_job(html): # 제목, 회사명, 위치, 링크 정보값을 얻는다.
  title = html.find("h2", {"class": "title"}).find("a")["title"]
  sjcl = html.find("div", {"class": "sjcl"}).find("span", {"class": "company"})
  company_a = sjcl.find("a")
  if company_a is not None: # 회사명에 a태그가 있다면 a 태그의 string을 가져옴
    sjcl = str(company_a.string)
  else:
    sjcl = str(sjcl.string) # a태그가 없다면 span의 string을 가져옴
  sjcl = sjcl.strip() # strip은 양쪽 공백을 모두 지워준다. 
  location = html.find("div", {"class" : "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {
    'title': title,
    'company': sjcl,
    'location' : location, 
    "link": f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?l=%EC%84%9C%EC%9A%B8&limit=50&radius=25&vjk={job_id}"
  }

def extract_jobs(last_page): # 페이지 수 만큼 데이터들을 추출
  jobs = []
  for page in range(last_page): # range(0,20)
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
  # print(result.status_code) # 200이 뜬다면 ok라는 의미
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
  for result in results:
    job = extract_job(result)
    jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs
