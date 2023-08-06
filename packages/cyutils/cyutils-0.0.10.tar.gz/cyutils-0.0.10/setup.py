from setuptools import setup, find_packages

setup_args = dict(
    name='cyutils',
    version='0.0.10',
    description='Utilities by cy4',
    license='MIT',
    packages=find_packages(),
    author='Cy4',
    keywords=['Cy4', 'Cy', 'CyUtils'],
    python_requires='>=3.6'
)

install_requires = [
    'numpy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)