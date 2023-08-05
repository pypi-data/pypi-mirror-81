# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2020 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Module with package utils of the aea cli."""

import os
import re
import shutil
from pathlib import Path
from typing import List, Optional

import click
from jsonschema import ValidationError

from aea import AEA_DIR
from aea.cli.utils.constants import NOT_PERMITTED_AUTHORS
from aea.cli.utils.context import Context
from aea.cli.utils.loggers import logger
from aea.configurations.base import (
    AgentConfig,
    DEFAULT_AEA_CONFIG_FILE,
    PackageType,
    PublicId,
    _compute_fingerprint,
    _get_default_configuration_file_name_from_type,
)
from aea.configurations.constants import (
    DEFAULT_CONNECTION,
    DEFAULT_SKILL,
    LOCAL_PROTOCOLS,
)
from aea.configurations.loader import ConfigLoader
from aea.crypto.helpers import verify_or_create_private_keys
from aea.crypto.ledger_apis import DEFAULT_LEDGER_CONFIGS, LedgerApis
from aea.crypto.wallet import Wallet


ROOT = Path(".")


def verify_or_create_private_keys_ctx(
    ctx: Context, aea_project_path: Path = ROOT, exit_on_error: bool = True,
) -> None:
    """
    Verify or create private keys with ctx provided.

    :param ctx: Context
    """
    try:
        agent_config = verify_or_create_private_keys(aea_project_path, exit_on_error)
        if ctx is not None:
            ctx.agent_config = agent_config
    except ValueError as e:  # pragma: nocover
        click.ClickException(str(e))


def validate_package_name(package_name: str):
    """Check that the package name matches the pattern r"[a-zA-Z_][a-zA-Z0-9_]*".

    >>> validate_package_name("this_is_a_good_package_name")
    >>> validate_package_name("this-is-not")
    Traceback (most recent call last):
    ...
    click.exceptions.BadParameter: this-is-not is not a valid package name.
    """
    if re.fullmatch(PublicId.PACKAGE_NAME_REGEX, package_name) is None:
        raise click.BadParameter("{} is not a valid package name.".format(package_name))


def _is_valid_author_handle(author: str) -> bool:
    """
    Check that the author matches the pattern r"[a-zA-Z_][a-zA-Z0-9_]*".

    >>> _is_valid_author_handle("this_is_a_good_author_name")
    ...
    True
    >>> _is_valid_author_handle("this-is-not")
    ...
    False
    """
    if re.fullmatch(PublicId.AUTHOR_REGEX, author) is None:
        return False
    return True


def _is_permitted_author_handle(author: str) -> bool:
    """
    Check that the author handle is permitted.

    :param author: the author
    :retun: bool
    """
    result = author not in NOT_PERMITTED_AUTHORS
    return result


def try_get_item_source_path(
    path: str, author_name: Optional[str], item_type_plural: str, item_name: str
) -> str:
    """
    Get the item source path.

    :param path: the source path root
    :param author_name: the name of the author of the item
    :param item_type_plural: the item type (plural)
    :param item_name: the item name

    :return: the item source path
    """
    if author_name is None:
        source_path = os.path.join(path, item_type_plural, item_name)
    else:
        source_path = os.path.join(path, author_name, item_type_plural, item_name)
    if not os.path.exists(source_path):
        raise click.ClickException(
            'Item "{}" not found in source folder.'.format(item_name)
        )
    return source_path


def try_get_item_target_path(
    path: str, author_name: str, item_type_plural: str, item_name: str
) -> str:
    """
    Get the item target path.

    :param path: the target path root
    :param author_name the author name
    :param item_type_plural: the item type (plural)
    :param item_name: the item name

    :return: the item target path
    """
    target_path = os.path.join(path, author_name, item_type_plural, item_name)
    if os.path.exists(target_path):
        raise click.ClickException(
            'Item "{}" already exists in target folder.'.format(item_name)
        )
    return target_path


def get_package_path(
    ctx: Context, item_type: str, public_id: PublicId, is_vendor: bool = True
) -> str:
    """
    Get a vendorized path for a package.

    :param ctx: context.
    :param item_type: item type.
    :param public_id: item public ID.
    :param is_vendor: flag for vendorized path (True by defaut).

    :return: vendorized estenation path for package.
    """
    item_type_plural = item_type + "s"
    if is_vendor:
        return os.path.join(
            ctx.cwd, "vendor", public_id.author, item_type_plural, public_id.name
        )
    return os.path.join(ctx.cwd, item_type_plural, public_id.name)


