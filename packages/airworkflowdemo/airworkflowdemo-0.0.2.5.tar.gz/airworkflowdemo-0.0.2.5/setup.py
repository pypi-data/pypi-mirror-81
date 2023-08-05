import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airworkflowdemo", # Replace with your own username
    version="0.0.2.5",
    author="Zana",
    author_email="aarunkaashyap@gmail.com",
    description="A small example package to test backend functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcarun123/air_backend_test",
    packages=['airworkflowdemo','airworkflowdemo/model','airworkflowdemo/util'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
	'cognite-sdk==2.4.1',
	'cognite-sdk-experimental==0.20.1',
	'PyGithub==1.53',
	'gitdb==4.0.5',
	'gitpython==3.1.8',
	'pytest==5.4.3',
    ],
    python_requires='>=3.6',
)
