from distutils.core import setup

setup(
    name="templatext",
    packages=["templatext"],
    version="0.0.2",
    license="MIT",
    description="Text preprocessing template for NLP.",
    author="Jaime Tenorio",
    author_email="jaimeteb@gmail.com",
    url="https://github.com/jaimeteb/templatext",
    download_url="https://github.com/jaimeteb/templatext/archive/v0.0.2.tar.gz",
    keywords=["nlp", "preprocessing", "text"],
    install_requires=[
        "beautifulsoup4",
        "gensim",
        "spacy",
        "Unidecode",
        "word2number",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
