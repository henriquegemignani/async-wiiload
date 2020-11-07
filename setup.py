from setuptools import setup, find_packages

with open("README.md") as readme_file:
    long_description = readme_file.read()


def version_scheme(version):
    import setuptools_scm.version
    if version.exact:
        return setuptools_scm.version.guess_next_simple_semver(
            version.tag, retain=setuptools_scm.version.SEMVER_LEN, increment=False)
    else:
        return version.format_next_version(
            setuptools_scm.version.guess_next_simple_semver, retain=setuptools_scm.version.SEMVER_MINOR
        )


setup(
    name='async-wiiload',
    use_scm_version={
        "version_scheme": version_scheme,
        "write_to": "wiiload/version.py",
    },
    author='Henrique Gemignani',
    url='https://github.com/henriquegemignani/async-wiiload',
    description="library for sending executables to Wii's Homebrew Channel",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    scripts=[
    ],
    license='License :: OSI Approved :: Apache Software License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires=">=3.6",
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
    ],
    extras_require={
        "test": [
            'pytest',
            'pytest-cov',
            'pytest-asyncio',
            'pytest-mock',
            'mock>=4.0',
        ]
    },
    entry_points={},
)
