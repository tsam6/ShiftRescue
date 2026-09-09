import argparse
import json
from .domain import coverage_plan, load_scenario


def main():
    parser = argparse.ArgumentParser(description="ShiftRescue synthetic prototype")
    parser.add_argument("mode", choices=["demo", "agent"], nargs="?", default="demo")
    args = parser.parse_args()
    if args.mode == "demo":
        print("OFFLINE FIXTURE CHECK — no model invocation or email delivery")
        print(json.dumps(coverage_plan(load_scenario()), indent=2))
    else:
        from .agent import build_agent
        try:
            agent = build_agent()
        except ValueError as error:
            parser.error(str(error))
        agent("Inspect the sample cancellation and propose an outreach plan for coordinator review.")


if __name__ == "__main__":
    main()
