from distutils.core import setup
setup(
  name = 'trainingtracker',         # How you named your package folder (MyLib)
  packages = ['trainingtracker'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple remote tracker for model training progress.',   # Give a short description about your library
  author = 'Joe Fioti',                   # Type in your name
  author_email = 'jafioti@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/trainingtracker/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jafioti/trainingtracker/archive/0.0.1.tar.gz',    # I explain this later on
  keywords = ['PyTorch', 'Tensorflow', 'ML'],   # Keywords that define your package best
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of the package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)