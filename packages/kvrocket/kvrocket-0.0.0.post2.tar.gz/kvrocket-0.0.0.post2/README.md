# kvrocket

`KVRocket` is a lightweight persistent key value store for Python.

## Primary Design Purpose

The primary reason this utility library was designed was for use within the ApexAPI framework. The framework uses KVRocket as its default persistent layer for it's own internal configuration.

This allows duplicating identical api's very quickly, by simply re-using a portable data layer that contains your pre-existing config.

## It's just a KV Store

At the end of the day, it is a single file, kv store built on Python objects. It can be used for anything really. But I needed something for a specific purpose, so I built this and it works suprisingly well for my particular use case.