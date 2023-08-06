from distutils.core import setup

setup(
    name='gics',
    packages=['gics'],
    version='0.1-alpha.5',
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='This library provides a way to parse, manipulate and analyze GICS codes.',
    author='Dor Klein',
    author_email='dorklein2@gmail.com',
    url='https://github.com/dorklein/py-gics',
    download_url='https://github.com/dorklein/py-gics/archive/v0.1-alpha.5.tar.gz',
    keywords=['GICS', 'Global Industry Classification Standard'],  # Keywords that define your package best
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
