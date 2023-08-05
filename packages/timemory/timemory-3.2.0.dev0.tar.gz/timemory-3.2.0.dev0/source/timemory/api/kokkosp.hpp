// MIT License
//
// Copyright (c) 2020, The Regents of the University of California,
// through Lawrence Berkeley National Laboratory (subject to receipt of any
// required approvals from the U.S. Dept. of Energy).  All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#pragma once

#include "timemory/timemory.hpp"

#include <cstdint>

#if defined(TIMEMORY_SOURCE)
#    define TIMEMORY_KOKKOSP_PREFIX TIMEMORY_WEAK_PREFIX
#    define TIMEMORY_KOKKOSP_POSTFIX TIMEMORY_WEAK_POSTFIX TIMEMORY_VISIBILITY("default")
#else
#    define TIMEMORY_KOKKOSP_PREFIX
#    define TIMEMORY_KOKKOSP_POSTFIX TIMEMORY_VISIBILITY("default")
#endif

TIMEMORY_DECLARE_API(kokkosp)
TIMEMORY_DEFINE_API(kokkosp)

struct SpaceHandle
{
    char name[64];
};

struct KokkosPDeviceInfo
{
    uint32_t deviceID;
};

//--------------------------------------------------------------------------------------//

namespace tim
{
namespace kokkosp
{
//--------------------------------------------------------------------------------------//

enum Space
{
    SPACE_HOST,
    SPACE_CUDA
};

//--------------------------------------------------------------------------------------//

enum
{
    NSPACES = 2
};

//--------------------------------------------------------------------------------------//

inline Space
get_space(SpaceHandle const& handle)
{
    switch(handle.name[0])
    {
        case 'H': return SPACE_HOST;
        case 'C': return SPACE_CUDA;
    }
    abort();
    return SPACE_HOST;
}

//--------------------------------------------------------------------------------------//

inline const char*
get_space_name(int space)
{
    switch(space)
    {
        case SPACE_HOST: return "HOST";
        case SPACE_CUDA: return "CUDA";
    }
    abort();
    return nullptr;
}

//--------------------------------------------------------------------------------------//

inline uint64_t
get_unique_id()
{
    static thread_local uint64_t _instance = 0;
    return _instance++;
}

//--------------------------------------------------------------------------------------//

inline std::mutex&
get_cleanup_mutex()
{
    static std::mutex _instance;
    return _instance;
}

//--------------------------------------------------------------------------------------//

inline auto&
get_cleanup()
{
    static std::vector<std::function<void()>> _instance{};
    return _instance;
}

//--------------------------------------------------------------------------------------//

template <typename Tp>
inline Tp&
get_tl_static()
{
    // create a thread-local instance
    static thread_local Tp _instance;
    // on first pass, add to cleanup
    static thread_local bool _init = [&]() {
        get_cleanup_mutex().lock();
        get_cleanup().push_back([&]() { _instance.clear(); });
        get_cleanup_mutex().unlock();
        return true;
    }();
    consume_parameters(_init);

    return _instance;
}

//--------------------------------------------------------------------------------------//

template <typename Tp>
inline Tp&
get_static()
{
    // create a thread-local instance
    static Tp _instance;
    // on first pass, add to cleanup
    static bool _init = [&]() {
        get_cleanup_mutex().lock();
        get_cleanup().push_back([&]() { _instance.clear(); });
        get_cleanup_mutex().unlock();
    }();
    consume_parameters(_init);

    return _instance;
}

//--------------------------------------------------------------------------------------//

inline void
cleanup()
{
    get_cleanup_mutex().lock();
    for(auto& itr : get_cleanup())
        itr();
    get_cleanup_mutex().unlock();
}

//--------------------------------------------------------------------------------------//

using memory_tracker = component::data_tracker<int64_t, api::kokkosp>;
using kokkos_bundle  = component::user_bundle<0, api::kokkosp>;

template <typename... Tail>
using profiler_t = tim::component_bundle_t<api::kokkosp, memory_tracker, Tail...>;

template <typename... Tail>
using profiler_section_t = std::tuple<std::string, profiler_t<Tail...>>;

// various data structurs used
template <typename... Tail>
using profiler_stack_t = std::vector<profiler_t<Tail...>>;

template <typename... Tail>
using profiler_memory_map_t = std::map<const void* const, profiler_t<Tail...>>;

template <typename... Tail>
using profiler_index_map_t = std::unordered_map<uint64_t, profiler_t<Tail...>>;

template <typename... Tail>
using profiler_section_map_t = std::unordered_map<uint64_t, profiler_section_t<Tail...>>;

//--------------------------------------------------------------------------------------//

template <typename... Tail>
inline profiler_index_map_t<Tail...>&
get_profiler_index_map()
{
    return get_tl_static<profiler_index_map_t<Tail...>>();
}

//--------------------------------------------------------------------------------------//

template <typename... Tail>
inline profiler_section_map_t<Tail...>&
get_profiler_section_map()
{
    return get_tl_static<profiler_section_map_t<Tail...>>();
}

//--------------------------------------------------------------------------------------//

template <typename... Tail>
inline profiler_memory_map_t<Tail...>&
get_profiler_memory_map()
{
    return get_tl_static<profiler_memory_map_t<Tail...>>();
}

//--------------------------------------------------------------------------------------//

template <typename... Tail>
inline profiler_stack_t<Tail...>&
get_profiler_stack()
{
    return get_tl_static<profiler_stack_t<Tail...>>();
}

//--------------------------------------------------------------------------------------//

template <typename... Tail>
inline void
create_profiler(const std::string& pname, uint64_t kernid)
{
    get_profiler_index_map<Tail...>().insert({ kernid, profiler_t<Tail...>(pname) });
}

//--------------------------------------------------------------------------------------//

template <typename... Tail>
inline void
destroy_profiler(uint64_t kernid)
{
    if(get_profiler_index_map<Tail...>().find(kernid) !=
       get_profiler_index_map<Tail...>().end())
        get_profiler_index_map<Tail...>().erase(kernid);
}

//--------------------------------------------------------------------------------------//

template <typename... Tail>
inline void
start_profiler(uint64_t kernid)
{
    if(get_profiler_index_map<Tail...>().find(kernid) !=
       get_profiler_index_map<Tail...>().end())
        get_profiler_index_map<Tail...>().at(kernid).start();
}

//--------------------------------------------------------------------------------------//

template <typename... Tail>
inline void
stop_profiler(uint64_t kernid)
{
    if(get_profiler_index_map<Tail...>().find(kernid) !=
       get_profiler_index_map<Tail...>().end())
        get_profiler_index_map<Tail...>().at(kernid).stop();
}

//--------------------------------------------------------------------------------------//

}  // namespace kokkosp
}  // namespace tim

