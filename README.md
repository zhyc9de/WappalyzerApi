Fork project by: https://github.com/zhyc9de/WappalyzerApi

# Wappalyzer-api

Flask version.

A Modified Wappalyzer Extension to Intercept API Responses via Selenium ChromeDriver

# Installation

```pip install -r requirements.txt```

Note: chromedriver should be in PATH!

# Running
To create db:
```python manage.py init_db  ```

To up server:
```python manage.py runserver ```

Execute script to update with wappalyzer results your db. --> JSON format.:
``` py analyze.py ``` 