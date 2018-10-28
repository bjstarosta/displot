if __name__ == '__main__':
    from setuptools import setup
    from displot.displot import displot_info

    with open("README.md", 'r') as f:
        long_description = f.read()

    setup(
       name=displot_info['appTitle'],
       version=displot_info['appVersion'],
       description='Structural dislocation detector.',
       long_description=long_description,
       license="GPLv3",
       author=displot_info['author'],
       author_email=displot_info['authorEmail'],
       packages=['displot'],
       install_requires=[
        'numpy',
        'scipy',
        'scikit-image'
        ],
    )
