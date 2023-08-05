# import Libraries of other lib packages
import numpy
import bob.core

# import our own Library
import bob.extension
bob.extension.load_bob_library('bob.io.base', __file__)

from ._library import File as _File_C, HDF5File as _HDF5File_C, extensions
from . import version
from .version import module as __version__
from .version import api as __api_version__

import os


class File(_File_C):
  __doc__ = _File_C.__doc__

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()


class HDF5File(_HDF5File_C):
  __doc__ = _HDF5File_C.__doc__

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    return self.close()

  def __contains__(self, x):
    __doc__ = self.has_key.__doc__
    return self.has_key(x)

  def __iter__(self):
    __doc__ = self.keys.__doc__
    return iter(self.keys())

  def __getitem__(self, name):
    __doc__ = self.get.__doc__
    return self.get(name)

  def __setitem__(self, name, value):
    __doc__ = self.set.__doc__
    return self.set(name, value)

  def values(self):
    '''Yields the datasets contained in the current directory.

    Yields
    -------
    object
        The datasets that are being read.
    '''
    return (self[key] for key in self)

  def items(self):
    '''Yields the keys and the datasets contained in the current directory.

    Yields
    -------
    tuple
        The key and the datasets that are being read in a tuple.
    '''
    return ((key, self[key]) for key in self)


def _is_string(s):
  """Returns ``True`` if the given object is a string

  This method can be used with Python-2.x or 3.x and returns a string
  respecting each environment's constraints.
  """

  from sys import version_info

  return (version_info[0] < 3 and isinstance(s, (str, unicode))) or \
      isinstance(s, (bytes, str))


@numpy.deprecate(new_name="os.makedirs(directory, exist_ok=True)")
def create_directories_safe(directory, dryrun=False):
  """Creates a directory if it does not exists, with concurrent access support.
  This function will also create any parent directories that might be required.
  If the dryrun option is selected, it does not actually create the directory,
  but just writes the (Linux) command that would have been executed.

  **Parameters:**

  ``directory`` : str
    The directory that you want to create.

  ``dryrun`` : bool
    Only ``print`` the command to console, but do not execute it.
  """
  if dryrun:
    print("[dry-run] mkdir -p '%s'" % directory)
  else:
    os.makedirs(directory, exist_ok=True)


def load(inputs):
  """load(inputs) -> data

  Loads the contents of a file, an iterable of files, or an iterable of
  :py:class:`bob.io.base.File`'s into a :py:class:`numpy.ndarray`.

  **Parameters:**

  ``inputs`` : various types

    This might represent several different entities:

    1. The name of a file (full path) from where to load the data. In this
       case, this assumes that the file contains an array and returns a loaded
       numpy ndarray.
    2. An iterable of filenames to be loaded in memory. In this case, this
       would assume that each file contains a single 1D sample or a set of 1D
       samples, load them in memory and concatenate them into a single and
       returned 2D :py:class:`numpy.ndarray`.
    3. An iterable of :py:class:`File`. In this case, this would assume
       that each :py:class:`File` contains a single 1D sample or a set
       of 1D samples, load them in memory if required and concatenate them into
       a single and returned 2D :py:class:`numpy.ndarray`.
    4. An iterable with mixed filenames and :py:class:`File`. In this
       case, this would returned a 2D :py:class:`numpy.ndarray`, as described
       by points 2 and 3 above.

  **Returns:**

  ``data`` : :py:class:`numpy.ndarray`
    The data loaded from the given ``inputs``.
  """

  from collections import Iterable
  import numpy
  if _is_string(inputs):
    return File(inputs, 'r').read()
  elif isinstance(inputs, Iterable):
    retval = []
    for obj in inputs:
      if _is_string(obj):
        retval.append(load(obj))
      elif isinstance(obj, File):
        retval.append(obj.read())
      else:
        raise TypeError(
            "Iterable contains an object which is not a filename nor a "
            "bob.io.base.File.")
    return numpy.vstack(retval)
  else:
    raise TypeError(
        "Unexpected input object. This function is expecting a filename, "
        "or an iterable of filenames and/or bob.io.base.File's")


def merge(filenames):
  """merge(filenames) -> files

  Converts an iterable of filenames into an iterable over read-only
  :py:class:`bob.io.base.File`'s.

  **Parameters:**

  ``filenames`` : str or [str]

    A list of file names.
    This might represent:

    1. A single filename. In this case, an iterable with a single
       :py:class:`File` is returned.
    2. An iterable of filenames to be converted into an iterable of
       :py:class:`File`'s.

  **Returns:**

  ``files`` : [:py:class:`File`]
    The list of files.
  """

  from collections import Iterable
  from .utils import is_string
  if is_string(filenames):
    return [File(filenames, 'r')]
  elif isinstance(filenames, Iterable):
    return [File(k, 'r') for k in filenames]
  else:
    raise TypeError(
        "Unexpected input object. This function is expecting an "
        "iterable of filenames.")


