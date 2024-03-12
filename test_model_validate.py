import pytest
import model

import os

from parsers import SOLFileParser


@pytest.fixture
def source_code_factory():
    def wrapper(filename: str):
        with open(os.path.join(os.path.dirname(__file__), filename), "r") as f:
            return f.read()

    return wrapper


@pytest.fixture
def usdt_contract(source_code_factory):
    return model.Contract(
        protocol="",
        version="1.0.0",
        address="0x0000000000000000000000000000000000000000",
        status="active",
        subcontract_interfaces=SOLFileParser().parse(
            source_code_factory("data/usdt_source_code.sol")
        ),
    )


@pytest.fixture
def shiba_inu_contract(source_code_factory):
    return model.Contract(
        protocol="",
        version="1.0.0",
        address="0x0000000000000000000000000000000000000000",
        status="active",
        subcontract_interfaces=SOLFileParser().parse(
            source_code_factory("data/shiba_inu_source_code.sol")
        ),
    )


def test_can_identify_usdt_implements_erc20_protocol(usdt_contract: model.Contract):
    expected_result = "ERC20"
    result = model.identify_protocol(contract=usdt_contract)

    assert result == expected_result


def test_can_identify_shiba_inu_implements_erc20_protocol(
    shiba_inu_contract: model.Contract,
):
    # test fails because shiba_inu_source_code.sol does not implement erc20 events,
    # so maybe events should not be included in ERC20...

    expected_result = "ERC20"
    result = model.identify_protocol(contract=shiba_inu_contract)

    assert result == expected_result
