# ! /usr/bin/env bash
import os
import pickle
from pydantic.utils import deep_update
# from functools import reduce
# import operator


class Picklebase:
    def __init__(self, path: str) -> None:
        """ Initializes the picklebase.

        Args:
            path (str): The path to the pickle file.
        """
        self.path = path
        self.cache = self.load()

    def __call__(self, path: str = '/'):
        if path == '/':
            return self.cache
        return self.obtain(self.cache, self.make_keys(path))

    @staticmethod
    def make_dict(keys: list, value: dict) -> dict:
        """ Creates a dict from a list of keys and a value.

        Args:
            keys (list): The list of keys.
            value (dict): The value to set.

        Returns:
            dict: The dict created from the keys and value.
        """
        result = {}
        reference = result
        for key in keys[:-1]:
            reference = reference.setdefault(key, {})
        reference[keys[-1]] = value
        return result

    @staticmethod
    def make_keys(path: str) -> list:
        """ Splits the path into a list of keys.

        Args:
            path (str): The path to split.

        Returns:
            list: The list of keys.
        """
        keys = path.split('/')
        if keys[-1] == '':
            del keys[-1]
        return keys

    @staticmethod
    def obtain(ref: dict, keys: list) -> dict:
        """ Traverses the dict to get the data at the specified path.

        Args:
            ref (dict): The dict to traverse.
            keys (list): The list of keys to traverse.

        Returns:
            dict: The data at the specified path.
        """
        try:
            for key in keys:
                ref = ref[key]
            return ref
        except KeyError:
            return {}
        
    def read(self, path: str = '/') -> dict:
        """ Reads the data at the specified path.

        Args:
            path (str): The path to the data.

        Returns:
            dict: The data at the specified path.
        """
        if path == '/':
            return self.cache
        return self.obtain(self.cache, self.make_keys(path))

    def delete(self, path: str, sync: bool = True) -> None:
        """ Deletes the data at the specified path.

        Args:
            path (str): The path to the data.
            sync (bool, optional): Whether to sync the cache. Defaults to True.
        """
        # NOTE: alternative method (requires functools and operator)
        # *path, key = make_keys(path) 
        # try:
        #     del reduce(operator.getitem, path, ref)[key]
        # except KeyError:
        #     pass
        # except TypeError:
        #     pass
        # return ref
        references = self.cache
        ref = references
        keys = self.make_keys(path)
        try:
            for key in keys[:-1]:
                ref = ref[key]
            if isinstance(ref, dict):
                del ref[keys[-1]]
        except KeyError:
            pass
        if sync:
            self.save()

    def update(self, path: str, data: dict, sync: bool = True) -> None:
        """ Updates the data at the specified path.

        Args:
            path (str): The path to the data.
            data (dict): The data to update.
            sync (bool): Whether to sync the cache. Defaults to True.
        """

        self.cache = deep_update(
            self.cache,
            self.make_dict(self.make_keys(path.strip()), data) if path != '/' else data
        )
        if sync:
            self.save()

    def load(self) -> None:
        """ Loads the pickle file. """
        if os.path.exists(self.path.strip()):
            with open(self.path, 'rb') as file:
                return pickle.load(file)
        return {}

    def save(self) -> None:
        """ Saves the pickle file. """
        if self.path[0] == '/':
            self.path = self.path[1:]
        paths = os.path.split(self.path.strip())
        if not os.path.exists(paths[0]):
            os.makedirs(paths[0])
        with open(self.path.strip(), 'wb') as file:
            pickle.dump(self.cache, file)