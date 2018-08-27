# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Standard Library
import os
import sys

PATH=os.path.normpath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, PATH)

source_suffix = '.rst'
master_doc = 'index'
project = 'molden_modifier'
year = '2018'
author = 'Jürgen Löhel'
copyright = '{0}, {1}'.format(year, author)
version = '0.1.0'
release = '0.1.0'

autosummary_generate = True

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode'
]

language = None
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'

pygments_style = 'trac'
templates_path = ['_templates']
extlinks = {
    'bb': ('https://bitbucket.org/jloehel/molden_modifier', None),
    'issue': ('https://bitbucket.org/jloehel/molden_modifier/issues/%s', '#'),
    'pr': ('https://bitbucket.org/jloehel/molden_modifier/pull-requests/%s', 'PR #'),
}

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'bizstyle'
html_theme_options = {
    'rightsidebar': 'false',
}
html_static_path = ['_static']
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_short_title = '%s-%s' % (project, version)
htmlhelp_basename = 'molden_modifierdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'molden_modifier.tex', 'molden\\_modifier Documentation',
     'Jürgen Löhel', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'molden_modifier', 'molden_modifier Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'molden_modifier', 'molden_modifier Documentation',
     author, 'molden_modifier', 'One line description of project.',
     'Miscellaneous'),
]


intersphinx_mapping = {'https://docs.python.org/': None}
