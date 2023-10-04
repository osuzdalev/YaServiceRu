from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = [
    "numpy==1.24.2",
    "openai==0.27.2",
    "pandas==1.5.3",
    "psycopg2-binary==2.9.3",
    "python-dotenv==1.0.0",
    "python-telegram-bot==15.0.0",
    "PyYAML==6.0",
    "sentence_transformers==2.2.2",
    "Telethon==1.27.0",
    "tiktoken==0.3.3",
    "torch==2.0.0",
    "weaviate-client==3.154",
]

setup(
    name="yaserviceru",
    version="0.1",
    description="Yaserviceru is a bot application",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Oleg Suzdalev",
    author_email="odsuzdalev@gmail.com",
    url="https://github.com/osuzdalev/yaserviceru",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "yaserviceru=yaserviceru.scripts.main:main",
        ],
    },
    python_requires=">=3.9,<4.0",
)
