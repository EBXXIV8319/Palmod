#pragma once
#include <MinHook.h>
#include <cstdint>
namespace StorageHook {
class x64Detour {
    void* target; void* replacement; uint64_t* trampoline; bool created=false;
public:
    x64Detour(uint64_t t,uint64_t r,uint64_t* p):target((void*)t),replacement((void*)r),trampoline(p){}
    bool hook() {
        auto s=MH_Initialize();
        if(s!=MH_OK && s!=MH_ERROR_ALREADY_INITIALIZED) return false;
        s=MH_CreateHook(target,replacement,(void**)trampoline);
        if(s!=MH_OK) return false;
        created=true;
        if(MH_EnableHook(target)==MH_OK) return true;
        MH_RemoveHook(target);created=false;return false;
    }
    void unHook(){if(created){MH_DisableHook(target);MH_RemoveHook(target);created=false;}}
    ~x64Detour(){unHook();}
};
}
