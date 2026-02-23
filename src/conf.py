project = 'pytest-loco'
copyright = '2026, pytest-loco'
author = 'Mikhalev Oleg'
release = '1.3.3'

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.autodoc_pydantic',
    'sphinx.ext.napoleon',
    'sphinx_copybutton',
    'sphinx_inline_tabs',
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_typehints_format = 'short'

autodoc_pydantic_field_doc_policy = 'description'
autodoc_pydantic_field_list_validators = False
autodoc_pydantic_field_show_constraints = False
autodoc_pydantic_field_show_alias = False

autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_field_summary = False
autodoc_pydantic_model_show_validator_summary = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_model_hide_paramlist = True

autodoc_pydantic_model_show_json = False
autodoc_pydantic_settings_show_json = False

html_static_path = ['_static']
html_theme = 'furo'

html_title = 'pytest-loco'

html_show_sourcelink = False

html_css_files = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css',
    'https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap',
    'https://fonts.googleapis.com/css2?family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap',
    'custom.css',
]

html_theme_options = {
    'dark_css_variables': {
        'font-stack': '"Roboto", sans-serif',
        'font-stack--monospace': '"Roboto Mono", monospace',
        'font-stack--headings': '"Roboto", sans-serif',
    },
    'light_css_variables': {
        'font-stack': '"Roboto", sans-serif',
        'font-stack--monospace': '"Roboto Mono", monospace',
        'font-stack--headings': '"Roboto", sans-serif',
    },
    'footer_icons': [
        {
            'name': 'GitHub',
            'url': 'https://github.com/pytest-loco/pytest-loco-docs',
            'html': '',
            'class': 'fa-brands fa-solid fa-github fa-2x',
        },
    ],
}