def get_package_path_unified(ctx: Context, item_type: str, public_id: PublicId) -> str:
    """
    Get a path for a package, either vendor or not.

    That is:
    - if the author in the public id is not the same of the AEA project author,
      just look into vendor/
    - Otherwise, first look into local packages, then into vendor/.

    :param ctx: context.
    :param item_type: item type.
    :param public_id: item public ID.

    :return: vendorized estenation path for package.
    """
    vendor_path = get_package_path(ctx, item_type, public_id, is_vendor=True)
    if ctx.agent_config.author != public_id.author or not is_item_present(
        ctx, item_type, public_id, is_vendor=False
    ):
        return vendor_path
    return get_package_path(ctx, item_type, public_id, is_vendor=False)


def copy_package_directory(src: Path, dst: str) -> Path:
    """
     Copy a package directory to the agent vendor resources.

    :param src: source path to the package to be added.
    :param dst: str package destenation path.

    :return: copied folder target path.
    :raises SystemExit: if the copy raises an exception.
    """
    # copy the item package into the agent's supported packages.
    src_path = str(src.absolute())
    logger.debug("Copying modules. src={} dst={}".format(src_path, dst))
    try:
        shutil.copytree(src_path, dst)
    except Exception as e:
        raise click.ClickException(str(e))

    items_folder = os.path.split(dst)[0]
    Path(items_folder, "__init__.py").touch()
    return Path(dst)


def find_item_locally(ctx, item_type, item_public_id) -> Path:
    """
    Find an item in the local registry.

    :param ctx: the CLI context.
    :param item_type: the type of the item to load. One of: protocols, connections, skills
    :param item_public_id: the public id of the item to find.
    :return: path to the package directory (either in registry or in aea directory).
    :raises SystemExit: if the search fails.
    """
    item_type_plural = item_type + "s"
    item_name = item_public_id.name

    # check in registry
    registry_path = os.path.join(ctx.cwd, ctx.agent_config.registry_path)
    package_path = Path(
        registry_path, item_public_id.author, item_type_plural, item_name
    )
    config_file_name = _get_default_configuration_file_name_from_type(item_type)
    item_configuration_filepath = package_path / config_file_name
    if not item_configuration_filepath.exists():
        raise click.ClickException(
            "Cannot find {}: '{}'.".format(item_type, item_public_id)
        )

    # try to load the item configuration file
    try:
        item_configuration_loader = ConfigLoader.from_configuration_type(
            PackageType(item_type)
        )
        item_configuration = item_configuration_loader.load(
            item_configuration_filepath.open()
        )
    except ValidationError as e:
        raise click.ClickException(
            "{} configuration file not valid: {}".format(item_type.capitalize(), str(e))
        )

    # check that the configuration file of the found package matches the expected author and version.
    version = item_configuration.version
    author = item_configuration.author
    if item_public_id.author != author or (
        not item_public_id.package_version.is_latest
        and item_public_id.version != version
    ):
        raise click.ClickException(
            "Cannot find {} with author and version specified.".format(item_type)
        )

    return package_path


def find_item_in_distribution(  # pylint: disable=unused-argument
    ctx, item_type, item_public_id: PublicId
) -> Path:
    """
    Find an item in the AEA directory.

    :param ctx: the CLI context.
    :param item_type: the type of the item to load. One of: protocols, connections, skills
    :param item_public_id: the public id of the item to find.
    :return: path to the package directory (either in registry or in aea directory).
    :raises SystemExit: if the search fails.
    """
    item_type_plural = item_type + "s"
    item_name = item_public_id.name

    # check in aea dir
    registry_path = AEA_DIR
    package_path = Path(registry_path, item_type_plural, item_name)
    config_file_name = _get_default_configuration_file_name_from_type(item_type)
    item_configuration_filepath = package_path / config_file_name
    if not item_configuration_filepath.exists():
        raise click.ClickException(
            "Cannot find {}: '{}'.".format(item_type, item_public_id)
        )

    # try to load the item configuration file
    try:
        item_configuration_loader = ConfigLoader.from_configuration_type(
            PackageType(item_type)
        )
        item_configuration = item_configuration_loader.load(
            item_configuration_filepath.open()
        )
    except ValidationError as e:
        raise click.ClickException(
            "{} configuration file not valid: {}".format(item_type.capitalize(), str(e))
        )

    # check that the configuration file of the found package matches the expected author and version.
    version = item_configuration.version
    author = item_configuration.author
    if item_public_id.author != author or (
        not item_public_id.package_version.is_latest
        and item_public_id.version != version
    ):
        raise click.ClickException(
            "Cannot find {} with author and version specified.".format(item_type)
        )

    return package_path


