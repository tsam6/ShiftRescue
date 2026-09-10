"""Real Strands event-loop tests with a scripted model, not Bedrock inference."""
from strands.models import Model
from shiftrescue.agent import build_agent, workflow_tools, ModelCallLimit
from shiftrescue.domain import load_scenario
from shiftrescue.workflow import Workflow
from types import SimpleNamespace

NOW='2026-09-11T18:00:00-04:00'


class ScriptedModel(Model):
    def __init__(self):
        self.calls=0
    def update_config(self, **kwargs):
        pass
    def get_config(self):
        return {}
    async def structured_output(self, *args, **kwargs):
        raise NotImplementedError
        yield
    async def stream(self, messages, tool_specs=None, system_prompt=None, **kwargs):
        self.calls+=1
        yield {'messageStart': {'role':'assistant'}}
        if self.calls <= 2:
            name='inspect_coverage' if self.calls==1 else 'advance_coverage'
            yield {'contentBlockStart':{'start':{'toolUse':{'toolUseId':str(self.calls),'name':name}}}}
            yield {'contentBlockDelta':{'delta':{'toolUse':{'input':'{}'}}}}
            yield {'contentBlockStop':{}}
            yield {'messageStop':{'stopReason':'tool_use'}}
        else:
            yield {'contentBlockDelta':{'delta':{'text':'Synthetic request prepared; awaiting reply.'}}}
            yield {'contentBlockStop':{}}
            yield {'messageStop':{'stopReason':'end_turn'}}


def setup(tmp_path):
    flow=Workflow(tmp_path/'agent.sqlite3')
    flow.start(load_scenario(),NOW)
    return flow


def test_strands_loop_executes_persistent_tools(tmp_path):
    flow=setup(tmp_path)
    flow.approve(NOW,dispatch=False)
    model=ScriptedModel()
    agent=build_agent(flow,lambda:NOW,model=model)
    result=agent('Inspect and advance coverage.')
    assert 'awaiting reply' in str(result)
    assert model.calls==3
    assert flow.snapshot()['offers'][0]['volunteer_id']=='v2'
    assert flow.snapshot()['booking'] is None


def test_agent_tools_cannot_approve_forge_reply_or_leak_offer_tokens(tmp_path):
    flow=setup(tmp_path)
    tools=workflow_tools(flow,lambda:NOW)
    assert [t.tool_name for t in tools]==['inspect_coverage','advance_coverage']
    assert tools[1]()['outbox']==[]
    flow.approve(NOW,dispatch=False)
    public=tools[1]()
    assert 'token' not in public['offers'][0]
    assert public['booking'] is None


def test_call_limit_stops_before_extra_request():
    guard=ModelCallLimit(2)
    events=[SimpleNamespace(cancel=False) for _ in range(3)]
    for event in events:
        guard.before_call(event)
    assert not events[0].cancel and not events[1].cancel
    assert events[2].cancel
    assert guard.calls==2
