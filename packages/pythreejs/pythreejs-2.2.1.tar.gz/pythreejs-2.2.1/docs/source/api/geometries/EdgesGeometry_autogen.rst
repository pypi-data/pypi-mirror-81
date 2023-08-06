
.. py:currentmodule:: pythreejs

EdgesGeometry
====================================================

.. Use autoclass to fill any memebers not manually specified.
   This ensures it picks up any members in overridden classes.

.. autohastraits:: EdgesGeometry(geometry=None, thresholdAngle=1, )
    :members:
    :undoc-members:


    Inherits :py:class:`~pythreejs.BaseBufferGeometry`.

    Three.js docs: https://threejs.org/docs/#api/geometries/EdgesGeometry


    .. py:attribute:: geometry


        .. sourcecode:: python

            Union([
                Instance(BaseGeometry, allow_none=True),
                Instance(BaseBufferGeometry, allow_none=True)
            ]).tag(sync=True, **widget_serialization)

    .. py:attribute:: thresholdAngle


        .. sourcecode:: python

            CFloat(1, allow_none=False).tag(sync=True)

    .. py:attribute:: type


        .. sourcecode:: python

            Unicode("EdgesGeometry", allow_none=False).tag(sync=True)

