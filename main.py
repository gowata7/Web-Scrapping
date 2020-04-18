from Scraping.indeed import get_jobs as get_indeed_jobs

# indeed 사이트 데이터 추출
indeed_jobs = get_indeed_jobs() 
print(indeed_jobs)
