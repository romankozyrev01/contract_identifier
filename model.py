from dataclasses import dataclass
import enum
from constants import IRC20_INTERFACE


class Protocol(str, enum.Enum):
    ERC20 = "ERC20"
    OTHER = "OTHER"

    def __str__(self) -> str:
        return self.value


@dataclass
class Contract:
    protocol: str
    version: str
    address: str
    status: str
    subcontract_interfaces: list[set]


def identify_protocol(contract: Contract) -> str:
    if is_erc20_contract(contract):
        return Protocol.ERC20

    return Protocol.OTHER


def is_erc20_contract(contract: Contract) -> bool:
    subcontracts = contract.subcontract_interfaces

    for interface in subcontracts:
        if IRC20_INTERFACE.issubset(interface):
            return True

    return False
