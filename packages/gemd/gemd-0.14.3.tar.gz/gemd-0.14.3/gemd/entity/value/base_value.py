"""Base class for all values."""
from gemd.entity.dict_serializable import DictSerializable


class BaseValue(DictSerializable):
    """
    Base class for all values.

    "Value" is a generic term for the information contained in an
    :class:`attribute <gemd.entity.attribute.base_attribute.BaseAttribute>`.
    A value may be one of the following types: `RealValue`, `IntegerValue`, `Categorical`.
    """

    typ = "value"
