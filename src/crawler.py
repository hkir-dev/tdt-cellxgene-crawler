import os
import shutil
import logging
import subprocess
import yaml
import urllib.request

from cas.file_utils import read_yaml_config
from cas.cxg_utils import download_dataset_with_id
from cas.anndata_to_cas import anndata2cas


PROJECT_CONFIG = "project_config.yaml"
SEED_FILE = "https://raw.githubusercontent.com/brain-bican/taxonomy-development-tools/main/seed-via-docker.sh"
SEED_FILE_NAME = "seed-via-docker.sh"
CAS_FILE_NAME = "taxonomy.json"

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../crawler_config.yaml")
TARGET_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../target/")
INNER_MAKE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../resources/Makefile")


def create_taxonomies():
    config = read_yaml_config(CONFIG_PATH)
    for dataset in config["datasets"]:
        if " " in str(dataset["repo"]):
            raise ValueError("Repo name should not contain whitespace character: '" + dataset["repo"] + "'")
        project_folder = os.path.abspath(os.path.join(TARGET_PATH, dataset["repo"]))
        os.makedirs(project_folder, exist_ok=True)
        create_project_config(dataset, project_folder)
        download_seed_script(project_folder)
        create_cas_file(dataset, project_folder)
        shutil.copy(INNER_MAKE_PATH, project_folder)

        # repo_folder = os.path.abspath(os.path.join(project_folder, "target/" + dataset["repo"]))
        # runcmd("cd {dir} && ./seed-via-docker.sh -C {conf}".format(dir=project_folder, conf=PROJECT_CONFIG))
        # runcmd("cd {dir} && cp {cas} ./target/{project_name}/input_data".format(dir=project_folder, cas=CAS_FILE_NAME, project_name=dataset["repo"]))
        # runcmd("cd {repo_folder} && bash ./run.sh make load_data".format(repo_folder=repo_folder))


def create_cas_file(dataset, project_folder):
    dataset_id = str(dataset["matrix_file_id"]).replace("CellXGene_dataset:", "")
    anndata_file_path = f"{dataset_id}.h5ad"
    if not os.path.exists(anndata_file_path):
        print("Downloading dataset: " + dataset_id)
        download_dataset_with_id(dataset_id)
    cas_file_path = os.path.join(project_folder, CAS_FILE_NAME)
    print("Creating CAS file: " + cas_file_path)
    anndata2cas(anndata_file_path, dataset["labelsets"], cas_file_path, True)
    print("CAS file created: " + cas_file_path)
    return cas_file_path


def download_seed_script(project_folder):
    seed_path = os.path.abspath(os.path.join(project_folder, SEED_FILE_NAME))
    urllib.request.urlretrieve(SEED_FILE, seed_path)
    runcmd("chmod u+x {seed}".format(seed=seed_path))
    print("Seed file downloaded: " + seed_path)


def create_project_config(conf, project_folder):
    dataset = conf.copy()
    del dataset['labelsets']
    config_path = os.path.join(project_folder, PROJECT_CONFIG)
    with open(config_path, 'w+') as ff:
        yaml.dump(dataset, ff)
        print("Project config created: " + config_path)
        return config_path


def clean_folder(folder_path):
    if not os.path.exists(TARGET_PATH):
        os.makedirs(TARGET_PATH)

    for member in os.listdir(folder_path):
        if os.path.isdir(os.path.join(TARGET_PATH, member)):
            shutil.rmtree(os.path.join(TARGET_PATH, member))


def runcmd(cmd):
    logging.info("RUNNING: {}".format(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True, env=os.environ)
    (out, err) = p.communicate()
    logging.info('OUT: {}'.format(out))
    if err:
        logging.error(err)
    if p.returncode != 0:
        raise Exception('Failed: {}'.format(cmd))
    return out


if __name__ == "__main__":
    clean_folder(TARGET_PATH)
    create_taxonomies()
    print("Completed.")
