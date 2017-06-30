from distutils.core import setup


setup(name='ChooChoo', version='1.0.0', author='Nils Diefenbach',
      author_email='23okrs20+pypi@mykolab.com',
      url="https://github.com/nlsdfnbch/choochoo.git",
      packages=['choochoo'],
      install_requires=['requests'],
      description="Python3-based API Wrapper for Deutsche Bahn's OpenData APIs",
      license='MIT',  classifiers=['Development Status :: 4 - Beta',
                                   'Intended Audience :: Developers'],
      )

