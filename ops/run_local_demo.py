"""Start the isolated local demo without exposing credential values."""
import argparse
import os
from pathlib import Path
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


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env-file',type=Path,default=ROOT/'runs/private/local-demo.env')
    parser.add_argument('--api-only',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args(); env=load_environment(args.env_file)
    if env.get('MODEL_PROVIDER')!='openai':raise SystemExit('Set MODEL_PROVIDER=openai in the private demo file.')
    print('OpenAI key configured: '+str(bool(env.get('OPENAI_API_KEY'))))
    print('Langfuse keys configured: '+str(all(env.get(k) for k in ('LANGFUSE_PUBLIC_KEY','LANGFUSE_SECRET_KEY','LANGFUSE_BASE_URL'))))
    if args.check:return 0
    env['COMMIT_SHA']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    children=[]
    try:
        children.append(subprocess.Popen([sys.executable,'-m','uvicorn','regulatory_agent.api:app','--app-dir','src',
            '--host','127.0.0.1','--port','8150','--no-proxy-headers'],cwd=ROOT,env=env))
        if not args.api_only:
            children.append(subprocess.Popen(['node','node_modules/vite/bin/vite.js','--host','127.0.0.1',
                '--port','5185','--strictPort'],cwd=ROOT/'src/web',env=env))
        print('Local demo: http://127.0.0.1:5185/')
        return children[0].wait()
    except KeyboardInterrupt:
        return 0
    finally:
        for child in children:
            if child.poll() is None:child.terminate(); child.wait(timeout=10)


if __name__=='__main__':raise SystemExit(main())
