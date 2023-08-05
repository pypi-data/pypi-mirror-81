from setuptools import setup, find_packages

try:
    import torch

    has_dev_pytorch = "dev" in torch.__version__
except ImportError:
    has_dev_pytorch = False

# Base equirements
install_requires = [
    "torch>=1.5.0",
]
if has_dev_pytorch:  # Remove the PyTorch requirement
    install_requires = [
        install_require for install_require in install_requires if "torch" != re.split(r"(=|<|>)", install_require)[0]
    ]
    

setup(
    name="qtorch_posit", #naming convention, use underscore to separate words
    version="0.1.1",
    description="Low-Precision Arithmetic Simulation in Pytorch - Extension for Posit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",    
    author="Extension: Minh Ho, Himeshi, Original: Tianyi Zhang, Zhiqiu Lin, Guandao Yang, Christopher De Sa,",
    author_email="minhhn@comp.nus.edu.sg",
    project_urls={
        "Documentation": "https://qpytorch.readthedocs.io",
        "Source": "https://github.com/minhhn2910/QPyTorch",
    },
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    python_requires=">=3.6",
    install_requires=install_requires,
)
