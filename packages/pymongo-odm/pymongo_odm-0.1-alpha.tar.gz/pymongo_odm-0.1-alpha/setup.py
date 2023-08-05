from distutils.core import setup

setup(
    name='pymongo_odm',
    packages=['pymongo_odm'],
    version='0.1-alpha',
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='A basic ODM wrapper for pymongo',
    author='Dor Klein',
    author_email='dorklein2@gmail.com',
    url='https://github.com/moon-investment-technologies/pymongo-odm',
    download_url='https://github.com/dorklein/pymongo-odm/archive/v0.1-alpha.tar.gz',
    keywords=['mongodb', 'mongo', 'pymongo', 'odm', 'pymongo odm'],  # Keywords that define your package best
    install_requires=[
        'pymongo',
    ],
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
