from setuptools import setup

setup(
    name='smartliu',
    version='20181102-20220210',
    py_modules=['smartliu'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        smartliu=smartliu:smart
    ''',
)
