
Forked project from: https://github.com/zhyc9de/WappalyzerApi
-------------------------------------------------------------------

# Wappalyzer-api

Flask version.

A Modified Wappalyzer Extension to Intercept API Responses via Selenium ChromeDriver.

This version include a new functionality that allow analyze each url, from the same domain, following COMODO CA Certificate Search page (https://crt.sh/).

# Installation

```pip install -r requirements.txt```

Note: chromedriver should be in PATH!

# Running

To create db:
```python manage.py init_db  ```

To up server:
```python manage.py runserver ```

To update with wappalyzer results in your db. --> JSON format.

Launch Wappalyzer to all subdomains found from url:
``` py analyze.py --url example.com ```

Launch Wappalyzer to each url in text file:
``` py analyze.py --file file.txt ```

Launch Wappalyzer to all subdomains found from urls in text file:
``` py analyze.py --certfile file.txt ```

