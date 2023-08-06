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

/*
 * A PyJNumberObject is a PyJObject with some extra methods attached to meet
 * the Python Number protocol/interface.  It should only be used where the
 * underlying jobject of the PyJObject is an implementation of java.lang.Number.
 */

#include "jep_platform.h"
#include "pyjobject.h"

#ifndef _Included_pyjnumber
#define _Included_pyjnumber

extern PyTypeObject PyJNumber_Type;

#define PyJNumber_Wrap(env, jobj, jcls) \
    PyJObject_New(env, &PyJNumber_Type, jobj, jcls)

#define PyJNumber_Check(pyobj) \
    PyObject_TypeCheck(pyobj, &PyJNumber_Type)


#endif // ndef pyjnumber
