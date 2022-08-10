import re
from setuptools import setup, find_packages

version = ''
with open('AzureTTS/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')


readme = ''
with open('README.md') as f:
    readme = f.read()


setup(
    name='AzureTTS',
    version=version,
    description='Microsoft Azure TTS Extension for ZerodayTTS',
    long_description=readme,
    long_description_content_type="text/markdown",
    license='MIT',
    include_package_data=True,
    author='zeroday0619',
    author_email='zeroday0619_dev@outlook.com',
    url='https://github.com/zeroday0619/AzureTTS',
    packages=find_packages(exclude=['.vscode', '.idea', '.github']),
    keywords=[
        "ZerodayTTS", "Microsoft Azure", "TTS"
    ],
    python_requires='>=3',
    install_requires=["aiohttp"],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
