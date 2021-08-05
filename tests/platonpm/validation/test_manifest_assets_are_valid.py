import json
import pytest

from platonpm import (
    ASSETS_DIR,
)
from platonpm.exceptions import (
    InsufficientAssetsError,
)
from platonpm.validation.manifest import (
    validate_manifest_against_schema,
)

SOURCES_GLOB = "**/*.json"


def get_all_manifest_paths():
    # Expects all json in platonpm/assets to be either compiler_output or a manifest
    all_use_case_json = set(ASSETS_DIR.glob(SOURCES_GLOB)) - set(
        (ASSETS_DIR / "spec").glob(SOURCES_GLOB)
    )
    all_manifests = [json for json in all_use_case_json if json.name == "v3.json"]
    if not all_manifests:
        raise InsufficientAssetsError(
            "Error importing manifests for validation, "
            "no v3 manifests found in `platonpm/platonpm-spec` submodule"
        )
    return all_manifests


@pytest.fixture(params=get_all_manifest_paths())
def manifest(request):
    return json.loads(request.param.read_text())


def test_manifest_assets_are_valid(manifest):
    assert validate_manifest_against_schema(manifest) is None
