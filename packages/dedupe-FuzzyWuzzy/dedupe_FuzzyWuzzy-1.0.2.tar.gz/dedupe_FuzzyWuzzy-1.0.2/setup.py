from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(name='dedupe_FuzzyWuzzy',
      version='1.0.2',
      description='Deduplication using RapidFuzz library.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://github.com/Gandharv30/dedupe-FuzzyWuzzy',
      author='Gandharv Pathak',
      author_email='pathakgandharv@gmail.com',
      license='MIT',
      packages=['dedupe_FuzzyWuzzy'],
      include_package_data=True,
      install_requires=[
          'rapidfuzz',
          'pandas',
      ],
      zip_safe=False,
      
)