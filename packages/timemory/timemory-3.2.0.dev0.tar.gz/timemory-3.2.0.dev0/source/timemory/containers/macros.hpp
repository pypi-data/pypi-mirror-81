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

/**
 * \file timemory/containers/macros.hpp
 * \brief Include the macros for containers
 */

#pragma once

#include "timemory/dll.hpp"

//======================================================================================//
//
//                              Define macros for containers
//
//======================================================================================//
//
#if defined(TIMEMORY_USE_EXTERN) && !defined(TIMEMORY_USE_CONTAINERS_EXTERN)
#    define TIMEMORY_USE_CONTAINERS_EXTERN
#endif
//
#if defined(TIMEMORY_CONTAINERS_SOURCE)
#    define TIMEMORY_CONTAINERS_LINKAGE(...) __VA_ARGS__
#elif defined(TIMEMORY_USE_CONTAINERS_EXTERN)
#    define TIMEMORY_CONTAINERS_LINKAGE(...) extern __VA_ARGS__
#else
#    define TIMEMORY_CONTAINERS_LINKAGE(...) inline __VA_ARGS__
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_EXTERN_NAME_COMBINE)
#    define TIMEMORY_EXTERN_NAME_COMBINE(X, Y) X##Y
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_EXTERN_TUPLE_ALIAS)
#    define TIMEMORY_EXTERN_TUPLE_ALIAS(Y) TIMEMORY_EXTERN_NAME_COMBINE(extern_tuple_, Y)
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_EXTERN_LIST_ALIAS)
#    define TIMEMORY_EXTERN_LIST_ALIAS(Y) TIMEMORY_EXTERN_NAME_COMBINE(extern_list_, Y)
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_EXTERN_HYBRID_ALIAS)
#    define TIMEMORY_EXTERN_HYBRID_ALIAS(Y)                                              \
        TIMEMORY_EXTERN_NAME_COMBINE(extern_hybrid_, Y)
#endif
//
//--------------------------------------------------------------------------------------//
//
//      extern declaration
//
#if !defined(TIMEMORY_DECLARE_EXTERN_TUPLE)
#    define TIMEMORY_DECLARE_EXTERN_TUPLE(_ALIAS, ...)                                   \
        namespace tim                                                                    \
        {                                                                                \
        extern template class component_tuple<__VA_ARGS__>;                              \
        extern template class auto_tuple<__VA_ARGS__>;                                   \
        using TIMEMORY_EXTERN_TUPLE_ALIAS(_ALIAS) = auto_tuple<__VA_ARGS__>;             \
        }
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_DECLARE_EXTERN_LIST)
#    define TIMEMORY_DECLARE_EXTERN_LIST(_ALIAS, ...)                                    \
        namespace tim                                                                    \
        {                                                                                \
        extern template class component_list<__VA_ARGS__>;                               \
        extern template class auto_list<__VA_ARGS__>;                                    \
        using TIMEMORY_EXTERN_LIST_ALIAS(_ALIAS) = auto_list<__VA_ARGS__>;               \
        }
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_DECLARE_EXTERN_HYBRID)
#    define TIMEMORY_DECLARE_EXTERN_HYBRID(_ALIAS)                                       \
        namespace tim                                                                    \
        {                                                                                \
        extern template class component_hybrid<TIMEMORY_EXTERN_TUPLE_ALIAS(_ALIAS),      \
                                               TIMEMORY_EXTERN_LIST_ALIAS(_ALIAS)>;      \
        extern template class auto_hybrid<TIMEMORY_EXTERN_TUPLE_ALIAS(_ALIAS),           \
                                          TIMEMORY_EXTERN_LIST_ALIAS(_ALIAS)>;           \
        using TIMEMORY_EXTERN_HYBRID_ALIAS(_ALIAS) = auto_hybrid<                        \
            TIMEMORY_EXTERN_TUPLE_ALIAS(_ALIAS), TIMEMORY_EXTERN_LIST_ALIAS(_ALIAS)>;    \
        }
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_DECLARE_EXTERN_BUNDLE)
#    define TIMEMORY_DECLARE_EXTERN_BUNDLE(API, ...)                                     \
        namespace tim                                                                    \
        {                                                                                \
        extern template class component_bundle<API, __VA_ARGS__>;                        \
        extern template class auto_bundle<API, __VA_ARGS__>;                             \
        }
