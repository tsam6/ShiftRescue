import argparse
import json
from .domain import coverage_plan, load_scenario


def main():
    parser = argparse.ArgumentParser(description="ShiftRescue synthetic prototype")
    parser.add_argument("mode", choices=["demo", "simulate", "agent", "live-demo", "serve"], nargs="?", default="demo")
    parser.add_argument("--database", default="runtime/demo.sqlite3", help="New SQLite file for a simulation")
    parser.add_argument("--outcome", choices=["covered", "unfilled"], default="covered")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if args.mode == "serve":
        from .server import serve
        serve(args.database, args.port)
    elif args.mode == "demo":
        print("OFFLINE FIXTURE CHECK — no model invocation or email delivery")
        print(json.dumps(coverage_plan(load_scenario()), indent=2))
    elif args.mode == "simulate":
        from pathlib import Path
        from .workflow import Workflow
        path = Path(args.database)
        path.parent.mkdir(parents=True, exist_ok=True)
        flow = Workflow(path)
        try:
            now = "2026-09-11T18:00:00-04:00"
            flow.start(load_scenario(), now)
            first = flow.approve(now)["offers"][-1]
            state = flow.reply(first["token"], "decline", now)
            if args.outcome == "covered":
                state = flow.reply(state["offers"][-1]["token"], "accept", now)
            else:
                state = flow.tick("2026-09-11T18:15:00-04:00")
        except ValueError as error:
            parser.error(str(error))
        print("LOCAL SIMULATION — scripted replies, no AI calls or email delivery")
        for event in state["events"]:
            print(f"{event['time']} | {event['kind']} | {event['detail']}")
        print(f"Result: {state['status']}; booking: {state['booking']}")
        print(f"Saved to {path.resolve()}")
    elif args.mode == "live-demo":
        from .live_demo import run
        try:
            run(args.database, args.outcome)
        except (ValueError, RuntimeError) as error:
            parser.error(str(error))
    else:
        from .agent import build_agent
        try:
            agent = build_agent()
        except ValueError as error:
            parser.error(str(error))
        print(agent("Inspect the sample cancellation and propose an outreach plan for coordinator review."))


if __name__ == "__main__":
    main()
