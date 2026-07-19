from setuptools import setup, find_packages
from pathlib import Path

readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="TallySync",
    version="1.0.0",
    author="OmniMagination",
    author_email="support@tallysync.com",
    description="Professional Desktop Application for TallyPrime Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omnimagination/TallyWhatsappSync",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tallysync=app.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
