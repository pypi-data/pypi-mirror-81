import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spiffy", # Replace with your own username
    version="0.0.2",
    author="Arthur Reis",
    author_email="arpereis@gmail.com",
    description="Space Interferometer Python Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurpreis/spiffy",
    #packages=setuptools.find_packages('./venv/Lib/site-packages'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.6',
    install_requires = ['adodbapi', 'apptools', 'argon2', 'async_generator',
                         'attr', 'backcall', 'bleach', 'certifi', 'cffi',
                         'chardet', 'colorama', 'dateutil', 'defusedxml',
                         'docutils', 'envisage', 'idna', 'ipykernel', 'IPython',
                          'ipython_genutils', 'isapi', 'jedi', 'jinja2', 'json5',
                          'jsonschema', 'jupyterlab', 'jupyterlab_pygments',
                          'jupyterlab_server', 'jupyter_client', 'jupyter_core',
                          'keyring', 'markupsafe', 'matplotlib', 'mayavi',
                          'mpmath', 'nbclient', 'nbconvert', 'nbformat', 'nose',
                          'notebook', 'numpy', 'packaging', 'parso', 'PIL', 'pip',
                          'pkginfo', 'pkg_resources', 'prometheus_client',
                          'prompt_toolkit', 'pycparser', 'pyface', 'pygments',
                          'PyQt5', 'pyrsistent', 'readme_renderer', 'requests',
                          'requests_toolbelt', 'rfc3986', 'send2trash',
                          'setuptools', 'sympy', 'terminado',
                         'testpath', 'tornado', 'tqdm', 'traitlets', 'traits',
                         'traitsui', 'tvtk', 'twine', 'urllib3', 'vtkmodules',
                          'wcwidth', 'webencodings', 'wheel', 'win32com',
                         'win32ctypes', 'winpty', 'zmq',
                          ]
)