## Welcome to the LinkedIn Scraper!

### This package allows one to scrape LinkedIn for both profile data and company data

### You need to have Chrome Version 85 installed


### To install the scraper: 

```
$ pip install linkedScraper
```

### You always need to run the logon function first, this gets passed the sign-on page:

```
from linkedScraper import scraper

scraper.logon(LinkedIn_email, LinkedIn_passwod)

```
### To scrape a profile:

```

profile_info = profilescaper(Profile_URL)

# returns an array of [name, about, job]
```


### To scrape a profile:
#### For company scraping, the url format is: 
#### https://www.linkedin.com/company/THECOMPANYNAME

```
company_info = companyscraper(urls)

# returns a dataframe of all the information on a company's abuot page

```
