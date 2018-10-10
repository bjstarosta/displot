if __name__ == '__main__':
    from setuptools import setup

    with open("README.md", 'r') as f:
        long_description = f.read()

    setup(
       name='displot',
       version='0.1',
       description='Structural dislocation detector.',
       long_description=long_description,
       license="GPLv3",
       author='Bohdan Starosta',
       author_email='bjstarosta@gmail.com',
       packages=['displot'],
       install_requires=[
        'numpy',
        'scipy',
        'scikit-image'
        ],
    )
