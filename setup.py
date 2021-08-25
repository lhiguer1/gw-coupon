import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gw_coupon_downloader",
    author="Leonel Higuera",
    author_email="lhiguer1@asu.edu",
    description="Enrolls to the Goodwill newsletter using a temporary email address so that I don't have to go through the process of signing up myself.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lhiguer1/gw-coupon-downloader",
    project_urls={
        "Bug Tracker": "https://github.com/lhiguer1/gw-coupon-downloader/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'lxml',
        'python-dotenv',
        'requests',
        'secmail',
    ],
)
