from numpy import random
import polars as pl
import datetime
import os
import typer
from typing_extensions import Annotated
from pathlib import Path
import configparser
from loguru import logger


# Powerball rules: 5 numbers range from 1 to 69
# 1 powerball number range from 1 to 26

# use configparser to read initial value


def get_init(ini_path) -> int:
    logger.info("initialize lottery configuration")
    config = configparser.ConfigParser()
    config.read(ini_path)

    # logger.info("Config: {config}")

    maxFiveNumber = int(config["POWERBALL"]["maxFiveNumber"])
    beginNumber = int(config["POWERBALL"]["beginNumber"])
    maxPowerBall = int(config["POWERBALL"]["maxPowerBall"])
    fiveSize = int(config["POWERBALL"]["fiveSize"])
    oneSize = int(config["POWERBALL"]["oneSize"])

    return maxFiveNumber, beginNumber, maxPowerBall, fiveSize, oneSize


def get_time_now() -> str:
    now = datetime.datetime.now()
    dt = now.strftime("%m/%d/%Y, %H:%M:%S")
    return dt


def get_random_number(beginNumber, endNumber, sizeNumber) -> random:
    rn = random.randint(beginNumber, endNumber, sizeNumber)
    return rn


# using with open to append data
# no need to close file. Nice!!!


def write_to_file(fileName, dataFrame):
    logger.info("Writing to file")

    with open(fileName, mode="ab") as f:
        if os.stat(fileName).st_size > 0:
            dataFrame.write_csv(f, include_header=False)
        else:
            dataFrame.write_csv(f)


PROGRAM_NAME = "data/" + Path(__file__).stem
# print(PROGRAM_NAME)


def main(
    counter: Annotated[
        int, typer.Argument(help="Number of powerball generate", min=1)
    ] = 1,
    ini_path: Annotated[Path, typer.Argument(help="ini file")] = PROGRAM_NAME + ".ini",
    path: Annotated[Path, typer.Argument(help="CSV output file")] = PROGRAM_NAME
    + ".csv",
    log_path: Annotated[Path, typer.Argument(help="Log file")] = PROGRAM_NAME + ".log",
):
    # adding log
    logger.add(log_path)
    logger.info("Starting the lottery...")

    # getting initial value from init file
    maxFiveNumber, beginNumber, maxPowerBall, fiveSize, oneSize = get_init(ini_path)

    for _ in range(counter):
        # using numpy to random generate to pick size,
        # 5 sizeNumber in this case
        x = get_random_number(beginNumber, maxFiveNumber, fiveSize)

        # using numpy to random generate pick 1 sizePowerBallNumber
        pb = get_random_number(beginNumber, maxPowerBall, oneSize)

        print(x)

        # using Polars DataFrame
        # Need to convert a NDArray to string
        try:
            df = pl.DataFrame(
                {
                    "currentDate": get_time_now(),
                    # "number": s,
                    "number": str(x)[1:-1],
                    "powerBall": str(pb)[1:-1],
                }
            )
        except BaseException:
            print("Error creating data frame {df}")
        else:
            print(df)

        # write result to file
        write_to_file(fileName=path, dataFrame=df)


if __name__ == "__main__":
    typer.run(main)
