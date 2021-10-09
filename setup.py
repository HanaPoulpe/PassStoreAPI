import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="pass_store",
    version="0.0.1",

    description="PassStore AWS API Package",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Hana Burtin",

    package_dir={
        "": "pass_store",
        "src": "pass_store"
    },
    packages=setuptools.find_packages(where="pass_store"),

    install_requires=[
        # CDK
        "aws-cdk.core~=1.124.0",

        # AWS Base
        "boto3~=1.18.53",

        # Unittests
        "coverage~=5.5",
        "flake8~=3.9.2",

        # Libs
        "python-dateutil~=2.8.2"
    ],

    python_requires=">=3.9",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
