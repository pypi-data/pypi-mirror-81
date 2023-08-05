from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="circuitdb",
    version="0.2.0",
    packages=["circuitdb",],
    install_requires=["logical",],
    license="MIT",
    url="https://github.com/reity/circuitdb",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Data set of optimal circuits for Boolean functions "+\
                "that have low arity.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
