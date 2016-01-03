import django_validajax

from setuptools import setup, find_packages

setup(
    name='django-validajax',
    version=django_validajax.__version__,
    description="Real-time form validation with Django",
    long_description=open('README.md').read(),
    classifiers=[
        # TODO
    ],
    keywords=['django', 'forms', 'validation', 'AJAX', ],
    author="Eric Plumb",
    author_email="eric.plumb@gmail.com",
    url="https://github.com/professorplumb/django-validajax",
    license='MIT',
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
)
