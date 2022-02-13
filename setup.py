import setuptools

setuptools.setup(
    name='MTPPy',
    version='0.0.6',
    url='',
    license='',
    author='Valentin Khaydarov, Tobias Kock',
    author_email='valentin.khaydarov@gmail.com',
    description='Open-source modular automation',
    install_requires=[
        'opcua~=0.98.13'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
