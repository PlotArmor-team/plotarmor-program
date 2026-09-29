import subprocess, pathlib, sys, datetime, os
name, cwd, *cmd=sys.argv[1:]
p=pathlib.Path('/tmp/m2-pass4-independent/logs')/(name+'.txt')
with p.open('w') as f:
 f.write('UTC: '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\nCWD: '+cwd+'\nARGV: '+repr(cmd)+'\n'); f.flush()
 env=os.environ.copy();env['NO_DNA']='1'
 proc=subprocess.Popen(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,text=True)
 for line in proc.stdout:
  f.write(line);f.flush(); print(line,end='',flush=True)
 rc=proc.wait();f.write('\nEXIT CODE: '+str(rc)+'\n');print('EXIT CODE:',rc)
sys.exit(rc)