#endif
//
//--------------------------------------------------------------------------------------//
//
//      extern instantiation
//
#if !defined(TIMEMORY_INSTANTIATE_EXTERN_TUPLE)
#    define TIMEMORY_INSTANTIATE_EXTERN_TUPLE(_ALIAS, ...)                               \
        namespace tim                                                                    \
        {                                                                                \
        template class component_tuple<__VA_ARGS__>;                                     \
        template class auto_tuple<__VA_ARGS__>;                                          \
        using TIMEMORY_EXTERN_TUPLE_ALIAS(_ALIAS) = auto_tuple<__VA_ARGS__>;             \
        }
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_INSTANTIATE_EXTERN_LIST)
#    define TIMEMORY_INSTANTIATE_EXTERN_LIST(_ALIAS, ...)                                \
        namespace tim                                                                    \
        {                                                                                \
        template class component_list<__VA_ARGS__>;                                      \
        template class auto_list<__VA_ARGS__>;                                           \
        using TIMEMORY_EXTERN_LIST_ALIAS(_ALIAS) = auto_list<__VA_ARGS__>;               \
        }
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_INSTANTIATE_EXTERN_HYBRID)
#    define TIMEMORY_INSTANTIATE_EXTERN_HYBRID(_ALIAS)                                   \
        namespace tim                                                                    \
        {                                                                                \
        template class component_hybrid<TIMEMORY_EXTERN_TUPLE_ALIAS(_ALIAS),             \
                                        TIMEMORY_EXTERN_LIST_ALIAS(_ALIAS)>;             \
        template class auto_hybrid<TIMEMORY_EXTERN_TUPLE_ALIAS(_ALIAS),                  \
                                   TIMEMORY_EXTERN_LIST_ALIAS(_ALIAS)>;                  \
        using TIMEMORY_EXTERN_HYBRID_ALIAS(_ALIAS) = auto_hybrid<                        \
            TIMEMORY_EXTERN_TUPLE_ALIAS(_ALIAS), TIMEMORY_EXTERN_LIST_ALIAS(_ALIAS)>;    \
        }
#endif
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_INSTANTIATE_EXTERN_BUNDLE)
#    define TIMEMORY_INSTANTIATE_EXTERN_BUNDLE(API, ...)                                 \
        namespace tim                                                                    \
        {                                                                                \
        template class component_bundle<API, __VA_ARGS__>;                               \
        template class auto_bundle<API, __VA_ARGS__>;                                    \
        }
#endif
//
//--------------------------------------------------------------------------------------//
//
//                      generic for build
//
//--------------------------------------------------------------------------------------//
//
#if defined(TIMEMORY_CONTAINERS_SOURCE)
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_TUPLE)
#        define TIMEMORY_EXTERN_TUPLE(_ALIAS, ...)                                       \
            TIMEMORY_INSTANTIATE_EXTERN_TUPLE(_ALIAS, __VA_ARGS__)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_LIST)
#        define TIMEMORY_EXTERN_LIST(_ALIAS, ...)                                        \
            TIMEMORY_INSTANTIATE_EXTERN_LIST(_ALIAS, __VA_ARGS__)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_HYBRID)
#        define TIMEMORY_EXTERN_HYBRID(_ALIAS) TIMEMORY_INSTANTIATE_EXTERN_HYBRID(_ALIAS)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_BUNDLE)
#        define TIMEMORY_EXTERN_BUNDLE(...)                                              \
            TIMEMORY_INSTANTIATE_EXTERN_BUNDLE(__VA_ARGS__)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#elif defined(TIMEMORY_USE_CONTAINERS_EXTERN)
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_TUPLE)
#        define TIMEMORY_EXTERN_TUPLE(_ALIAS, ...)                                       \
            TIMEMORY_DECLARE_EXTERN_TUPLE(_ALIAS, __VA_ARGS__)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_LIST)
#        define TIMEMORY_EXTERN_LIST(_ALIAS, ...)                                        \
            TIMEMORY_DECLARE_EXTERN_LIST(_ALIAS, __VA_ARGS__)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_HYBRID)
#        define TIMEMORY_EXTERN_HYBRID(_ALIAS) TIMEMORY_DECLARE_EXTERN_HYBRID(_ALIAS)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_BUNDLE)
#        define TIMEMORY_EXTERN_BUNDLE(...) TIMEMORY_DECLARE_EXTERN_BUNDLE(__VA_ARGS__)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#else
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_TUPLE)
#        define TIMEMORY_EXTERN_TUPLE(...)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_LIST)
#        define TIMEMORY_EXTERN_LIST(...)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_HYBRID)
#        define TIMEMORY_EXTERN_HYBRID(...)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#    if !defined(TIMEMORY_EXTERN_BUNDLE)
#        define TIMEMORY_EXTERN_BUNDLE(...)
#    endif
//
//--------------------------------------------------------------------------------------//
//
#endif
//
//--------------------------------------------------------------------------------------//
//
//                          AUTO_BUNDLE macros
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_BLANK_AUTO_BUNDLE)
#    define TIMEMORY_BLANK_AUTO_BUNDLE(...)                                              \
        TIMEMORY_BLANK_POINTER(::tim::auto_bundle, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_BASIC_AUTO_BUNDLE)
