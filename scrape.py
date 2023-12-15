""" 
reference: https://www.scrapingdog.com/blog/scrape-linkedin-jobs/
"""

import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

def getJobIds(numberOfJobs: int):
    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Analyst&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start={}'
    number_of_loops = math.ceil(numberOfJobs/25)

    result = []

    for i in range(number_of_loops):
        res = requests.get(target_url.format(i))
        soup = BeautifulSoup(res.text, 'html.parser')
        jobs = soup.find_all("li")

        for x in range(len(jobs)):
            job = jobs[x].find("div", {"class": "base-card"})
            
            if job != None:
                jobId = job.get('data-entity-urn').split(":")[3]
                result.append(jobId)

    return result

def getAllJobs(result):
    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    jobResult = []
    for job in range(len(result)):
        detail = {}
        resp = requests.get(target_url.format(result[job]))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            detail["job-title"] = soup.find(
                "div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
        except:
            detail["job-title"] = None

        try:
            detail["company"] = soup.find(
                "div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            detail["company"] = None

        try:
            detail["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find_all(
                "li")[0].text.replace("Seniority level", "").strip()
        except:
            detail["level"] = None

        try:
            detail["employment-type"] = soup.find("ul", {"class": "description__job-criteria-list"}).find_all(
                "li")[1].text.replace("Employment type", "").strip()
        except:
            detail["employment-type"] = None

        jobResult.append(detail)
    
    return jobResult

jobIds = getJobIds(25)
allJobs = getAllJobs(jobIds)

print(allJobs)