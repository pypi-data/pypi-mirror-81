.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_nested_parallel_memory.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_nested_parallel_memory.py:


==================================================
Checkpoint using joblib.Memory and joblib.Parallel
==================================================

This example illustrates how to cache intermediate computing results using
:class:`joblib.Memory` within :class:`joblib.Parallel`.

Embed caching within parallel processing
##############################################################################

 It is possible to cache a computationally expensive function executed during
 a parallel process. ``costly_compute`` emulates such time consuming function.


.. code-block:: default


    import time


    def costly_compute(data, column):
        """Emulate a costly function by sleeping and returning a column."""
        time.sleep(2)
        return data[column]


    def data_processing_mean(data, column):
        """Compute the mean of a column."""
        return costly_compute(data, column).mean()









Create some data. The random seed is fixed to generate deterministic data
across Python session. Note that this is not necessary for this specific
example since the memory cache is cleared at the end of the session.


.. code-block:: default


    import numpy as np
    rng = np.random.RandomState(42)
    data = rng.randn(int(1e4), 4)








It is first possible to make the processing without caching or parallel
processing.


.. code-block:: default


    start = time.time()
    results = [data_processing_mean(data, col) for col in range(data.shape[1])]
    stop = time.time()

    print('\nSequential processing')
    print('Elapsed time for the entire processing: {:.2f} s'
          .format(stop - start))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Sequential processing
    Elapsed time for the entire processing: 8.01 s




``costly_compute`` is expensive to compute and it is used as an intermediate
step in ``data_processing_mean``. Therefore, it is interesting to store the
intermediate results from ``costly_compute`` using :class:`joblib.Memory`.


.. code-block:: default


    from joblib import Memory

    location = './cachedir'
    memory = Memory(location, verbose=0)
    costly_compute_cached = memory.cache(costly_compute)









Now, we define ``data_processing_mean_using_cache`` which benefits from the
cache by calling ``costly_compute_cached``


.. code-block:: default


    def data_processing_mean_using_cache(data, column):
        """Compute the mean of a column."""
        return costly_compute_cached(data, column).mean()









Then, we execute the same processing in parallel and caching the intermediate
results.


.. code-block:: default


    from joblib import Parallel, delayed

    start = time.time()
    results = Parallel(n_jobs=2)(
        delayed(data_processing_mean_using_cache)(data, col)
        for col in range(data.shape[1]))
    stop = time.time()

    print('\nFirst round - caching the data')
    print('Elapsed time for the entire processing: {:.2f} s'
          .format(stop - start))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    First round - caching the data
    Elapsed time for the entire processing: 4.10 s




By using 2 workers, the parallel processing gives a x2 speed-up compared to
the sequential case. By executing again the same process, the intermediate
results obtained by calling ``costly_compute_cached`` will be loaded from the
cache instead of executing the function.


.. code-block:: default


    start = time.time()
    results = Parallel(n_jobs=2)(
        delayed(data_processing_mean_using_cache)(data, col)
        for col in range(data.shape[1]))
    stop = time.time()

    print('\nSecond round - reloading from the cache')
    print('Elapsed time for the entire processing: {:.2f} s'
          .format(stop - start))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Second round - reloading from the cache
    Elapsed time for the entire processing: 0.03 s




Reuse intermediate checkpoints
##############################################################################

 Having cached the intermediate results of the ``costly_compute_cached``
 function, they are reusable by calling the function. We define a new
 processing which will take the maximum of the array returned by
 ``costly_compute_cached`` instead of previously the mean.


.. code-block:: default



    def data_processing_max_using_cache(data, column):
        """Compute the max of a column."""
        return costly_compute_cached(data, column).max()


    start = time.time()
    results = Parallel(n_jobs=2)(
        delayed(data_processing_max_using_cache)(data, col)
        for col in range(data.shape[1]))
    stop = time.time()

    print('\nReusing intermediate checkpoints')
    print('Elapsed time for the entire processing: {:.2f} s'
          .format(stop - start))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Reusing intermediate checkpoints
    Elapsed time for the entire processing: 0.01 s




The processing time only corresponds to the execution of the ``max``
function. The internal call to ``costly_compute_cached`` is reloading the
results from the cache.

Clean-up the cache folder
##############################################################################


.. code-block:: default


    memory.clear(warn=False)








.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  12.168 seconds)


.. _sphx_glr_download_auto_examples_nested_parallel_memory.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: nested_parallel_memory.py <nested_parallel_memory.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: nested_parallel_memory.ipynb <nested_parallel_memory.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
