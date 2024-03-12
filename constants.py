IRC20_METHODS: list[str] = [
    "totalSupply",
    "balanceOf",
    "transfer",
    "allowance",
    "approve",
    "transferFrom",
]

IRC20_EVENTS: list[str] = [
    "Transfer",
    "Approval",
]

IRC20_INTERFACE = set(IRC20_METHODS + IRC20_EVENTS)
