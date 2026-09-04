from datetime import date, timedelta


def _format_dob(dob: date) -> str:
    return dob.strftime("%d-%m-%Y")


_today = date.today()
_exactly_18_birthday = _today.replace(year=_today.year - 18)

OVER_18_DOB = _format_dob(_exactly_18_birthday - timedelta(days=1))

AGE_VERIFICATION_TEST_DATA = [
    (
        "over_18",
        OVER_18_DOB,
        "success",
        "You are of age",
    ),
    (
        "exactly_18",
        _format_dob(_exactly_18_birthday),
        "success",
        "You are of age",
    ),
    (
        "under_18",
        _format_dob(_exactly_18_birthday + timedelta(days=1)),
        "fail",
        "You are underage",
    ),
]
