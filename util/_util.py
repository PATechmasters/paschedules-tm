#!/usr/bin/python

def compose(f, g):
    def func(*args, **kwargs):
        return f(g(*args, **kwargs))
    return func
