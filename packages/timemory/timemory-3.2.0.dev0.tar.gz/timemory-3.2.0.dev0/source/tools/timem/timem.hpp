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

#define TIMEM_DEBUG
#define TIMEMORY_DISABLE_BANNER
#define TIMEMORY_DISABLE_COMPONENT_STORAGE_INIT

#include "timemory/macros.hpp"
#include "timemory/mpl/types.hpp"
#include "timemory/utility/macros.hpp"

#if defined(_MACOS)
TIMEMORY_FORWARD_DECLARE_COMPONENT(page_rss)
TIMEMORY_DEFINE_CONCRETE_TRAIT(is_available, component::page_rss, false_type)
#endif

#include "timemory/components/timing/child.hpp"
#include "timemory/sampling/sampler.hpp"
#include "timemory/timemory.hpp"

TIMEMORY_DEFINE_CONCRETE_TRAIT(custom_label_printing, component::papi_array_t, true_type)

// C includes
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>

#if defined(TIMEMORY_USE_LIBEXPLAIN)
#    include <libexplain/execvp.h>
#endif

#if defined(_UNIX)
#    include <unistd.h>
extern "C"
{
    extern char** environ;
}
#endif

// C++ includes
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <thread>
#include <vector>

template <typename Tp>
using vector_t       = std::vector<Tp>;
using string_t       = std::string;
using stringstream_t = std::stringstream;

using namespace tim::component;

//--------------------------------------------------------------------------------------//
// create a custom component tuple printer
//
namespace tim
{
//
//--------------------------------------------------------------------------------------//
//
//                              OPERATION SPECIALIZATION
//
//--------------------------------------------------------------------------------------//
//
namespace operation
{
struct set_print_rank
{};
//
template <typename Tp>
struct print_properties
{
    print_properties(const Tp&, set_print_rank, int32_t _rank) { rank() = _rank; }
    static int32_t& rank()
    {
        static int32_t _v = -1;
        return _v;
    }
};
//
template <typename Tp>
struct custom_print
{
    using value_type = typename Tp::value_type;
    using base_type  = component::base<Tp, value_type>;

    custom_print(std::size_t N, std::size_t /*_Ntot*/, base_type& obj, std::ostream& os)
    {
        if(!tim::trait::runtime_enabled<Tp>::get())
            return;

        stringstream_t ss;
        if(N == 0)
            ss << std::endl;
        ss << "    ";
        if(print_properties<Tp>::rank() > -1)
            ss << print_properties<Tp>::rank() << "|> ";
        ss << obj << std::endl;
        os << ss.str();
    }
};
//
template <typename Tp, bool SampleV = (tim::trait::sampler<Tp>::value ||
                                       tim::trait::file_sampler<Tp>::value)>
struct timem_sample;
//
template <typename Tp>
struct timem_sample<Tp, true>
{
    template <typename... Args>
    explicit timem_sample(Tp& obj, Args&&... args);

    template <typename Up, typename... Args>
    auto sfinae(Up& obj, int, Args&&... args)
        -> decltype(obj.measure(std::forward<Args>(args)...), void())
    {
        obj.measure(std::forward<Args>(args)...);
    }

    template <typename Up, typename... Args>
    auto sfinae(Up& obj, int, Args&&...) -> decltype(obj.measure(), void())
    {
        obj.measure();
    }
};
//
template <typename Tp>
template <typename... Args>
timem_sample<Tp, true>::timem_sample(Tp& obj, Args&&... args)
{
    sfinae(obj, 0, std::forward<Args>(args)...);
}
//
template <typename Tp>
struct timem_sample<Tp, false>
{
    template <typename... Args>
    explicit timem_sample(Tp&, Args&&...)
    {}
};
//
/// this is a custom version of base_printer for {read,written}_{char,bytes} components
template <typename Tp>
struct custom_base_printer
{
    using type       = Tp;
    using value_type = typename type::value_type;
    using base_type  = typename type::base_type;

