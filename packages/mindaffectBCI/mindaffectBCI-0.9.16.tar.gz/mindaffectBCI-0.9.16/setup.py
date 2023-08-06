from setuptools import setup, find_packages
import glob

with open("README.rst", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='mindaffectBCI',
      version='0.9.16',
      description='The MindAffect BCI python SDK',
      long_description_content_type='text/x-rst',      
      long_description=long_description,
      url='http://github.com/mindaffect/pymindaffectBCI',
      author='Jason Farquhar',
      author_email='jason@mindaffect.nl',
      license='MIT',
      packages=['mindaffectBCI','mindaffectBCI/decoder','mindaffectBCI/decoder/offline','mindaffectBCI/examples/presentation','mindaffectBCI/examples/output','mindaffectBCI/examples/utilities','mindaffectBCI/examples/acquisation'],#,find_packages(),#
      package_data={'mindaffectBCI':glob.glob('mindaffectBCI/*.txt')},
      include_package_data=True,
      #data_files=[('mindaffectBCI',glob.glob('mindaffectBCI/*.txt'))],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.5',
      install_requires=['numpy>=1.0.2', 'pyglet>=1.2', 'scipy>=1.0', 'brainflow>=3.0',
'matplotlib>=3.0'],
      zip_safe=False)