def validate_author_name(author: Optional[str] = None) -> str:
    """
    Validate an author name.

    :param author: the author name (optional)
    """
    is_acceptable_author = False
    if (
        author is not None
        and _is_valid_author_handle(author)
        and _is_permitted_author_handle(author)
    ):
        is_acceptable_author = True
        valid_author = author
    while not is_acceptable_author:
        author_prompt = click.prompt(
            "Please enter the author handle you would like to use", type=str
        )
        valid_author = author_prompt
        if _is_valid_author_handle(author_prompt) and _is_permitted_author_handle(
            author_prompt
        ):
            is_acceptable_author = True
        elif not _is_valid_author_handle(author_prompt):
            is_acceptable_author = False
            click.echo(
                "Not a valid author handle. Please try again. "
                "Author handles must satisfy the following regex: {}".format(
                    PublicId.AUTHOR_REGEX
                )
            )
        elif not _is_permitted_author_handle(author_prompt):
            is_acceptable_author = False
            click.echo(
                "Not a permitted author handle. The following author handles are not allowed: {}".format(
                    NOT_PERMITTED_AUTHORS
                )
            )

    return valid_author


def is_fingerprint_correct(package_path: Path, item_config) -> bool:
    """
    Validate fingerprint of item before adding.

    :param package_path: path to a package folder.
    :param item_config: item configuration.

    :return: None.
    """
    fingerprint = _compute_fingerprint(
        package_path, ignore_patterns=item_config.fingerprint_ignore_patterns
    )
    return item_config.fingerprint == fingerprint


def register_item(ctx: Context, item_type: str, item_public_id: PublicId) -> None:
    """
    Register item in agent configuration.

    :param ctx: click context object.
    :param item_type: type of item.
    :param item_public_id: PublicId of item.

    :return: None.
    """
    logger.debug(
        "Registering the {} into {}".format(item_type, DEFAULT_AEA_CONFIG_FILE)
    )
    item_type_plural = item_type + "s"
    supported_items = getattr(ctx.agent_config, item_type_plural)
    supported_items.add(item_public_id)
    ctx.agent_loader.dump(
        ctx.agent_config, open(os.path.join(ctx.cwd, DEFAULT_AEA_CONFIG_FILE), "w")
    )


def is_item_present_unified(ctx: Context, item_type: str, item_public_id: PublicId):
    """
    Check if item is present, either vendor or not.

    That is:
    - if the author in the public id is not the same of the AEA project author,
      just look into vendor/
    - Otherwise, first look into local packages, then into vendor/.

    :param ctx: context object.
    :param item_type: type of an item.
    :param item_public_id: PublicId of an item.
    :return: True if the item is present, False otherwise.
    """
    is_in_vendor = is_item_present(ctx, item_type, item_public_id, is_vendor=True)
    if item_public_id.author != ctx.agent_config.author:
        return is_in_vendor
    return is_in_vendor or is_item_present(
        ctx, item_type, item_public_id, is_vendor=False
    )


def is_item_present(
    ctx: Context, item_type: str, item_public_id: PublicId, is_vendor: bool = True
) -> bool:
    """
    Check if item is already present in AEA.

    :param ctx: context object.
    :param item_type: type of an item.
    :param item_public_id: PublicId of an item.
    :param is_vendor: flag for vendorized path (True by defaut).

    :return: boolean is item present.
    """
    # check item presence only by author/package_name pair, without version.
    item_type_plural = item_type + "s"
    items_in_config = set(
        map(lambda x: (x.author, x.name), getattr(ctx.agent_config, item_type_plural))
    )
    item_path = get_package_path(ctx, item_type, item_public_id, is_vendor=is_vendor)
    return (item_public_id.author, item_public_id.name,) in items_in_config and Path(
        item_path
    ).exists()


def is_local_item(item_public_id: PublicId) -> bool:
    """
    Check whether the item public id correspond to a local package.

    If the provided item has version 'latest', only the prefixes are compared.
    Otherwise, the function will try to match the exact version occurrence among the local packages.
    """
    local_packages: List[PublicId] = [
        DEFAULT_CONNECTION,
        *LOCAL_PROTOCOLS,
        DEFAULT_SKILL,
    ]
    if item_public_id.package_version.is_latest:
        return any(item_public_id.same_prefix(other) for other in local_packages)
    return item_public_id in local_packages


def try_get_balance(  # pylint: disable=unused-argument
    agent_config: AgentConfig, wallet: Wallet, type_: str
) -> int:
    """
    Try to get wallet balance.

    :param agent_config: agent config object.
    :param wallet: wallet object.
    :param type_: type of ledger API.

    :retun: token balance.
    """
    try:
        if type_ not in DEFAULT_LEDGER_CONFIGS:  # pragma: no cover
            raise ValueError("No ledger api config for {} available.".format(type_))
        address = wallet.addresses[type_]
        balance = LedgerApis.get_balance(type_, address)
        if balance is None:  # pragma: no cover
            raise ValueError("No balance returned!")
        return balance
    except ValueError as e:  # pragma: no cover
        raise click.ClickException(str(e))
