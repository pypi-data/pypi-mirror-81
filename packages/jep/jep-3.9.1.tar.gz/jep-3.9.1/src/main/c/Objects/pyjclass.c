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

#include "Jep.h"


/*
 * Adds a single inner class as attributes to the pyjclass. This will check if
 * the inner class is public and will only add it if it is public. This is
 * intended to only be called from pyjclass_add_inner_classes().
 *
 * @param env the JNI environment
 * @param topClz the pyjobject of the top/outer Class
 * @param innerClz the jclass of the inner class
 *
 * @return NULL on errors, topClz if there are no errors
 */
static PyObject* pyjclass_add_inner_class(JNIEnv *env, PyJClassObject *topClz,
        jclass innerClz)
{
    jint      mods;
    jboolean  public;

    // setup to verify this inner class should be available
    mods = java_lang_Class_getModifiers(env, innerClz);
    if (process_java_exception(env)) {
        return NULL;
    }
    public = java_lang_reflect_Modifier_isPublic(env, mods);
    if (process_java_exception(env)) {
        return NULL;
    }

    if (public) {
        PyObject        *attrClz    = NULL;
        jstring          shortName  = NULL;
        const char      *charName   = NULL;

        attrClz = PyJClass_Wrap(env, innerClz);
        if (!attrClz) {
            return NULL;
        }
        shortName = java_lang_Class_getSimpleName(env, innerClz);
        if (process_java_exception(env) || !shortName) {
            return NULL;
        }
        charName = jstring2char(env, shortName);

        if (PyDict_SetItemString(topClz->attr, charName, attrClz) != 0) {
            printf("Error adding inner class %s\n", charName);
        } else {
            PyObject *pyname = PyString_FromString(charName);
            Py_DECREF(pyname);
        }
        Py_DECREF(attrClz); // parent class will hold the reference
        release_utf_char(env, shortName, charName);
    }
    return (PyObject*) topClz;
}


/*
 * Adds a Java class's public inner classes as attributes to the pyjclass.
 *
 * @param env the JNI environment
 * @param topClz the pyjobject of the top/outer Class
 *
 * @return topClz if successful, otherwise NULL
 */
static PyObject* pyjclass_add_inner_classes(JNIEnv *env,
        PyJClassObject *topClz)
{
    jobjectArray      innerArray    = NULL;
    jsize             innerSize     = 0;

    innerArray = java_lang_Class_getDeclaredClasses(env, topClz->clazz);
    if (process_java_exception(env) || !innerArray) {
        return NULL;
    }

    innerSize = (*env)->GetArrayLength(env, innerArray);
    if (innerSize > 0) {
        int i;

        if ((*env)->PushLocalFrame(env, JLOCAL_REFS) != 0) {
            (*env)->DeleteLocalRef(env, innerArray);
            process_java_exception(env);
            return NULL;
        }

        // check each inner class to see if it's public
        for (i = 0; i < innerSize; i++) {
            jclass innerClz = (*env)->GetObjectArrayElement(env, innerArray, i);
            if (process_java_exception(env) || !innerClz) {
                (*env)->PopLocalFrame(env, NULL);
                (*env)->DeleteLocalRef(env, innerArray);
                return NULL;
            }
            if (pyjclass_add_inner_class(env, topClz, innerClz) == NULL) {
                (*env)->PopLocalFrame(env, NULL);
                (*env)->DeleteLocalRef(env, innerArray);
                return NULL;
            }
            (*env)->DeleteLocalRef(env, innerClz);
        }
        (*env)->PopLocalFrame(env, NULL);
    }
    (*env)->DeleteLocalRef(env, innerArray);

    return (PyObject*) topClz;
}


static int pyjclass_init(JNIEnv *env, PyObject *pyjob)
{
    ((PyJClassObject*) pyjob)->constructor = NULL;

    /*
     * attempt to add public inner classes as attributes since lots of people
     * code with public enum.  Note this will not allow the inner class to be
     * imported separately, it must be accessed through the enclosing class.
     */
    if (!pyjclass_add_inner_classes(env, (PyJClassObject*) pyjob)) {
        /*
         * let's just print the error to stderr and continue on without
         * inner class support, it's not the end of the world
         */
        if (PyErr_Occurred()) {
            PyErr_PrintEx(0);
        }
    }

    return 1;
}

PyObject* PyJClass_Wrap(JNIEnv *env, jobject obj)
{
    PyObject* pyjob = PyJObject_New(env, &PyJClass_Type, NULL, obj);
    if (pyjob) {
        if (!pyjclass_init(env, pyjob)) {
            Py_DecRef(pyjob);
            pyjob = NULL;
        }
    }
    return pyjob;
}