    template <typename Up                                        = value_type,
              enable_if_t<!(std::is_same<Up, void>::value), int> = 0>
    explicit custom_base_printer(std::ostream& _os, const type& _obj, int32_t _rank,
                                 const std::string& _label)
    {
        stringstream_t ss, ssv, ssr, ssrank;
        auto           _prec  = base_type::get_precision();
        auto           _width = base_type::get_width();
        auto           _flags = base_type::get_format_flags();
        auto           _disp  = _obj.get_display_unit();
        auto           _val   = _obj.get();

        ssv.setf(_flags);
        ssv << std::setw(_width) << std::setprecision(_prec) << std::get<0>(_val);
        if(!std::get<0>(_disp).empty())
            ssv << " " << std::get<0>(_disp);

        if(_rank > -1)
            ssrank << _rank << "|> ";

        ssr.setf(_flags);
        ssr << std::setw(_width) << std::setprecision(_prec) << std::get<1>(_val);
        if(!std::get<1>(_disp).empty())
            ssr << " " << std::get<1>(_disp);

        ss << ssv.str() << " " << _label << "\n    " << ssrank.str() << ssr.str() << " "
           << _label;
        _os << ss.str();
    }

    template <typename Up = value_type, typename... Args,
              enable_if_t<(std::is_same<Up, void>::value), int> = 0>
    explicit custom_base_printer(std::ostream&, const type&, Args&&...)
    {}
};
//
#define CUSTOM_BASE_PRINTER_SPECIALIZATION(TYPE, LABEL)                                  \
    template <>                                                                          \
    struct base_printer<TYPE> : custom_base_printer<TYPE>                                \
    {                                                                                    \
        using type = TYPE;                                                               \
        static int32_t& rank() { return print_properties<TYPE>::rank(); }                \
        explicit base_printer(std::ostream& _os, const type& _obj)                       \
        : custom_base_printer<type>(_os, _obj, rank(), LABEL)                            \
        {}                                                                               \
    };
//
CUSTOM_BASE_PRINTER_SPECIALIZATION(component::read_bytes, "bytes read")
CUSTOM_BASE_PRINTER_SPECIALIZATION(component::read_char, "char read")
CUSTOM_BASE_PRINTER_SPECIALIZATION(component::written_bytes, "bytes written")
CUSTOM_BASE_PRINTER_SPECIALIZATION(component::written_char, "char written")
//
#if defined(TIMEMORY_USE_PAPI)
//
template <>
struct sample<component::papi_array_t>
{
    using EmptyT                 = std::tuple<>;
    using type                   = papi_array_t;
    using value_type             = typename type::value_type;
    using base_type              = typename type::base_type;
    using this_type              = sample<type>;
    static constexpr bool enable = trait::sampler<type>::value;
    using data_type = conditional_t<enable, decltype(std::declval<type>().get()), EmptyT>;

    TIMEMORY_DEFAULT_OBJECT(sample)

    template <typename Up, typename... Args,
              enable_if_t<(std::is_same<Up, this_type>::value), int> = 0>
    explicit sample(base_type& obj, Up, Args&&...)
    {
        obj.value        = type::record();
        obj.is_transient = false;
    }
};
//
template <>
struct start<component::papi_array_t>
{
    using type       = papi_array_t;
    using value_type = typename type::value_type;
    using base_type  = typename type::base_type;

    template <typename... Args>
    explicit start(base_type&, Args&&...)
    {
        type::configure();
    }
};
//
template <>
struct stop<component::papi_array_t>
{
    using type       = papi_array_t;
    using value_type = typename type::value_type;
    using base_type  = typename type::base_type;

