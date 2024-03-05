# tdt-cellxgene-crawler
Generates taxonomy repositories for Taxonomy Development Tools based on datasets published via CellXGene.

To run the project:

1. Create a virtual environment

```commandline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. Create project skeletons

```commandline
make create
```

1. Create repositories

```commandline
make publish
```
