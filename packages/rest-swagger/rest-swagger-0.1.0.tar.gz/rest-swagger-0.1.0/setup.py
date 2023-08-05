from setuptools import setup

with open("README.md", "r") as rd:
    long_description = rd.read()

setup(
    name='rest-swagger',
    version='0.1.0',
    description='Implementation of Swagger UI for Django Rest Framework',
    url='https://github.com/AjibsBaba/rest-swagger',
    packages=['rest_swagger'],
    include_package_data=True,
    author='Samuel Ajibade',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='samuelajibade22@gmail.com',
    license='LICENSE',
    install_requires=[
        'coreapi>=2.3.3',
        'openapi-codec>=1.3.2',
        'djangorestframework>=3.12.1',
        'Django>=3.1.1',
        'simplejson>=3.17.2'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Topic :: Documentation',
        'Topic :: Software Development :: Code Generators',
        'Programming Language :: Python :: 3',
     ],
    zip_safe=False,
    python_requires='>=3.6',
    keywords=('rest_swagger rest-swagger rest swagger djangorestframework documentation'),
)