    template <typename... Args>
    explicit stop(base_type&, Args&&...)
    {}
};
//
#endif
//
}  // namespace operation
//
//--------------------------------------------------------------------------------------//
//
//                              COMPONENT SPECIALIZATION
//
//--------------------------------------------------------------------------------------//
//
namespace component
{
//
#if defined(TIMEMORY_USE_PAPI)
//
template <>
std::string
papi_array_t::get_display() const
{
    if(events.size() == 0)
        return "";
    auto val          = (is_transient) ? accum : value;
    auto _get_display = [&](std::ostream& os, size_type idx) {
        auto     _obj_value = val[idx];
        auto     _evt_type  = events[idx];
        string_t _label     = papi::get_event_info(_evt_type).short_descr;
        string_t _disp      = papi::get_event_info(_evt_type).units;
        auto     _prec      = base_type::get_precision();
        auto     _width     = base_type::get_width();
        auto     _flags     = base_type::get_format_flags();

        stringstream_t ss, ssv, ssi;
        ssv.setf(_flags);
        ssv << std::setw(_width) << std::setprecision(_prec) << _obj_value;
        if(!_disp.empty())
            ssv << " " << _disp;
        if(!_label.empty())
            ssi << " " << _label;
        if(idx > 0 && operation::print_properties<papi_array_t>::rank() > -1)
            ss << operation::print_properties<papi_array_t>::rank() << "|> ";
        ss << ssv.str() << ssi.str();
        if(idx > 0)
            os << "    ";
        os << ss.str();
    };

    stringstream_t ss;
    for(size_type i = 0; i < events.size(); ++i)
    {
        _get_display(ss, i);
        if(i + 1 < events.size())
            ss << '\n';
    }

    return ss.str();
}
//
#endif
//
}  // namespace component
//
//--------------------------------------------------------------------------------------//
//
//                         VARIADIC WRAPPER SPECIALIZATION
//
//--------------------------------------------------------------------------------------//
//
/// \class timem_tuple
/// \brief A specialized variadic component wrapper which inherits from the
/// lightweight_tuple which does not automatically push and pop to storage
///
template <typename... Types>
class timem_tuple : public lightweight_tuple<Types...>
{
public:
    using base_type = lightweight_tuple<Types...>;
    using apply_v   = typename base_type::apply_v;
    using data_type = typename base_type::impl_type;
    using this_type = timem_tuple<Types...>;

    template <template <typename> class Op, typename Tuple = data_type>
    using custom_operation_t =
        typename base_type::template custom_operation<Op, Tuple>::type;

    template <typename... T>
    struct opsample;

    template <template <typename...> class Tuple, typename... T>
    struct opsample<Tuple<T...>>
    {
        using type =
            Tuple<operation::timem_sample<T, (trait::sampler<T>::value ||
                                              trait::file_sampler<T>::value)>...>;
    };

    template <typename T>
    using opsample_t = typename opsample<T>::type;

    template <typename... T>
    struct mpi_getter;

    template <template <typename...> class Tuple, typename... T>
    struct mpi_getter<Tuple<T...>>
    {
        using value_type = Tuple<std::vector<T>...>;
    };

    template <typename T>
    using mpi_getter_v = typename mpi_getter<T>::value_type;

public:
    timem_tuple()
    : base_type()
    {}

    explicit timem_tuple(const string_t& key)
    : base_type(key)
    {}

    timem_tuple(const std::string& _key, data_type&& _data)
    : base_type(_key)
    {
        m_data = std::move(_data);
    }

    ~timem_tuple() {}

    void start() { base_type::start(); }
    void stop() { base_type::stop(); }
    void reset() { base_type::reset(); }
    auto get() { return base_type::get(); }
    auto get_labeled() { return base_type::get_labeled(); }
    void set_output(std::ofstream* ofs) { m_ofs = ofs; }

    template <typename... Args>
    void sample(Args&&... args)
    {
        base_type::sample(std::forward<Args>(args)...);
        apply<void>::access<opsample_t<data_type>>(this->m_data,
                                                   std::forward<Args>(args)...);
        if(m_ofs)
            (*m_ofs) << get_local_datetime("[===== %r %F =====]\n") << *this << std::endl;
    }

    auto mpi_get()
    {
        constexpr auto N      = std::tuple_size<data_type>::value;
        auto           v_data = mpi_getter_v<data_type>{};
        // merge the data
        mpi_get(v_data, m_data, make_index_sequence<N>{});
        // return an array of this_type
        return mpi_get(v_data, make_index_sequence<N>{});
    }