def save(array, filename, create_directories=False):
  """Saves the contents of an array-like object to file.

  Effectively, this is the same as creating a :py:class:`File` object
  with the mode flag set to ``'w'`` (write with truncation) and calling
  :py:meth:`File.write` passing ``array`` as parameter.

  Parameters:

  ``array`` : array_like
    The array-like object to be saved on the file

  ``filename`` : str
    The name of the file where you need the contents saved to

  ``create_directories`` : bool
    Automatically generate the directories if required (defaults to ``False``
    because of compatibility reasons; might change in future to default to
    ``True``)
  """
  # create directory if not existent yet
  if create_directories:
    create_directories_safe(os.path.dirname(filename))

  # requires data is c-contiguous and aligned, will create a copy otherwise
  array = numpy.require(array, requirements=('C_CONTIGUOUS', 'ALIGNED'))

  return File(filename, 'w').write(array)

# Just to make it homogenous with the C++ API
write = save
read = load


def append(array, filename):
  """append(array, filename) -> position

  Appends the contents of an array-like object to file.

  Effectively, this is the same as creating a :py:class:`File` object
  with the mode flag set to ``'a'`` (append) and calling
  :py:meth:`File.append` passing ``array`` as parameter.

  **Parameters:**

  ``array`` : array_like
    The array-like object to be saved on the file

  ``filename`` : str
    The name of the file where you need the contents saved to

  **Returns:**

  ``position`` : int
    See :py:meth:`File.append`
  """

  # requires data is c-contiguous and aligned, will create a copy otherwise
  array = numpy.require(array, requirements=('C_CONTIGUOUS', 'ALIGNED'))

  return File(filename, 'a').append(array)


def peek(filename):
  """peek(filename) -> dtype, shape, stride

  Returns the type of array (frame or sample) saved in the given file.

  Effectively, this is the same as creating a :py:class:`File` object
  with the mode flag set to `r` (read-only) and calling
  :py:meth:`File.describe`.

  **Parameters**:

  ``filename`` : str
    The name of the file to peek information from

  **Returns:**

  ``dtype, shape, stride`` : see :py:meth:`File.describe`
  """
  return File(filename, 'r').describe()


def peek_all(filename):
  """peek_all(filename) -> dtype, shape, stride

  Returns the type of array (for full readouts) saved in the given file.

  Effectively, this is the same as creating a :py:class:`File` object
  with the mode flag set to ``'r'`` (read-only) and returning
  ``File.describe`` with its parameter ``all`` set to ``True``.

  **Parameters:**

  ``filename`` : str
    The name of the file to peek information from

  **Returns:**

  ``dtype, shape, stride`` : see :py:meth:`File.describe`
  """
  return File(filename, 'r').describe(all=True)


# Keeps compatibility with the previously existing API
open = File


def get_config():
  """Returns a string containing the configuration information.
  """
  return bob.extension.get_config(__name__, version.externals, version.api)


def get_include_directories():
  """get_include_directories() -> includes

  Returns a list of include directories for dependent libraries, such as HDF5.
  This function is automatically used by
  :py:func:`bob.extension.get_bob_libraries` to retrieve the non-standard
  include directories that are required to use the C bindings of this library
  in dependent classes. You shouldn't normally need to call this function by
  hand.

  **Returns:**

  ``includes`` : [str]
    The list of non-standard include directories required to use the C bindings
    of this class. For now, only the directory for the HDF5 headers are
    returned.
  """
  # try to use pkg_config first
  try:
    from bob.extension.utils import find_header
    # locate pkg-config on our own
    header = 'hdf5.h'
    candidates = find_header(header)
    if not candidates:
      raise RuntimeError(
          "could not find %s's `%s' - have you installed %s on this "
          "machine?" % ('hdf5', header, 'hdf5'))

    return [os.path.dirname(candidates[0])]
  except RuntimeError:
    from bob.extension import pkgconfig
    pkg = pkgconfig('hdf5')
    return pkg.include_directories()


def get_macros():
  """get_macros() -> macros

  Returns a list of preprocessor macros, such as ``(HAVE_HDF5, 1)``. This
  function is automatically used by :py:func:`bob.extension.get_bob_libraries`
  to retrieve the prerpocessor definitions that are required to use the C
  bindings of this library in dependent classes. You shouldn't normally need to
  call this function by hand.

  **Returns:**

  ``macros`` : [(str,str)]
    The list of preprocessor macros required to use the C bindings of this
    class. For now, only ``('HAVE_HDF5', '1')`` is returned, when applicable.
  """
  # get include directories
  if get_include_directories():
    return [('HAVE_HDF5', '1')]


