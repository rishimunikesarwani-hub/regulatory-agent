"""Start the isolated local demo without exposing credential values."""
import argparse
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
KEYS={'MODEL_PROVIDER','OPENAI_API_KEY','LANGFUSE_PUBLIC_KEY','LANGFUSE_SECRET_KEY','LANGFUSE_BASE_URL','LANGFUSE_CAPTURE_CONTENT'}


def load_environment(path):
    env=os.environ.copy()
    if path.exists():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if not line.strip() or line.lstrip().startswith('#'):continue
            key,separator,value=line.partition('=')
            if not separator or key.strip() not in KEYS:raise ValueError('invalid_demo_configuration')
            value=value.strip()
            if len(value)>=2 and value[0]==value[-1] and value[0] in ('"',"'"):value=value[1:-1]
            env[key.strip()]=value
    env.update(APP_ENV='local',DEVELOPMENT_USER='slice-05-rishi-feedback',LOCAL_WEB_PORT='5185',LOCAL_API_PORT='8150',
        CASES_DB_PATH=str(ROOT/'runs/private/slice-05/feedback.sqlite'),PYTHONPATH=str(ROOT/'src'))
    return env


def port(value):
    try:
        number=int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('Use a port between 1 and 65535.') from None
    if not 1<=number<=65535:raise argparse.ArgumentTypeError('Use a port between 1 and 65535.')
    return str(number)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env-file',type=Path,default=ROOT/'runs/private/local-demo.env')
    parser.add_argument('--api-only',action='store_true')
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--web-port',type=port,default='5185')
    parser.add_argument('--api-port',type=port,default='8150')
    parser.add_argument('--db-path',type=Path,default=Path('runs/private/slice-05/feedback.sqlite'))
    args=parser.parse_args(); env=load_environment(args.env_file)
    database=(ROOT/args.db_path).resolve()
    if args.web_port==args.api_port:raise SystemExit('Use different web and API ports.')
    if not database.is_relative_to((ROOT/'runs/private').resolve()):
        raise SystemExit('Keep the database under runs/private/.')
    env.update(LOCAL_WEB_PORT=args.web_port,LOCAL_API_PORT=args.api_port,CASES_DB_PATH=str(database))
    if env.get('MODEL_PROVIDER')!='openai':raise SystemExit('Set MODEL_PROVIDER=openai in the private demo file.')
    ready=bool(env.get('OPENAI_API_KEY','').strip())
    print('OpenAI key configured: '+str(ready))
    print('Langfuse keys configured: '+str(all(env.get(k) for k in ('LANGFUSE_PUBLIC_KEY','LANGFUSE_SECRET_KEY','LANGFUSE_BASE_URL'))))
    if not ready:raise SystemExit('Set OPENAI_API_KEY in the private demo file. Your key is never included in GitHub.')
    if args.check:return 0
    node=shutil.which('node')
    if not args.api_only and (not node or not (ROOT/'src/web/node_modules/vite/bin/vite.js').is_file()):
        raise SystemExit('Install Node.js, then run npm ci from src/web.')
    for value in ([args.api_port] if args.api_only else [args.api_port,args.web_port]):
        with socket.socket() as probe:
            try:probe.bind(('127.0.0.1',int(value)))
            except OSError:raise SystemExit('A required local port is already in use. Select different ports.') from None
    env['COMMIT_SHA']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip() if (ROOT/'.git').exists() else 'source-archive'
    children=[]
    try:
        children.append(subprocess.Popen([sys.executable,'-m','uvicorn','regulatory_agent.api:app','--app-dir','src',
            '--host','127.0.0.1','--port',args.api_port,'--no-proxy-headers'],cwd=ROOT,env=env))
        if not args.api_only:
            children.append(subprocess.Popen([node,'node_modules/vite/bin/vite.js','--host','127.0.0.1',
                '--port',args.web_port,'--strictPort'],cwd=ROOT/'src/web',env=env))
        print('Local API: http://127.0.0.1:'+args.api_port+'/api/health')
        if not args.api_only:print('Local demo: http://127.0.0.1:'+args.web_port+'/')
        return children[0].wait()
    except KeyboardInterrupt:
        return 0
    finally:
        for child in children:
            if child.poll() is None:child.terminate(); child.wait(timeout=10)


if __name__=='__main__':raise SystemExit(main())
