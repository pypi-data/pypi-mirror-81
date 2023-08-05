# Mobile Vikings scraper

### This library is a web-scraper to get data about your account on Mobile Vikings (in Poland)

Usage is super simple:

```python
import mobilevikings_scraper

# Get a dict with all the data
stuff = mobilevikings_scraper.scrape('your_login_email', 'password')

# You can play around with what you will find in this dict:
internet = stuff['services'][0]['pointer_description']
print(f'You have {internet} of internet left')

if float(internet[:-2]) > 100:
    print('Niiiiice')
elif float(internet[:-2]) < 1:
    print('WHAAAT!!!')
```


