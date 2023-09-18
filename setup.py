from setuptools import setup, find_packages

setup(
    name='mkdocs-action-yml',
    version='0.1',
    packages=find_packages(),
    install_requires=['Markdown'],
    entry_points={
        'markdown.extensions': [
            'action_yml = my_mkdocs_plugin.markdown_ext:makeExtension'
        ]
    },
)
