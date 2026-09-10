"""Real model, local state, scripted volunteer replies. No outbound email."""
import json
from pathlib import Path
from .agent import build_agent
from .domain import load_scenario
from .workflow import Workflow


def run(path, outcome='covered'):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    flow = Workflow(path)
    now = ['2026-09-11T18:00:00-04:00']
    # Validate model configuration before persisting the initial fixture.
    agent = build_agent(flow, lambda: now[0])
    flow.start(load_scenario(), now[0])
    flow.approve(now[0], dispatch=False)
    transcript = []
    def turn(prompt):
        response = agent(prompt)
        transcript.append({'prompt':prompt, 'response':str(response)})
        Path(str(path)+'.transcript.json').write_text(json.dumps(transcript, indent=2))
        print(str(response))
    print('REAL BEDROCK AGENT / SYNTHETIC VOLUNTEERS AND REPLIES / NO EMAIL DELIVERY')
    turn('The coordinator approved synthetic backup outreach. Inspect and advance coverage, then report status.')
    state = flow.snapshot()
    pending = [o for o in state['offers'] if o['status']=='pending']
    if len(pending)!=1 or pending[0]['volunteer_id']!='v2':
        raise RuntimeError('Agent did not create expected initial offer; inspect saved state.')
    flow.reply(pending[0]['token'], 'decline', now[0], dispatch=False)
    turn('A scripted volunteer decline was recorded by the application. Inspect and advance coverage.')
    state = flow.snapshot()
    pending = [o for o in state['offers'] if o['status']=='pending']
    if len(pending)!=1 or pending[0]['volunteer_id']!='v3':
        raise RuntimeError('Agent did not create replacement offer; inspect saved state.')
    if outcome=='covered':
        flow.reply(pending[0]['token'], 'accept', now[0], dispatch=False)
        turn('An explicit scripted acceptance was recorded by the application. Inspect and report the actual booking.')
    else:
        now[0]='2026-09-11T18:15:00-04:00'
        turn('The application clock advanced to the offer deadline. Inspect and advance coverage; report any remaining gap.')
    final = flow.snapshot()
    expected = 'covered' if outcome=='covered' else 'needs_coordinator'
    if final['status'] != expected:
        raise RuntimeError(f'Expected {expected}, got {final["status"]}; inspect saved state.')
    print(f'Persisted result verified: {expected}')
    return final
