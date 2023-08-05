# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sus = src.sus:sus']}

setup_kwargs = {
    'name': 'sus',
    'version': '1.1.0',
    'description': 'Really simple static website URL shortener',
    'long_description': 'sus: Static URL Shortener\n=========================\n\n**sus** is a static site based URL shortener.\nSimple idea: generate a static site with a bunch of\n``redirect-slug-goes-here/index.html`` files with nothing but an HTML redirect in them.\n\n.. image:: https://github.com/nkantar/sus/workflows/Automated%20Checks/badge.svg\n\n\nInstallation\n------------\n\n.. code-block:: sh\n\n    # note: you\xe2\x80\x99ll need Python 3.6 or higher\n    pip install sus\n\n\nUsage\n-----\n\n#. Install package\n#. Have an ``input`` file ready\n#. Have a ``home.html`` file ready (optional)\n#. Run ``sus`` in the same directory as ``input``\n#. Voil\xc3\xa0\xe2\x80\x94your results are in the ``output/`` directory\n\n\nInput\n-----\n\nsus expects to find a file named ``input`` in the current directory, and each row\nconsists of the redirect slug and destination URL, separated by a pipe (``|``).\n\nE.g.,\n\n.. code-block::\n\n    nk|https://nkantar.com\n    sus|https://github.com/nkantar/sus\n\nIf one were to serve ``output/`` on `<https://sus-example.nkantar.com>`_, then\n`<https://sus-example.nkantar.com/nk>`_ would redirect to `<https://nkantar.com>`_ and\n`<https://sus-example.nkantar.com/sus>`_ would redirect to\n`<https://github.com/nkantar/sus>`_.\n\nThat example site exists, and its repository can be found at\n`<https://github.com/nkantar/sus-example.nkantar.com>`_.\n\n\nHomepage\n--------\n\nIf sus finds a ``home.html`` file next to ``input``, it will copy it to\n``output/index.html``, thereby generating a homepage.\nIf it doesn\xe2\x80\x99t, it will simply carry on.\n\n\nPronunciation\n-------------\n\nMuch controversy has sparked around the pronunciation of the project\xe2\x80\x99s name (no, it\nhasn\xe2\x80\x99t).\nAs such, here is the definitive guide on doing so, as conceived by the original author.\nPlease note that\xe2\x80\x94much like with\n`GIF <https://bits.blogs.nytimes.com/2013/05/23/battle-over-gif-pronunciation-erupts/>`_\n\xe2\x80\x94others may have different ideas, and who\xe2\x80\x99s to say the author knows what he\xe2\x80\x99s talking\nabout anyway?\n\n\xe2\x80\x9csus\xe2\x80\x9d is in this case pronounced as in \xe2\x80\x9csuspicious\xe2\x80\x9d, and\n`Wiktionary <https://en.wiktionary.org/wiki/sus#English>`_ helpfully provides the\nfollowing guide:\n\n- `IPA <https://en.wiktionary.org/wiki/Wiktionary:International_Phonetic_Alphabet>`_ (`key <https://en.wiktionary.org/wiki/Appendix:English_pronunciation>`_): /s\xca\x8cs/\n- Rhymes: `-\xca\x8cs <https://en.wiktionary.org/wiki/Rhymes:English/%CA%8Cs>`_\n- `Homophone <https://en.wiktionary.org/wiki/Appendix:Glossary#homophone>`_: `suss <https://en.wiktionary.org/wiki/suss#English>`_\n\n\nDevelopment\n-----------\n\nThe project by default uses `Poetry <https://python-poetry.org/>`_, and ``make install``\nshould get you up and running with all the dev dependencies.\nAfter that see other ``make`` commands for convenience.\nThey correspond to CI checks required for changes to be merged in.\n\nThe ``main`` branch is the bleeding edge version.\n`Git tags <https://github.com/nkantar/sus/tags>`_ correspond to releases.\n\n\nContributing Guidelines\n-----------------------\n\nContributions of all sorts are welcome, be they bug reports, patches, or even just\nfeedback.\nCreating a `new issue <https://github.com/nkantar/sus/issues/new>`_ or\n`pull request <https://github.com/nkantar/sus/compare>`_ is probably the best way to get\nstarted.\n\nPlease note that this project is released with a\n`Contributor Code of Conduct <https://github.com/nkantar/sus/blob/master/CODE_OF_CONDUCT.md>`_.\nBy participating in this project you agree to abide by its terms.\n\n\nLicense\n-------\n\nThis project is licensed under the MIT license. See ``LICENSE`` file for details.\n',
    'author': 'Nik Kantar',
    'author_email': 'nik@nkantar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nkantar/sus',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
