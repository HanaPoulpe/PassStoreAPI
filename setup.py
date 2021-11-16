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
    author_email="hana@hanaburtin.net",

    package_dir={
        "": "src",
        "test": "test"
    },
    packages=setuptools.find_packages(where="src"),

    install_requires=[
        # CDK
        "aws-cdk.core~=1.124.0",

        # AWS Base
        "boto3~=1.18",
        "botocore~=1.21",

        # Libs
        "dateutil",
        "mypy",

        # External Layers
        "aws-lambda-powertools~=1.21",
        "pydantic~=1.8.2",
    ],

    tests_require=[
        # Unittests
        "coverage",
        "flake8",
        "isort",
        "tox",
    ],

    python_requires=">=3.9",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",

        "Typing :: Typed",
    ],
)
