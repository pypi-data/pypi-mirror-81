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
//

/**
 * \headerfile "timemory/components/user_bundle/overloads.hpp"
 * Defines the user_bundle component which can be used to inject components
 * at runtime. There are very useful for dynamically assembling collections
 * of tools at runtime
 *
 */

#pragma once

#if defined(TIMEMORY_USER_BUNDLE_SOURCE)
#    define TIMEMORY_USER_BUNDLE_LINKAGE(...) __VA_ARGS__
#elif !defined(TIMEMORY_USE_USER_BUNDLE_EXTERN)
#    define TIMEMORY_USER_BUNDLE_LINKAGE(...) inline __VA_ARGS__
#else
#    define TIMEMORY_USER_BUNDLE_LINKAGE(...) __VA_ARGS__
#endif
