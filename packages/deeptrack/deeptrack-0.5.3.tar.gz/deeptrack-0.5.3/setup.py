import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deeptrack",  # Replace with your own username
    version="0.5.3",
    author="Benjamin Midtvedt",
    author_email="benjamin.midtvedt@physics.gu.se",
    description="A deep learning oriented microscopy image simulation package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/softmatterlab/DeepTrack-2.0/",
    install_requires=["tensorflow>=2.0.1", "numpy", "scipy"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)