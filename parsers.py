from solidity_parser import parser
from exceptions import ContractParsingException
from constants import IRC20_INTERFACE


def collect_interface(current_contract: dict, contracts: dict):
    interface = current_contract["methods"]
    interface.extend(current_contract["events"])

    for base in current_contract["baseContracts"]:
        try:
            base = contracts[base]
        except KeyError:
            continue
        interface.extend(collect_interface(base, contracts))

    return interface


class SOLFileParser:
    def parse(self, source_code):
        try:
            root = parser.parse(source_code)
            contracts = {}
            for children in root["children"]:
                contract = {}

                if (
                    children["type"] == "ContractDefinition"
                    and children["kind"] == "contract"
                ):
                    contract = {
                        "methods": [],
                        "events": [],
                        "baseContracts": [],
                    }
                    for base_contract in children["baseContracts"]:
                        if base_contract["type"] == "InheritanceSpecifier":
                            contract["baseContracts"].append(
                                base_contract["baseName"]["namePath"]
                            )

                    for node in children["subNodes"]:
                        if node["type"] == "EventDefinition":
                            contract["events"].append(node["name"])
                        elif (
                            node["type"] == "FunctionDefinition"
                            and node["name"] in IRC20_INTERFACE
                        ):
                            contract["methods"].append(node["name"])

                    if not contract["methods"] and not contract["baseContracts"]:
                        continue

                    contracts.update({children["name"]: contract})

            for _, contract in contracts.items():
                yield set(collect_interface(contract, contracts))

        except Exception:
            raise ContractParsingException()