static void pyjclass_dealloc(PyJClassObject *self)
{
#if USE_DEALLOC
    Py_CLEAR(self->constructor);
    PyJClass_Type.tp_base->tp_dealloc((PyObject*) self);
#endif
}

/*
 * Initialize the constructors field of a pyjclass.
 *
 * @return 1 on successful initialization, -1 on error.
 */
static int pyjclass_init_constructors(PyJClassObject *pyc)
{
    JNIEnv       *env         = NULL;
    jobjectArray  initArray   = NULL;
    int           initLen     = 0;
    PyObject     *pycallable  = NULL;
    int           i           = 0;

    env = pyembed_get_env();
    if ((*env)->PushLocalFrame(env, JLOCAL_REFS) != 0) {
        process_java_exception(env);
        return -1;
    }

    initArray = java_lang_Class_getConstructors(env, pyc->clazz);
    if (process_java_exception(env) || !initArray) {
        goto EXIT_ERROR;
    }

    initLen   = (*env)->GetArrayLength(env, initArray);

    for (i = 0; i < initLen; i++) {
        PyObject *pyjinit     = NULL;
        jobject   constructor = NULL;

        constructor = (*env)->GetObjectArrayElement(env, initArray, i);
        if (process_java_exception(env) || !constructor) {
            goto EXIT_ERROR;
        }
        pyjinit = PyJConstructor_New(env, constructor);
        if (pyjinit == NULL) {
            goto EXIT_ERROR;
        }
        (*env)->DeleteLocalRef(env, constructor);

        if (i == 0) {
            pycallable = pyjinit;
        } else if (i == 1) {
            PyObject* firstInit = pycallable;
            pycallable = PyJMultiMethod_New(firstInit, pyjinit);
            Py_DECREF(firstInit);
            Py_DECREF(pyjinit);
            if (pycallable == NULL) {
                goto EXIT_ERROR;
            }
        } else {
            if (PyJMultiMethod_Append(pycallable, pyjinit) == -1) {
                Py_DECREF(pyjinit);
                goto EXIT_ERROR;
            }
            Py_DECREF(pyjinit);
        }
    }
    (*env)->DeleteLocalRef(env, initArray);

    if (pycallable) {
        pyc->constructor = pycallable;
    }

    (*env)->PopLocalFrame(env, NULL);
    return 1;

EXIT_ERROR:
    (*env)->PopLocalFrame(env, NULL);
    Py_CLEAR(pycallable);
    return -1;
}

// call constructor as a method and return pyjobject.
static PyObject* pyjclass_call(PyJClassObject *self,
                               PyObject *args,
                               PyObject *keywords)
{
    PyObject *boundConstructor = NULL;
    PyObject *result           = NULL;
    if (self->constructor == NULL) {
        if (pyjclass_init_constructors(self) == -1) {
            return NULL;
        }
        if (self->constructor == NULL) {
            PyErr_Format(PyExc_TypeError, "No public constructor");
            return NULL;
        }
    }
    /*
     * Bind the constructor to the class so that the class will
     * be the first arg when constructor is called.
     */
#if PY_MAJOR_VERSION >= 3
    boundConstructor = PyMethod_New(self->constructor, (PyObject*) self);
#else
    boundConstructor = PyMethod_New(self->constructor, (PyObject*) self,
                                    (PyObject*) Py_TYPE((PyObject*)self));
#endif
    result = PyObject_Call(boundConstructor, args, keywords);
    Py_DECREF(boundConstructor);
    return result;
}


PyTypeObject PyJClass_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "jep.PyJClass",
    sizeof(PyJClassObject),
    0,
    (destructor) pyjclass_dealloc,            /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_compare */
    0,                                        /* tp_repr */
    0,                                        /* tp_as_number */
    0,                                        /* tp_as_sequence */
    0,                                        /* tp_as_mapping */
    0,                                        /* tp_hash  */
    (ternaryfunc) pyjclass_call,              /* tp_call */
    0,                                        /* tp_str */
    0,                                        /* tp_getattro */
    0,                                        /* tp_setattro */
    0,                                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                       /* tp_flags */
    "jclass",                                 /* tp_doc */
    0,                                        /* tp_traverse */
    0,                                        /* tp_clear */
    0,                                        /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    0,                                        /* tp_iter */
    0,                                        /* tp_iternext */
    0,                                        /* tp_methods */
    0,                                        /* tp_members */
    0,                                        /* tp_getset */
    0, // &PyJObject_Type                     /* tp_base */
    0,                                        /* tp_dict */
    0,                                        /* tp_descr_get */
    0,                                        /* tp_descr_set */
    0,                                        /* tp_dictoffset */
    0,                                        /* tp_init */
    0,                                        /* tp_alloc */
    NULL,                                     /* tp_new */
};
