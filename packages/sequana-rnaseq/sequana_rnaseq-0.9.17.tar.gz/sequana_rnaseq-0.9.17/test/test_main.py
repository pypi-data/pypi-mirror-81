import easydev
import os
import tempfile
import subprocess
import sys
from sequana.pipelines_common import get_pipeline_location as getpath

sharedir = getpath("rnaseq")
saccer3 = getpath("rnaseq") + "/Saccer3/"

#sequana_path = easydev.get_package_location('sequana_rnaseq')
#sharedir = os.sep.join([sequana_path , "sequana", 'data'])


def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = """sequana_pipelines_rnaseq --input-directory {} --working-directory {} --rnadiff-mode one_factor""".format(
        sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.rnaseq.main as m
    sys.argv = ["test", "--input-directory", sharedir, "--genome-directory",
        saccer3, "--force", "--aligner", "bowtie2", "--rnadiff-mode",
"one_factor",
        "--rRNA-feature", "rRNA_gene"]   # ideally should be rRNA but current
    m.main()


def test_version():
    cmd = "sequana_pipelines_rnaseq --version"
    subprocess.call(cmd.split())

