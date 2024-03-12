import model


def identify_protocol(contracts_repo, parser):
    contracts = contracts_repo.contracts_iterator()
    processed = []
    for contract in contracts:
        parser.parse(contract.source_code)

        try:
            protocol = model.identify_protocol(contract)
        except Exception:
            contract.status = "FAILURE"
        else:
            contract.status = "SUCCESS"
            contract.protocol = protocol

        processed.append(contract)

        contracts_repo.batch_save(processed)
