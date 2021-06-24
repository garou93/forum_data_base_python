#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 21:38:45 2021

@author: haihem
"""
# forum , propriétes, méthodes de classe, base de données
import abc
import datetime

class Database:
    data = []

    def insert(self, obj):
        self.data.append(obj)

    def select(self, cls, **kwargs):
        items = (item for item in self.data
                 if isinstance(item, cls)
                 and all(hasattr(item, k) and getattr(item, k) == v
                         for (k, v) in kwargs.items()))
        try:
            return next(items)
        except StopIteration:
            raise ValueError('item not found')

class Model(abc.ABC):
    db = Database()
    @abc.abstractmethod
    def __init__(self):
        self.db.insert(self)
    @classmethod
    def get(cls, **kwargs):
        return cls.db.select(cls, **kwargs)
    @property
    def id(self):
        return id(self)

class User(Model):
    def __init__(self, name):
        super().__init__()
        self.name = name

class Post(Model):
    def __init__(self, author, message):
        super().__init__()
        self.author = author
        self.message = message
        self.date = datetime.datetime.now()

    def format(self):
        date = self.date.strftime('le %d/%m/%Y à %H:%M:%S')
        return '<div><span>Par {} {}</span><p>{}</p></div>'.format(self.author.name, date, self.message)

if __name__ == '__main__':
    user1 = User('user1')
    user2 = User('user2')
    Post(user1, 'salut')
    Post(user2, 'coucou')

    print(Post.get(author=User.get(name='user2')).format())
    print(Post.get(author=User.get(id=user1.id)).format())