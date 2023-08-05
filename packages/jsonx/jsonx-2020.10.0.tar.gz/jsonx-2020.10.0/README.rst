=====
JSONx
=====

This is a Python module implementing JSONx, an XML representation of the JSON
data model. The format is defined by IBM, and documentation is available on the
IBM website: `JSONx conversion rules
<http://pic.dhe.ibm.com/infocenter/wsdatap/v6r0m0/index.jsp?topic=%2Fcom.ibm.dp.xm.doc%2Fjson_jsonx.html>`_

Note: currently only writing support has been implemented; there's no parser
yet!

WHAT? WHY WOULD I NEED THIS?
============================

You probably don't want to use this. But, hey, remember, using XML makes your
product ready for the enterprise!


Installation
============

Install using ``pip``::

    pip install jsonx


Usage
=====

The interface mimics the familiar `json` module::

    import jsonx

    obj = {
        "name": "John Doe",
        "age": 12,
    }

    # To obtain a byte string, use dumps()
    value = jsonx.dumps(obj)

    # To write directly to a file-like object, use dump()
    with open("output.xml") as fp:
        jsonx.dump(obj, fp)
