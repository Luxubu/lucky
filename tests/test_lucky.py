# from lucky import get_init
import lucky.lucky as ll

# get_init("data/lucky.ini") -> int
#     return maxFiveNumber, beginNumber, maxPowerBall, fiveSize, oneSize


def test_get_init():
    maxFiveNumber, beginNumber, maxPowerBall, fiveSize, oneSize = ll.get_init(
        "data/lucky.ini"
    )
    assert (maxFiveNumber, beginNumber, maxPowerBall, fiveSize, oneSize) == (
        69,
        1,
        26,
        5,
        1,
    )


def test_fail_get_init():
    maxFiveNumber, beginNumber, maxPowerBall, fiveSize, oneSize = ll.get_init(
        "data/lucky.ini"
    )
    assert (maxFiveNumber, beginNumber, maxPowerBall, fiveSize, oneSize) != (
        70,
        1,
        26,
        5,
        1,
    )
