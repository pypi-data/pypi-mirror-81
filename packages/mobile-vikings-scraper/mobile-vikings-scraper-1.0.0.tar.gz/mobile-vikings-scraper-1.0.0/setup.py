import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setuptools.setup(
    name="mobile-vikings-scraper",
    version="1.0.0",
    description="Scraper for Mobile Vikings in Poland",
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/TheLastGimbus/mobile-vikings-scraper',
    author='TheLastGimbus',
    author_email='mateusz.soszynski@tuta.io',
    license='GPL-3.0',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Internet :: WWW/HTTP'
    ],
    install_requires=(HERE/'requirements.txt').read_text().split('\n'),
)
