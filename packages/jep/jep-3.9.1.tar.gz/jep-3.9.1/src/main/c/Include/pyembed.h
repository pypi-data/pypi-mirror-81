/*
   jep - Java Embedded Python

   Copyright (c) 2004-2019 JEP AUTHORS.

   This file is licensed under the the zlib/libpng License.

   This software is provided 'as-is', without any express or implied
   warranty. In no event will the authors be held liable for any
   damages arising from the use of this software.

   Permission is granted to anyone to use this software for any
   purpose, including commercial applications, and to alter it and
   redistribute it freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you
   must not claim that you wrote the original software. If you use
   this software in a product, an acknowledgment in the product
   documentation would be appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and
   must not be misrepresented as being the original software.

   3. This notice may not be removed or altered from any source
   distribution.
*/

#include "jep_platform.h"

#ifndef _Included_pyembed
#define _Included_pyembed


#define DICT_KEY "jep"

struct __JepThread {
    PyObject      *modjep;
    PyObject      *globals;
    PyThreadState *tstate;
    JNIEnv        *env;
    jobject        classloader;
    jobject        caller;      /* Jep instance that called us. */
    PyObject      *fqnToPyJAttrs; /* a dictionary of fully qualified Java
                                       classnames to PyJMethods and PyJFields */
#if PY_MAJOR_VERSION < 3
    PyObject      *originalBuiltins;
#endif
};
typedef struct __JepThread JepThread;


void pyembed_preinit(JNIEnv*, jint, jint, jint, jint, jint, jint, jint,
                     jstring);
void pyembed_startup(JNIEnv*, jobjectArray);
void pyembed_shutdown(JavaVM*);
void pyembed_shared_import(JNIEnv*, jstring);

intptr_t pyembed_thread_init(JNIEnv*, jobject, jobject, jboolean, jboolean);
void pyembed_thread_close(JNIEnv*, intptr_t);

void pyembed_close(void);
void pyembed_run(JNIEnv*, intptr_t, char*);
jobject pyembed_invoke_method(JNIEnv*, intptr_t, const char*, jobjectArray,
                              jobject);
jobject pyembed_invoke_method_as(JNIEnv*, intptr_t, const char*, jobjectArray,
                                 jobject, jclass);
jobject pyembed_invoke(JNIEnv*, PyObject*, jobjectArray, jobject);
jobject pyembed_invoke_as(JNIEnv*, PyObject*, jobjectArray, jobject, jclass);
void pyembed_eval(JNIEnv*, intptr_t, char*);
int pyembed_compile_string(JNIEnv*, intptr_t, char*);
void pyembed_exec(JNIEnv*, intptr_t, char*);
void pyembed_setloader(JNIEnv*, intptr_t, jobject);
jobject pyembed_getvalue(JNIEnv*, intptr_t, char*, jclass);
jobject pyembed_getvalue_array(JNIEnv*, intptr_t, char*);
jobject pyembed_getvalue_on(JNIEnv*, intptr_t, intptr_t, char*);

JNIEnv* pyembed_get_env(void);
JepThread* pyembed_get_jepthread(void);

// -------------------------------------------------- set() methods

void pyembed_setparameter_object(JNIEnv*, intptr_t, intptr_t, const char*,
                                 jobject);
void pyembed_setparameter_array(JNIEnv *, intptr_t, intptr_t, const char *,
                                jobjectArray);
void pyembed_setparameter_class(JNIEnv *, intptr_t, intptr_t, const char*,
                                jclass);
void pyembed_setparameter_string(JNIEnv*, intptr_t, intptr_t, const char*,
                                 const char*);
void pyembed_setparameter_bool(JNIEnv*, intptr_t, intptr_t, const char*,
                               jboolean);
void pyembed_setparameter_int(JNIEnv*, intptr_t, intptr_t, const char*, int);
void pyembed_setparameter_long(JNIEnv*, intptr_t, intptr_t, const char*,
                               PY_LONG_LONG);
void pyembed_setparameter_double(JNIEnv*, intptr_t, intptr_t, const char*,
                                 double);
void pyembed_setparameter_float(JNIEnv*, intptr_t, intptr_t, const char*,
                                float);

#endif
