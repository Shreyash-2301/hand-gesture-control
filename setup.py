from setuptools import setup, find_packages

setup(
    name="gesture-control",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.8.0",
        "mediapipe>=0.10.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    author="Shreyash Danke",
    author_email="your.email@example.com",
    description="A hand gesture detection and control system using MediaPipe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Shreyash-2301/hand-gesture-control",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)