.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_parallel_memmap.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_parallel_memmap.py:


===============================
NumPy memmap in joblib.Parallel
===============================

This example illustrates some features enabled by using a memory map
(:class:`numpy.memmap`) within :class:`joblib.Parallel`. First, we show that
dumping a huge data array ahead of passing it to :class:`joblib.Parallel`
speeds up computation. Then, we show the possibility to provide write access to
original data.

Speed up processing of a large data array
#############################################################################

 We create a large data array for which the average is computed for several
 slices.


.. code-block:: default


    import numpy as np

    data = np.random.random((int(1e7),))
    window_size = int(5e5)
    slices = [slice(start, start + window_size)
              for start in range(0, data.size - window_size, int(1e5))]








The ``slow_mean`` function introduces a :func:`time.sleep` call to simulate a
more expensive computation cost for which parallel computing is beneficial.
Parallel may not be beneficial for very fast operation, due to extra overhead
(workers creations, communication, etc.).


.. code-block:: default


    import time


    def slow_mean(data, sl):
        """Simulate a time consuming processing."""
        time.sleep(0.01)
        return data[sl].mean()









First, we will evaluate the sequential computing on our problem.


.. code-block:: default


    tic = time.time()
    results = [slow_mean(data, sl) for sl in slices]
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Elapsed time computing the average of couple of slices 1.09 s




:class:`joblib.Parallel` is used to compute in parallel the average of all
slices using 2 workers.


.. code-block:: default


    from joblib import Parallel, delayed


    tic = time.time()
    results = Parallel(n_jobs=2)(delayed(slow_mean)(data, sl) for sl in slices)
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Elapsed time computing the average of couple of slices 0.88 s




Parallel processing is already faster than the sequential processing. It is
also possible to remove a bit of overhead by dumping the ``data`` array to a
memmap and pass the memmap to :class:`joblib.Parallel`.


.. code-block:: default


    import os
    from joblib import dump, load

    folder = './joblib_memmap'
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    data_filename_memmap = os.path.join(folder, 'data_memmap')
    dump(data, data_filename_memmap)
    data = load(data_filename_memmap, mmap_mode='r')

    tic = time.time()
    results = Parallel(n_jobs=2)(delayed(slow_mean)(data, sl) for sl in slices)
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s\n'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Elapsed time computing the average of couple of slices 0.66 s





Therefore, dumping large ``data`` array ahead of calling
:class:`joblib.Parallel` can speed up the processing by removing some
overhead.

Writable memmap for shared memory :class:`joblib.Parallel`
##############################################################################

 ``slow_mean_write_output`` will compute the mean for some given slices as in
 the previous example. However, the resulting mean will be directly written on
 the output array.


.. code-block:: default



    def slow_mean_write_output(data, sl, output, idx):
        """Simulate a time consuming processing."""
        time.sleep(0.005)
        res_ = data[sl].mean()
        print("[Worker %d] Mean for slice %d is %f" % (os.getpid(), idx, res_))
        output[idx] = res_









Prepare the folder where the memmap will be dumped.


.. code-block:: default


    output_filename_memmap = os.path.join(folder, 'output_memmap')








Pre-allocate a writable shared memory map as a container for the results of
the parallel computation.


.. code-block:: default


    output = np.memmap(output_filename_memmap, dtype=data.dtype,
                       shape=len(slices), mode='w+')








``data`` is replaced by its memory mapped version. Note that the buffer has
already been dumped in the previous section.


.. code-block:: default


    data = load(data_filename_memmap, mmap_mode='r')








Fork the worker processes to perform computation concurrently


.. code-block:: default


    Parallel(n_jobs=2)(delayed(slow_mean_write_output)(data, sl, output, idx)
                       for idx, sl in enumerate(slices))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]



Compare the results from the output buffer with the expected results


.. code-block:: default


    print("\nExpected means computed in the parent process:\n {}"
          .format(np.array(results)))
    print("\nActual means computed by the worker processes:\n {}"
          .format(output))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Expected means computed in the parent process:
     [0.50075894 0.50068495 0.50064327 0.50044217 0.50038146 0.50019771
     0.49972935 0.49936545 0.49933908 0.499139   0.49912131 0.49956501
     0.49999776 0.49969998 0.49964402 0.49957265 0.49938828 0.49926568
     0.49939077 0.4996239  0.49996623 0.49983847 0.49953889 0.49971531
     0.49942849 0.49918081 0.49933006 0.49950281 0.49934353 0.49916575
     0.49951624 0.49965896 0.49955591 0.49944006 0.49958473 0.49937647
     0.49965629 0.49987511 0.49993857 0.50027265 0.50042428 0.50005855
     0.49992284 0.50027257 0.50031321 0.49999397 0.50015633 0.50049359
     0.50031371 0.49997376 0.50022598 0.50037709 0.50013133 0.50001533
     0.500182   0.50005378 0.49974391 0.49991468 0.50033042 0.50023438
     0.50047554 0.50060105 0.50065203 0.50058473 0.50072945 0.50062456
     0.50068697 0.50046269 0.50006888 0.50002303 0.49997364 0.49952566
     0.49938348 0.49947952 0.49965773 0.49981717 0.50003219 0.50040037
     0.50042859 0.50028228 0.49996501 0.50013959 0.49982921 0.49970856
     0.49938837 0.49950157 0.49966769 0.49990983 0.50009548 0.50008982
     0.50003805 0.49992255 0.50006548 0.49955756 0.49993132]

    Actual means computed by the worker processes:
     [0.50075894 0.50068495 0.50064327 0.50044217 0.50038146 0.50019771
     0.49972935 0.49936545 0.49933908 0.499139   0.49912131 0.49956501
     0.49999776 0.49969998 0.49964402 0.49957265 0.49938828 0.49926568
     0.49939077 0.4996239  0.49996623 0.49983847 0.49953889 0.49971531
     0.49942849 0.49918081 0.49933006 0.49950281 0.49934353 0.49916575
     0.49951624 0.49965896 0.49955591 0.49944006 0.49958473 0.49937647
     0.49965629 0.49987511 0.49993857 0.50027265 0.50042428 0.50005855
     0.49992284 0.50027257 0.50031321 0.49999397 0.50015633 0.50049359
     0.50031371 0.49997376 0.50022598 0.50037709 0.50013133 0.50001533
     0.500182   0.50005378 0.49974391 0.49991468 0.50033042 0.50023438
     0.50047554 0.50060105 0.50065203 0.50058473 0.50072945 0.50062456
     0.50068697 0.50046269 0.50006888 0.50002303 0.49997364 0.49952566
     0.49938348 0.49947952 0.49965773 0.49981717 0.50003219 0.50040037
     0.50042859 0.50028228 0.49996501 0.50013959 0.49982921 0.49970856
     0.49938837 0.49950157 0.49966769 0.49990983 0.50009548 0.50008982
     0.50003805 0.49992255 0.50006548 0.49955756 0.49993132]




Clean-up the memmap
##############################################################################

 Remove the different memmap that we created. It might fail in Windows due
 to file permissions.


.. code-block:: default


    import shutil

    try:
        shutil.rmtree(folder)
    except:  # noqa
        print('Could not clean-up automatically.')








.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  3.430 seconds)


.. _sphx_glr_download_auto_examples_parallel_memmap.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: parallel_memmap.py <parallel_memmap.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: parallel_memmap.ipynb <parallel_memmap.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
