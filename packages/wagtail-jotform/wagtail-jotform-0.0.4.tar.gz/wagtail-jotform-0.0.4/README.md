## Installation

TODO (pip install)

## Configuration

You will need an API key from jotform

Add the following variables to your settings

```
JOTFORM_API_KEY = 'somekey'
JOTFORM_API_URL = 'https://api.jotform.com'
```

If your Jotform account is in EU safe mode, your JOTFORM_API_URL should be `https://eu-api.jotform.com`

Add the following to you INSTALLED_APPS in settings, note that wagtail_jotform depends on routable_page:

```
INSTALLED_APPS = [
    ...
    'wagtail_jotform',
    "wagtail.contrib.routable_page",
]
```
