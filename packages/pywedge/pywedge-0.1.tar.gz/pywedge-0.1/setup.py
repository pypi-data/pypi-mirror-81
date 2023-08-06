

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywedge",
    version="0.1",
    author="Venkatesh rengarajan Muthu",
    author_email="taknev83@gmail.com",
    description="Cleans raw data, runs baseline models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/taknev83/pywedge/blob/main/pywedge.py",
    packages=['pywedge'],
    include_package_data=True,
    install_requires=[
        "jupyter",
        "xgboost",
        "catboost",
        "pandas",
        "scikit-learn",
        "imbalanced-learn",
    	"featuretools",        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