//--------------------------------------------------------------------------------------//

TIMEMORY_DEFINE_CONCRETE_TRAIT(uses_memory_units, kokkosp::memory_tracker, std::true_type)
TIMEMORY_DEFINE_CONCRETE_TRAIT(is_memory_category, kokkosp::memory_tracker,
                               std::true_type)

//--------------------------------------------------------------------------------------//

extern "C"
{
    TIMEMORY_KOKKOSP_PREFIX void kokkosp_init_library(
        const int loadSeq, const uint64_t interfaceVer, const uint32_t devInfoCount,
        void* deviceInfo) TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_finalize_library() TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_begin_parallel_for(
        const char* name, uint32_t devid, uint64_t* kernid) TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_end_parallel_for(uint64_t kernid)
        TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_begin_parallel_reduce(
        const char* name, uint32_t devid, uint64_t* kernid) TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_end_parallel_reduce(uint64_t kernid)
        TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_begin_parallel_scan(
        const char* name, uint32_t devid, uint64_t* kernid) TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_end_parallel_scan(uint64_t kernid)
        TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_push_profile_region(const char* name)
        TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_pop_profile_region() TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_create_profile_section(
        const char* name, uint32_t* secid) TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_destroy_profile_section(uint32_t secid)
        TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_start_profile_section(uint32_t secid)
        TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_stop_profile_section(uint32_t secid)
        TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_allocate_data(
        const SpaceHandle space, const char* label, const void* const ptr,
        const uint64_t size) TIMEMORY_KOKKOSP_POSTFIX;
    TIMEMORY_KOKKOSP_PREFIX void kokkosp_deallocate_data(
        const SpaceHandle space, const char* label, const void* const ptr,
        const uint64_t size) TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_begin_deep_copy(
        SpaceHandle dst_handle, const char* dst_name, const void* dst_ptr,
        SpaceHandle src_handle, const char* src_name, const void* src_ptr,
        uint64_t size) TIMEMORY_KOKKOSP_POSTFIX;

    TIMEMORY_KOKKOSP_PREFIX void kokkosp_end_deep_copy() TIMEMORY_KOKKOSP_POSTFIX;
}
