# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canvasutils']

package_data = \
{'': ['*']}

install_requires = \
['canvasapi>=2.0.0,<3.0.0', 'ipywidgets>=7.5.1,<8.0.0']

setup_kwargs = {
    'name': 'canvasutils',
    'version': '0.4.1',
    'description': 'Utilities for interacting with Canvas using Python and the canvasapi.',
    'long_description': '# CanvasUtils\n[![PyPI version](https://badge.fury.io/py/canvasutils.svg)](https://badge.fury.io/py/canvasutils)\n\nUtilities for interacting with Canvas using Python and the canvasapi.\n\n## Installation\n\n```bash\npip install canvasutils\n```\n\n`canvasutils` depends on the `ipywidgets` packages. To make sure widgets render correctly in notebooks, you may need to enable the widgets extension in Jupyter following [these instructions in the ipywidgets docs](https://ipywidgets.readthedocs.io/en/latest/user_install.html#installation), in particular, follow [these instructions](https://ipywidgets.readthedocs.io/en/latest/user_install.html#installing-the-jupyterlab-extension) if using Jupyter Lab.\n\n## Features\n\n- Submit files to Canvas from within a Jupyter notebook with user-friendly widgets.\n- Convert files to formats like `.html` from with canvas.\n- Create assignments (coming)\n- Create assignment rubrics (coming)\n\n## Dependencies\n\nSee the file [pyproject.toml](pyproject.toml), under the section `[tool.poetry.dependencies]`.\n\n## Usage\n\n### Assignment Submission in Jupyter\n\nThe submit module is made to be used within a Jupyter notebook (.ipynb file). See the provided [example.ipynb](example.ipynb). There are two available submission interfaces, widget-based drop-down menus, or text-based entries.\n\n#### Widget Submission\n\n![widget_gif](docs/img/canvasutils_widget.gif)\n\n```python\napi_url = "https://canvas.instructure.com/"\ncourse_code = 123456\n\nfrom canvasutils.submit import submit\nsubmit(course_code, api_url=api_url, token=False)  # token=False allows you to enter token interactively\n```\n\n#### Text-based Submission\n\n![text_gif](docs/img/canvasutils_text.gif)\n\n```python\nsubmit(course_code, api_url=api_url, token=False, no_widgets=True)\n```\n\n### Notebook Conversion in Jupyter\n\nNote that this command will convert the most recently saved version of a notebook. *You should save your notebook before executing this command in a cell*.\n\n```python\nfrom canvasutils.submit import convert_notebook\nconvert_notebook(\'example.ipynb\', to_format="html")\n\nNotebook successfully converted!\n```\n\n## Contributors\n\nContributions are welcomed and recognized. You can see a list of contributors in the [contributors tab](https://github.com/TomasBeuzen/canvasutils/graphs/contributors).\n\n### Credits\n\nThis package was originally based on [this repository](https://github.com/eagubsi/JupyterCanvasSubmit) created by Emily Gubski and Steven Wolfram.\n',
    'author': 'Tomas Beuzen',
    'author_email': 'tomas.beuzen@stat.ubc.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TomasBeuzen/canvasutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