    friend std::ostream& operator<<(std::ostream& os, const timem_tuple<Types...>& obj)
    {
        stringstream_t ssp;
        stringstream_t ssd;
        auto&&         _data  = obj.m_data;
        auto&&         _key   = obj.key();
        auto&&         _width = obj.output_width();

        using print_t = custom_operation_t<operation::custom_print, data_type>;
        apply<void>::access_with_indices<print_t>(_data, std::ref(ssd));

        ssp << std::setw(_width) << std::left << _key;
        os << ssp.str() << ssd.str();

        if(&os != obj.m_ofs && obj.m_ofs)
            *(obj.m_ofs) << get_local_datetime("[===== %r %F =====]\n") << ssp.str()
                         << ssd.str() << std::endl;

        return os;
    }

    void set_rank(int32_t _rank)
    {
        apply<void>::access<custom_operation_t<operation::print_properties, data_type>>(
            this->m_data, operation::set_print_rank{}, _rank);
    }

    bool empty() const { return m_empty; }

private:
    // this mpi_get overload merges the results from the different mpi processes
    template <typename... Tp, size_t... Idx>
    auto mpi_get(std::tuple<std::vector<Tp>...>& _data, std::tuple<Tp...>& _inp,
                 std::index_sequence<Idx...>)
    {
        TIMEMORY_FOLD_EXPRESSION(
            operation::finalize::mpi_get<decay_t<std::tuple_element_t<Idx, data_type>>,
                                         true>(std::get<Idx>(_data),
                                               std::get<Idx>(_inp)));
    }

    // this mpi_get overload converts the merged data into the tuples which are
    // of the same data type as the timem_tuple m_data field
    template <size_t Idx, typename... Tp>
    auto mpi_get(std::vector<std::tuple<Tp...>>& _targ,
                 std::tuple<std::vector<Tp>...>& _data)
    {
        auto&& _entries = std::get<Idx>(_data);
        size_t n        = _entries.size();
        if(n > _targ.size())
            _targ.resize(n, std::tuple<Tp...>{});
        for(size_t i = 0; i < n; ++i)
            std::get<Idx>(_targ.at(i)) = std::move(_entries.at(i));
    }

    // this mpi_get overload converts the data tuples into timem_tuple instances
    template <typename... Tp, size_t... Idx>
    auto mpi_get(std::tuple<std::vector<Tp>...>& _data, std::index_sequence<Idx...>)
    {
        // convert the tuple of vectors into a vector of tuples
        std::vector<std::tuple<Tp...>> _vec;
        TIMEMORY_FOLD_EXPRESSION(mpi_get<Idx>(_vec, _data));
        // convert the vector of tuples into a vector of this_tupe
        std::vector<this_type> _ret;
        for(auto&& itr : _vec)
            _ret.emplace_back(this_type(this->key(), std::move(itr)));
        return _ret;
    }

private:
    using base_type::m_data;
    bool           m_empty = false;
    std::ofstream* m_ofs   = nullptr;
};
//
template <typename... Types>
using timem_tuple_t = convert_t<available_t<type_list<Types...>>, timem_tuple<>>;
//
}  // namespace tim
//
//--------------------------------------------------------------------------------------//
//
#if !defined(TIMEM_BUNDLE)
#    define TIMEM_BUNDLE                                                                 \
        tim::timem_tuple_t<wall_clock, child_user_clock, child_system_clock,             \
                           child_cpu_clock, child_cpu_util, peak_rss, page_rss,          \
                           virtual_memory, num_major_page_faults, num_minor_page_faults, \
                           priority_context_switch, voluntary_context_switch, read_char, \
                           read_bytes, written_char, written_bytes, user_mode_time,      \
                           kernel_mode_time, papi_array_t>
#endif
//
#if !defined(TIMEM_PID_SIGNAL)
#    define TIMEM_PID_SIGNAL SIGCONT
#endif
//
#if !defined(TIMEM_PID_SIGNAL_STRING)
#    define TIMEM_PID_SIGNAL_STRING TIMEMORY_STRINGIZE(TIMEM_PID_SIGNAL)
#endif
//
using timem_bundle_t  = TIMEM_BUNDLE;
using sampler_t       = tim::sampling::sampler<TIMEM_BUNDLE, 1>;
using sampler_array_t = typename sampler_t::array_type;
static_assert(std::is_same<sampler_array_t, std::array<timem_bundle_t, 1>>::value,
              "Error! Sampler array is not std::array<timem_bundle_t, 1>");
