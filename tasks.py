import os
import shutil

from invoke import task

from lib import project
from lib.console import log_call
from lib.project import config


@task
@log_call
def clean(cmd):
    project.rmdir(config.build_dir)


@task
@log_call
def prepare_build(cmd):
    project.mkdir(config.build_dir)


@task(pre=[clean, prepare_build])
@log_call
def build_actor(cmd):
    project.glob_copy(config.src_dir, "Actor/**/*.png", config.build_dir)


@task(pre=[clean, prepare_build])
@log_call
def build_portrait(cmd):
    project.glob_copy(config.src_dir, "Portrait/**/*.png", config.build_dir)


@task(pre=[clean, prepare_build])
@log_call
def build_template(cmd):
    project.glob_copy(config.src_dir, "Template/*.json", config.build_dir, ".txt")


@task(pre=[clean, prepare_build])
@log_call
def build_meta(cmd):
    project.copy_file(os.path.join(config.src_dir, "preview.jpg"), config.build_dir, config.build_dir)
    project.copy_file(os.path.join(config.root, "README.md"), config.build_dir, config.build_dir)
    project.copy_file(os.path.join(config.root, "LICENSE"), config.build_dir, config.build_dir)


@task(pre=[clean, prepare_build])
@log_call
def build_package_xml(cmd):
    project.copy_template(os.path.join(config.src_dir, "package.xml"), config.build_dir, config.build_dir)


@task(pre=[build_actor, build_portrait, build_template, build_meta, build_package_xml], default=True)
@log_call
def build(cmd):
    pass


@task(pre=[build])
@log_call
def install(cmd, path: str = config.install_dir):
    package_dir = os.path.join(os.path.abspath(path), config.package_name)
    project.rmdir(package_dir)
    project.mkdir(package_dir)
    shutil.copytree(config.build_dir, package_dir, dirs_exist_ok=True)
    print(f"Installed: {package_dir}")


@task
@log_call
def install_templates(cmd, path: str = config.install_template_dir):
    template_dir = os.path.abspath(path)
    project.glob_copy(os.path.join(config.src_dir, "Template"), "*.json", template_dir, ".txt")
    print(f"Installed: {template_dir}")
