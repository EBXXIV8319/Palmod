import os, subprocess, pathlib, re
root=pathlib.Path(__file__).resolve().parents[1]
b=root/'build'; sdk=b/'RE-UE4SS'
vs=pathlib.Path(r'C:\Program Files\Microsoft Visual Studio\2022\Community')
raw=subprocess.check_output(f'cmd.exe /d /s /c ""{vs / "Common7/Tools/VsDevCmd.bat"}" -arch=x64 >nul && set"',text=True)
env=os.environ.copy()
for line in raw.splitlines():
 if '=' in line:
  k,v=line.split('=',1);env[k.upper()]=v
sdkroot=b/'winsdk'
env['INCLUDE']=';'.join([str(sdkroot/'sdk/include/um'),str(sdkroot/'sdk/include/shared'),str(sdkroot/'sdk/include/ucrt'),env.get('INCLUDE','')])
env['LIB']=';'.join([str(sdkroot/'sdk/lib/um/x86_64'),str(sdkroot/'sdk/lib/ucrt/x86_64'),env.get('LIB','')])
os.environ.update(env)
out=b/'native';out.mkdir(exist_ok=True)
def run(args):
 subprocess.run([str(x) for x in args],env=env,cwd=out,check=True)
dll=pathlib.Path(r'E:\SteamLibrary\steamapps\common\Palworld\Mods\NativeMods\UE4SS\UE4SS.dll')
exports=subprocess.check_output(['dumpbin.exe','/exports',str(dll)],env=env,text=True)
names=[m.group(1) for l in exports.splitlines() if (m:=re.match(r'\s+\d+\s+[0-9A-F]+\s+[0-9A-F]+\s+(\S+)',l))]
(out/'UE4SS.def').write_text('LIBRARY UE4SS.dll\nEXPORTS\n'+'\n'.join(names))
run(['lib.exe','/nologo','/def:UE4SS.def','/machine:x64','/out:UE4SS.lib'])
incs=[sdk/'UE4SS/include',sdk/'deps/first/Unreal/generated_include',sdk/'deps/first/Unreal/include/Unreal',sdk/'deps/first/Unreal/include/Unreal/Core',b/'zydis/include',b/'zydis/dependencies/zycore/include',b/'fmt/include',b/'imgui',b/'textedit',b/'minhook/include']
incs += list((sdk/'deps/first').glob('*/include'))
flags=['/nologo','/std:c++20','/EHsc','/MD','/O2','/utf-8','/DUNICODE','/D_UNICODE','/DFMT_HEADER_ONLY','/DRC_IS_ANSI=0','/DUE_BUILD_SHIPPING=1','/DUE_GAME','/DZYDIS_STATIC_BUILD','/DZYCORE_STATIC_BUILD','/DHAS_INPUT','/DPLATFORM_WINDOWS','/DPLATFORM_MICROSOFT','/DOVERRIDE_PLATFORM_HEADER_NAME=Windows','/DUBT_COMPILED_PLATFORM=Win64']+['/I'+str(p) for p in incs]
for source in [b/'minhook/src/buffer.c',b/'minhook/src/hook.c',b/'minhook/src/trampoline.c',b/'minhook/src/hde/hde64.c']:
 run(['cl.exe','/nologo','/c','/O2','/MD','/I'+str(b/'minhook/include'),source])
run(['cl.exe',*flags,'/LD',root/'native/dllmain.cpp','UE4SS.lib','buffer.obj','hook.obj','trampoline.obj','hde64.obj','/link','/OUT:main.dll'])
print('BUILT',out/'main.dll')