//
//--------------------------------------------------------------------------------------//
//
inline sampler_t*&
get_sampler()
{
    static sampler_t* _instance = nullptr;
    return _instance;
}
//
//--------------------------------------------------------------------------------------//
//
inline timem_bundle_t*
get_measure()
{
    return get_sampler()->get_last();
}
//
//--------------------------------------------------------------------------------------//
//
struct timem_config
{
    static constexpr bool papi_available = tim::trait::is_available<papi_array_t>::value;

    bool          use_shell        = tim::get_env("TIMEM_USE_SHELL", false);
    bool          use_mpi          = tim::get_env("TIMEM_USE_MPI", false);
    bool          use_papi         = tim::get_env("TIMEM_USE_PAPI", papi_available);
    bool          use_sample       = tim::get_env("TIMEM_SAMPLE", true);
    bool          signal_delivered = false;
    bool          debug            = tim::get_env("TIMEM_DEBUG", false);
    int           verbose          = tim::get_env("TIMEM_VERBOSE", 0);
    string_t      shell            = tim::get_env<string_t>("SHELL", getusershell());
    string_t      shell_flags  = tim::get_env<string_t>("TIMEM_USE_SHELL_FLAGS", "-i");
    string_t      output_file  = tim::get_env<string_t>("TIMEM_OUTPUT", "");
    double        sample_freq  = tim::get_env<double>("TIMEM_SAMPLE_FREQ", 1.0);
    double        sample_delay = tim::get_env<double>("TIMEM_SAMPLE_DELAY", 0.001);
    pid_t         master_pid   = getpid();
    pid_t         worker_pid   = getpid();
    string_t      command      = "";
    std::set<int> signal_types = { SIGALRM };
};
//
//--------------------------------------------------------------------------------------//
//
inline timem_config&
get_config()
{
    static timem_config _instance;
    return _instance;
}
//
//--------------------------------------------------------------------------------------//
//
#define TIMEM_CONFIG_FUNCTION(NAME)                                                      \
    inline auto& NAME() { return get_config().NAME; }
//
//--------------------------------------------------------------------------------------//
//
TIMEM_CONFIG_FUNCTION(use_shell)
TIMEM_CONFIG_FUNCTION(use_mpi)
TIMEM_CONFIG_FUNCTION(use_papi)
TIMEM_CONFIG_FUNCTION(use_sample)
TIMEM_CONFIG_FUNCTION(shell)
TIMEM_CONFIG_FUNCTION(shell_flags)
TIMEM_CONFIG_FUNCTION(output_file)
TIMEM_CONFIG_FUNCTION(sample_freq)
TIMEM_CONFIG_FUNCTION(sample_delay)
TIMEM_CONFIG_FUNCTION(signal_delivered)
TIMEM_CONFIG_FUNCTION(debug)
TIMEM_CONFIG_FUNCTION(verbose)
TIMEM_CONFIG_FUNCTION(command)
TIMEM_CONFIG_FUNCTION(master_pid)
TIMEM_CONFIG_FUNCTION(worker_pid)
TIMEM_CONFIG_FUNCTION(signal_types)
//
//--------------------------------------------------------------------------------------//
//
inline void
explain(int ret, const char* pathname, char** argv)
{
    if(ret < 0)
    {
#if defined(TIMEMORY_USE_LIBEXPLAIN)
        fprintf(stderr, "%s\n", explain_execvp(pathname, argv));
#else
        fprintf(stderr, "Return code: %i : %s\n", ret, pathname);
        int n = 0;
        std::cerr << "Command: ";
        while(argv[n] != nullptr)
            std::cerr << argv[n++] << " ";
        std::cerr << std::endl;
#endif
    }
    else if(debug() || verbose() > 0)
    {
        int n = 0;
        std::cerr << "Command: ";
        while(argv[n] != nullptr)
            std::cerr << argv[n++] << " ";
        std::cerr << std::endl;
    }
}
//
//--------------------------------------------------------------------------------------//
