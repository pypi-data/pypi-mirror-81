/*
   jep - Java Embedded Python

   Copyright (c) 2016-2019 JEP AUTHORS.

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

#include "Jep.h"

static jmethodID init     = 0;
static jmethodID getBytes = 0;

jstring java_lang_String_new_BArray_String(JNIEnv* env, jbyteArray bytes,
        jstring charsetName)
{
    jstring result = NULL;
    Py_BEGIN_ALLOW_THREADS
    if (JNI_METHOD(init, env, JSTRING_TYPE, "<init>",
                   "([BLjava/lang/String;)V")) {
        result = (*env)->NewObject(env, JSTRING_TYPE, init, bytes, charsetName);
    }
    Py_END_ALLOW_THREADS
    return result;
}

jbyteArray java_lang_String_getBytes(JNIEnv* env, jobject this,
                                     jstring charsetName)
{
    jbyteArray result = NULL;
    Py_BEGIN_ALLOW_THREADS
    if (JNI_METHOD(getBytes, env, JSTRING_TYPE, "getBytes",
                   "(Ljava/lang/String;)[B")) {
        result = (jbyteArray) (*env)->CallObjectMethod(env, this, getBytes,
                 charsetName);
    }
    Py_END_ALLOW_THREADS
    return result;
}
