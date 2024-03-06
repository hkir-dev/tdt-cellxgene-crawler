# tdt-cellxgene-crawler
Generates taxonomy repositories for Taxonomy Development Tools based on datasets published via CellXGene.

To run the project:

1. Create a virtual environment

```commandline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Update project config to specify datasets to crawl:

```yaml
datasets:

  - id: CCN20240304
    title: "Supercluster: IT-projecting excitatory neurons"
    description: "Cellular and molecular characterization of human cortical cytoarchitecture. Supercluster: IT-projecting excitatory neurons."
    matrix_file_id: CellXGene_dataset:c3aa4f95-7a18-4a7d-8dd8-ca324d714363
    github_org: hkir-dev
    repo: human-neocortex-it-projecting-excitatory-neurons
    author: https://orcid.org/0000-0003-3373-7386
    accession_id_prefix: AITXXX
    labelsets:
      - CrossArea_cluster
      - CrossArea_subclass
```

3. Create project skeletons

```commandline
make create
```

4. Create repositories

```commandline
make publish
```