#    define TIMEMORY_BASIC_AUTO_BUNDLE(...)                                              \
        TIMEMORY_BASIC_POINTER(::tim::auto_bundle, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_AUTO_BUNDLE)
#    define TIMEMORY_AUTO_BUNDLE(...) TIMEMORY_POINTER(::tim::auto_bundle, __VA_ARGS__)
#endif
//
//--------------------------------------------------------------------------------------//
// instance versions
//
#if !defined(TIMEMORY_BLANK_AUTO_BUNDLE_HANDLE)
#    define TIMEMORY_BLANK_AUTO_BUNDLE_HANDLE(...)                                       \
        TIMEMORY_BLANK_HANDLE(::tim::auto_bundle, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_BASIC_AUTO_BUNDLE_HANDLE)
#    define TIMEMORY_BASIC_AUTO_BUNDLE_HANDLE(...)                                       \
        TIMEMORY_BASIC_HANDLE(::tim::auto_bundle, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_AUTO_BUNDLE_HANDLE)
#    define TIMEMORY_AUTO_BUNDLE_HANDLE(...)                                             \
        TIMEMORY_HANDLE(::tim::auto_bundle, __VA_ARGS__)
#endif
//
//--------------------------------------------------------------------------------------//
// debug versions
//
#if !defined(TIMEMORY_DEBUG_BASIC_AUTO_BUNDLE)
#    define TIMEMORY_DEBUG_BASIC_AUTO_BUNDLE(...)                                        \
        TIMEMORY_DEBUG_BASIC_MARKER(::tim::auto_bundle, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_DEBUG_AUTO_BUNDLE)
#    define TIMEMORY_DEBUG_AUTO_BUNDLE(...)                                              \
        TIMEMORY_DEBUG_MARKER(::tim::auto_bundle, __VA_ARGS__)
#endif
//
//--------------------------------------------------------------------------------------//
//
//                          AUTO_TIMER macros
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEMORY_BLANK_AUTO_TIMER)
#    define TIMEMORY_BLANK_AUTO_TIMER(...)                                               \
        TIMEMORY_BLANK_POINTER(::tim::auto_timer, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_BASIC_AUTO_TIMER)
#    define TIMEMORY_BASIC_AUTO_TIMER(...)                                               \
        TIMEMORY_BASIC_POINTER(::tim::auto_timer, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_AUTO_TIMER)
#    define TIMEMORY_AUTO_TIMER(...) TIMEMORY_POINTER(::tim::auto_timer, __VA_ARGS__)
#endif
//
//--------------------------------------------------------------------------------------//
// instance versions
//
#if !defined(TIMEMORY_BLANK_AUTO_TIMER_HANDLE)
#    define TIMEMORY_BLANK_AUTO_TIMER_HANDLE(...)                                        \
        TIMEMORY_BLANK_HANDLE(::tim::auto_timer, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_BASIC_AUTO_TIMER_HANDLE)
#    define TIMEMORY_BASIC_AUTO_TIMER_HANDLE(...)                                        \
        TIMEMORY_BASIC_HANDLE(::tim::auto_timer, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_AUTO_TIMER_HANDLE)
#    define TIMEMORY_AUTO_TIMER_HANDLE(...)                                              \
        TIMEMORY_HANDLE(::tim::auto_timer, __VA_ARGS__)
#endif
//
//--------------------------------------------------------------------------------------//
// debug versions
//
#if !defined(TIMEMORY_DEBUG_BASIC_AUTO_TIMER)
#    define TIMEMORY_DEBUG_BASIC_AUTO_TIMER(...)                                         \
        TIMEMORY_DEBUG_BASIC_MARKER(::tim::auto_timer, __VA_ARGS__)
#endif
//
#if !defined(TIMEMORY_DEBUG_AUTO_TIMER)
#    define TIMEMORY_DEBUG_AUTO_TIMER(...)                                               \
        TIMEMORY_DEBUG_MARKER(::tim::auto_timer, __VA_ARGS__)
#endif
//
//--------------------------------------------------------------------------------------//
