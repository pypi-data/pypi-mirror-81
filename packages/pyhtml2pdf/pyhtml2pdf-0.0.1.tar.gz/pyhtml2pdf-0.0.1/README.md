# pyhtml2pdf
Simple python wrapper to convert HTML to PDF with headless Chrome via selenium.

## Install
```
pip install pyhtml2pdf
```

## Example

**Use with website url**

```
from pyhtml2pdf import converter

converter.convert('https://pypi.org', 'sample.pdf')
```

**Use with html file from local machine**

```
import os
from pyhtml2pdf import converter

path = os.path.abspath('index.html')
converter.convert(f'file:///{path}', 'sample.pdf')
```

Inspired the work from https://github.com/maxvst/python-selenium-chrome-html-to-pdf-converter.git