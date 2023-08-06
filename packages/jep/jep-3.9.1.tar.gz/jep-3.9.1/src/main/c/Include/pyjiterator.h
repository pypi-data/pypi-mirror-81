/*
   jep - Java Embedded Python

   Copyright (c) 2015-2019 JEP AUTHORS.

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
 * A PyJIteratorObject is a PyJObject that has tp_iter and tp_iternext
 * implemented to support iteration. It exists primarily to support PyJIterableObject.
 */

#include "jep_platform.h"
#include "pyjobject.h"

#ifndef _Included_pyjiterator
#define _Included_pyjiterator

extern PyTypeObject PyJIterator_Type;

#define PyJIterator_Wrap(env, jobj, jcls) \
    PyJObject_New(env, &PyJIterator_Type, jobj, jcls)

#define PyJIterator_Check(pyobj) \
    PyObject_TypeCheck(pyobj, &PyJIterator_Type)


#endif // ndef pyjiterator
