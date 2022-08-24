import finergy


# accounts
class PartyFrozen(finergy.ValidationError):
	pass


class InvalidAccountCurrency(finergy.ValidationError):
	pass


class InvalidCurrency(finergy.ValidationError):
	pass


class PartyDisabled(finergy.ValidationError):
	pass


class InvalidAccountDimensionError(finergy.ValidationError):
	pass


class MandatoryAccountDimensionError(finergy.ValidationError):
	pass
