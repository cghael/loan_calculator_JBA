import argparse
from math import ceil, log
import sys


def arguments_parsing():
    parser = argparse.ArgumentParser(description="The loan calculator able to work with \
    different types of payment and accept command-line arguments.")

    parser.add_argument("--type", choices=["annuity", "diff"], required=True,
                        help='You need to choose the type of payment: "annuity" or "diff" (differentiated)')

    parser.add_argument("--payment", type=float)
    parser.add_argument("--principal", type=float)  # loan
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)

    return parser.parse_args()


def arguments_errors_handling(args):
    params = [args.principal, args.payment, args.periods, args.interest]

    if args.type == "diff" and args.payment is not None:
        print("Incorrect parameters. You can't use 'type=diff' with '--payment' parameter")
        sys.exit(1)

    if args.interest is None:
        print("Incorrect parameters. Our loan calculator can't calculate the interest, \
it must always be provided.")
        sys.exit(1)

    if params.count(None) > 1:
        print("Incorrect parameters. Must be at least 3 parameters.")
        sys.exit(1)

    for i in params:
        if i is not None and i < 0:
            print("Incorrect parameters. Parameters cannot be negative.")
            sys.exit(1)


def print_periods(periods):
    months = periods % 12
    years = periods // 12

    if months == 0:
        if years == 1:
            output_str = "It will take 1 year to repay this loan!"
        else:
            output_str = "It will take {} years to repay this loan!".format(years)
    else:
        if years == 1:
            output_str = "It will take 1 year"
        else:
            output_str = "It will take {} years".format(years)

        if months == 1:
            output_str += " and 1 mounth to repay this loan!"
        else:
            output_str += " and {} months to repay this loan!".format(months)

    print(output_str)


def print_overpayment(args):
    overpayment = int((args.payment * args.periods) - args.principal)
    print(f"Overpayment = {overpayment}")


def print_overpayment_diff(args, total):
    overpayment = int(total - args.principal)
    print(f"\nOverpayment = {overpayment}")


def periods_calculation(args):
    i = args.interest / 1200
    args.periods = log((args.payment / (args.payment - i * args.principal)), 1 + i)
    if args.periods - int(args.periods) > 0:
        args.periods = int(args.periods) + 1
    print_periods(args.periods)


def principal_calculation(args):
    i = args.interest / 1200
    dividend = i * pow(1 + i, args.periods)
    divider = pow(1 + i, args.periods) - 1
    args.principal = int(args.payment / (dividend / divider))
    print("Your monthly payment = {}!".format(round(args.principal, 2)))


def payment_calculation(args):
    total_payments = 0

    if args.type == "diff":
        i = args.interest / 1200
        periods = args.periods
        m = 1
        p = args.principal
        n = periods

        while m <= periods:
            payment = (p / n) + i * (p - (p * (m - 1)) / n)
            payment = ceil(payment)
            print(f"Month {m}: payment is {payment}")
            total_payments += payment
            m += 1

    elif args.type == "annuity":
        i = args.interest / 1200
        dividend = i * pow(1 + i, args.periods)
        divider = pow(1 + i, args.periods) - 1
        args.payment = ceil(args.principal * (dividend / divider))
        print("Your monthly payment = {}!".format(args.payment))

    return total_payments


# ---------- START CALCULATOR ----------

def main():
    args = arguments_parsing()
    arguments_errors_handling(args)
    total_payments = 0

    if args.periods is None:
        periods_calculation(args)
    elif args.principal is None:
        principal_calculation(args)
    elif args.payment is None:
        total_payments = payment_calculation(args)

    if args.type == "diff":
        print_overpayment_diff(args, total_payments)
    else:
        print_overpayment(args)


if __name__ == "__main__":
    main()
