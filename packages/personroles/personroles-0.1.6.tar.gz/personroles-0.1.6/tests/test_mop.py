#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_person.py
"""Tests for `person` package."""
import pytest
from context import helpers  # noqa
from context import mop_role

# pylint: disable=redefined-outer-name


def test_person_MoP(mop_fixture):
    # pylint: disable=W0612, W0613

    mop = mop_role.MoP(
        "14",
        "NRW",
        "Grüne",
        "Alfons-Reimund",
        "Hubbeldubbel",
        peer_title="auf der",
        electoral_ward="Ennepe-Ruhr-Kreis I",
        minister="JM",
    )

    assert mop.legislature == "14"  # nosec
    assert mop.first_name == "Alfons-Reimund"  # nosec
    assert mop.last_name == "Hubbeldubbel"  # nosec
    assert mop.gender == "male"  # nosec
    assert mop.peer_preposition == "auf der"  # nosec
    assert mop.party_name == "Grüne"  # nosec
    assert mop.parties == [  # nosec
        helpers.Party(
            party_name="Grüne", party_entry="unknown", party_exit="unknown"
        )  # noqa  # nosec
    ]  # noqa  # nosec
    assert mop.ward_no == 105  # nosec
    assert mop.minister == "JM"  # nosec

    mop.add_Party("fraktionslos")
    assert mop.party_name == "fraktionslos"  # nosec
    assert mop.parties == [  # nosec
        helpers.Party(
            party_name="Grüne", party_entry="unknown", party_exit="unknown"
        ),  # noqa  # nosec
        helpers.Party(
            party_name="fraktionslos",
            party_entry="unknown",
            party_exit="unknown",  # noqa  # nosec
        ),
    ]


def test_person_NotInRangeError(notinrange_fixture):
    # pylint: disable=W0612, W0613
    mop = mop_role.MoP

    with pytest.raises(helpers.NotInRange):
        mop("100", "NRW", "SPD", "Alfons-Reimund", "Hubbeldubbel")