def _generate_features(reader, paths, same_size=False):
  """Load and stack features in a memory efficient way. This function is meant
  to be used inside :py:func:`vstack_features`.

  Parameters
  ----------
  reader : ``collections.Callable``
    See the documentation of :py:func:`vstack_features`.
  paths : ``collections.Iterable``
    See the documentation of :py:func:`vstack_features`.
  same_size : :obj:`bool`, optional
    See the documentation of :py:func:`vstack_features`.

  Yields
  ------
  object
    The first object returned is a tuple of :py:class:`numpy.dtype` of
    features and the shape of the first feature. The rest of objects are
    the actual values in features. The features are returned in C order.
  """

  shape_determined = False
  for i, path in enumerate(paths):

    feature = numpy.atleast_2d(reader(path))
    feature = numpy.ascontiguousarray(feature)
    if not shape_determined:
      shape_determined = True
      dtype = feature.dtype
      shape = list(feature.shape)
      yield (dtype, shape)
    else:
      # make sure all features have the same shape and dtype
      if same_size:
        assert shape == list(feature.shape)
      else:
        assert shape[1:] == list(feature.shape[1:])
      assert dtype == feature.dtype

    for value in feature.flat:
      yield value


def vstack_features(reader, paths, same_size=False):
  """Stacks all features in a memory efficient way.

  Parameters
  ----------
  reader : ``collections.Callable``
    The function to load the features. The function should only take one
    argument ``path`` and return loaded features. Use :any:`functools.partial`
    to accommodate your reader to this format.
    The features returned by ``reader`` are expected to have the same
    :py:class:`numpy.dtype` and the same shape except for their first
    dimension. First dimension should correspond to the number of samples.
  paths : ``collections.Iterable``
    An iterable of paths to iterate on. Whatever is inside path is given to
    ``reader`` so they do not need to be necessarily paths to actual files.
    If ``same_size`` is ``True``, ``len(paths)`` must be valid.
  same_size : :obj:`bool`, optional
    If ``True``, it assumes that arrays inside all the paths are the same
    shape. If you know the features are the same size in all paths, set this
    to ``True`` to improve the performance.

  Returns
  -------
  numpy.ndarray
    The read features with the shape ``(n_samples, *features_shape[1:])``.

  Examples
  --------
  This function in a simple way is equivalent to calling
  ``numpy.vstack(reader(p) for p in paths)``.

  >>> import numpy
  >>> from bob.io.base import vstack_features
  >>> def reader(path):
  ...     # in each file, there are 5 samples and features are 2 dimensional.
  ...     return numpy.arange(10).reshape(5,2)
  >>> paths = ['path1', 'path2']
  >>> all_features = vstack_features(reader, paths)
  >>> numpy.allclose(all_features, numpy.array(
  ...     [[0, 1],
  ...      [2, 3],
  ...      [4, 5],
  ...      [6, 7],
  ...      [8, 9],
  ...      [0, 1],
  ...      [2, 3],
  ...      [4, 5],
  ...      [6, 7],
  ...      [8, 9]]))
  True
  >>> all_features_with_more_memory = numpy.vstack(reader(p) for p in paths)
  >>> numpy.allclose(all_features, all_features_with_more_memory)
  True

  You can allocate the array at once to improve the performance if you know
  that all features in paths have the same shape and you know the total number
  of the paths:

  >>> all_features = vstack_features(reader, paths, same_size=True)
  >>> numpy.allclose(all_features, numpy.array(
  ...     [[0, 1],
  ...      [2, 3],
  ...      [4, 5],
  ...      [6, 7],
  ...      [8, 9],
  ...      [0, 1],
  ...      [2, 3],
  ...      [4, 5],
  ...      [6, 7],
  ...      [8, 9]]))
  True

  .. note::

    This function runs very slowly. Only use it when RAM is precious.
  """
  iterable = _generate_features(reader, paths, same_size)
  dtype, shape = next(iterable)
  if same_size:
    total_size = int(len(paths) * numpy.prod(shape))
    all_features = numpy.fromiter(iterable, dtype, total_size)
  else:
    all_features = numpy.fromiter(iterable, dtype)

  # the shape is assumed to be (n_samples, ...) it can be (5, 2) or (5, 3, 4).
  shape = list(shape)
  shape[0] = -1
  return numpy.reshape(all_features, shape, order="C")


# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]
