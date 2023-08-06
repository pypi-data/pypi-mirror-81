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

#ifndef _Included_java_util_Map
#define _Included_java_util_Map

jboolean java_util_Map_containsKey(JNIEnv*, jobject, jobject);
jobject  java_util_Map_get(JNIEnv*, jobject, jobject);
jobject  java_util_Map_keySet(JNIEnv*, jobject);
jobject  java_util_Map_put(JNIEnv*, jobject, jobject, jobject);
jobject  java_util_Map_remove(JNIEnv*, jobject, jobject);
jint     java_util_Map_size(JNIEnv*, jobject);
jobject  java_util_Map_entrySet(JNIEnv*, jobject);

#endif // ndef java_util_Map
