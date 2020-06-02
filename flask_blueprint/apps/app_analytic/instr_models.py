
"""
class A:
    def __init__(cls, *args, **kwargs):
        print('A init', args)

    def __new__(cls, *args, **kwargs):
        print(cls, object)
        print("args is", args)
        print("kwargs is", kwargs)
        # wo this no init
        #cls = super(A, cls).__new__(cls, *args, **kwargs)
        cls = super().__new__(cls)
        return cls

class C(A):
    def __init__(self, *args, **kwargs):
        print('C init',args, kwargs)

c = C()

"""

"""
class Singleton_meta(type):
    #instance=None
    def __init__(cls, name, bases, dict):
        #super(Singleton_meta, cls).__init__(name, bases, dict)
        super().__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls,*args,**kw):
        if not cls.instance:
            #cls.instance = super(Singleton_meta, cls).__call__(*args, **kw)
            cls.instance = super().__call__(*args, **kw)
        return cls.instance

class Instr(metaclass = Singleton_meta):
    #__metaclass__ = Singleton_meta
    #def __init__(self, id):
    #    super().__init__(id)

es = Instr(4)
es
us = Instr(9)
us
id(es) == id(us)
"""

"""
class Singleton:
  _instances = {}
  def __new__(cls, *args, **kwargs):
    if cls not in cls._instances:
        cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        #cls._instances[cls] = super().__new__(cls, *args, **kwargs)
    return cls._instances[cls]

class Multiton:
  _instances = {}

  #def __init__(self, *args, **kwargs):
  #    super().__init__(self, *args, **kwargs)

  def __new__(cls, *args, **kwargs):
  #def __new__(cls, id):
      if args[0] not in cls._instances:
          #cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
          #cls._instances[id] = super().__new__(cls, *id)
          #cls._instances[args[0]] = super(Multiton, cls).__new__(cls, *args, **kwargs)
          #cls._instances[args[0]] = super().__new__(cls, *args, **kwargs)
          #cls._instances[args[0]] = super(Multiton, cls).__new__(cls, *args, **kwargs)
          cls._instances[args[0]] = super().__new__(cls)
      return cls._instances[args[0]]
      #return cls._instances[args[0]](*args, **kwargs)
"""
"""
es = Instr('es')
us = Instr('us')
x = ('es')
es
us
x
id(es) == id(x)
id(es) == id(us)
id(x) = id(us)
"""
# ===========================================================
# Java style - factory pattern multiton
"""
class MyObject:
    def __init__(self, args):
        pass # Something Expensive

class MyObjectFactory:
    def __init__( self ):
        self.pool = {}
    def makeMyObject( self, args ):
        if args not in self.pool:
            self.pool[args] = MyObject( args )
        return self.pool[args]
"""
# ===========================================================
# Multiton decorator
def multiton(cls):
    instances = {}
    def get_instance(name):
        if name not in instances:
            instances[name] = cls()
        return instances[name]
    return get_instance

@multiton
class Instr_Singleton:
    def __init__(self):
        self.imported = False
        self.dt_lst = ['---']
