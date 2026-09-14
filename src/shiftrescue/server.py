"""Loopback-only coordinator demo. No cloud calls or external message delivery."""
from datetime import timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib.resources import files
from pathlib import Path
import json
import secrets
from .domain import coverage_plan, instant, load_scenario
from .workflow import Workflow


class Demo:
    def __init__(self, path):
        self.path=Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.flow=Workflow(self.path)
        try:
            self.flow.snapshot()
        except ValueError:
            self.flow.start(load_scenario(), '2026-09-11T18:00:00-04:00')

    def view(self):
        state=self.flow.snapshot()
        # Local demo exposes simulated offer capabilities to the volunteer-reply panel.
        return dict(state=state, plan=coverage_plan(state['scenario']))

    def action(self, action, payload):
        now=self.flow.snapshot()['last_time']
        if action=='approve':
            self.flow.approve(now, candidate_ids=payload.get('candidates', []))
        elif action=='reply':
            self.flow.reply(payload['token'],payload['decision'],now)
        elif action=='time':
            minutes=payload.get('minutes')
            if minutes not in (5,10,15):
                raise ValueError('Choose 5, 10, or 15 minutes')
            self.flow.tick((instant(now)+timedelta(minutes=minutes)).isoformat())
        elif action=='new':
            path=self.path.with_name(self.path.stem+'-'+secrets.token_hex(4)+'.sqlite3')
            self.flow=Workflow(path)
            self.flow.start(load_scenario(), '2026-09-11T18:00:00-04:00')
        else:
            raise ValueError('Unknown action')
        return self.view()


def serve(path, port):
    app=Demo(path)
    session=secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def send(self, status, body, content_type='application/json'):
            body=body.encode()
            self.send_response(status)
            self.send_header('Content-Type',content_type)
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.end_headers()
            self.wfile.write(body)
        def do_GET(self):
            if self.headers.get('Host') not in (f'127.0.0.1:{port}',f'localhost:{port}'):
                return self.send(403,'{}')
            if self.path=='/':
                html=files('shiftrescue').joinpath('web/index.html').read_text().replace('__SESSION__',session)
                self.send(200,html,'text/html; charset=utf-8')
            elif self.path=='/api/state':
                self.send(200,json.dumps(app.view()))
            else:
                self.send(404,'{}')
        def do_POST(self):
            if self.headers.get('X-Demo-Session') != session or self.headers.get('Host') not in (f'127.0.0.1:{port}',f'localhost:{port}'):
                return self.send(403,json.dumps({'error':'Invalid local session'}))
            try:
                length=int(self.headers.get('Content-Length','0'))
                if length<0 or length>10000:
                    raise ValueError('Request too large')
                payload=json.loads(self.rfile.read(length))
                result=app.action(self.path.removeprefix('/api/'),payload)
                self.send(200,json.dumps(result))
            except (ValueError, KeyError, TypeError) as error:
                self.send(400,json.dumps({'error':str(error)}))
    server=HTTPServer(('127.0.0.1',port),Handler)
    print(f'ShiftRescue local demo: http://127.0.0.1:{port} — no AI calls or email delivery',flush=True)
    server.serve_forever()
