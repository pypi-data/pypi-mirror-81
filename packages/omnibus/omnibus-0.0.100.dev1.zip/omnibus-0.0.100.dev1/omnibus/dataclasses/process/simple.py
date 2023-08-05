import dataclasses as dc
import inspect
import typing as ta

from ... import code
from ... import properties
from ..internals import cmp_fn
from ..internals import FieldType
from ..internals import hash_action
from ..internals import PARAMS
from ..internals import POST_INIT_NAME
from ..internals import repr_fn
from ..internals import tuple_str
from ..pickling import SimplePickle
from ..types import _Placeholder
from ..types import PostInit
from .bootstrap import Fields
from .init import Init
from .types import Aspect
from .types import attach


class Repr(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Fields]

    def process(self) -> None:
        if not self.ctx.params.repr:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.repr]
        self.ctx.set_new_attribute('__repr__', repr_fn(flds, self.ctx.spec.globals))


class Eq(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Fields]

    def process(self) -> None:
        if not self.ctx.params.eq:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.compare]
        self_tuple = tuple_str('self', flds)
        other_tuple = tuple_str('other', flds)
        self.ctx.set_new_attribute(
            '__eq__',
            cmp_fn(
                '__eq__',
                '==',
                self_tuple,
                other_tuple,
                globals=self.ctx.spec.globals,
            ),
        )


class Order(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Fields]

    def check(self) -> None:
        if self.ctx.params.order and not self.ctx.params.eq:
            raise ValueError('eq must be true if order is true')

    def process(self) -> None:
        if not self.ctx.params.order:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.compare]
        self_tuple = tuple_str('self', flds)
        other_tuple = tuple_str('other', flds)
        for name, op in [
            ('__lt__', '<'),
            ('__le__', '<='),
            ('__gt__', '>'),
            ('__ge__', '>='),
        ]:
            if name in self.ctx.cls.__dict__:
                raise TypeError(
                    f'Cannot overwrite attribute {name} in class {self.ctx.cls.__name__}. '
                    f'Consider using functools.total_ordering')

            self.ctx.set_new_attribute(
                name,
                cmp_fn(
                    name,
                    op,
                    self_tuple,
                    other_tuple,
                    globals=self.ctx.spec.globals,
                )
            )


class Hash(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Fields]

    DEFAULT_CACHE_ATTR = '___hash'

    @properties.cached
    def cache_attr(self) -> ta.Optional[str]:
        if isinstance(self.ctx.spec.extra_params.cache_hash, str):
            return self.ctx.spec.extra_params.cache_hash
        elif self.ctx.spec.extra_params.cache_hash:
            return self.DEFAULT_CACHE_ATTR
        else:
            return None

    @property
    def slots(self) -> ta.AbstractSet[str]:
        return {self.cache_attr} if self.cache_attr is not None else set()

    def check(self) -> None:
        if self.cache_attr in self.ctx.spec.fields.by_name:
            raise AttributeError(self.cache_attr)

    def process(self) -> None:
        # Was this class defined with an explicit __hash__?  Note that if __eq__ is defined in this class, then python
        # will automatically set __hash__ to None.  This is a heuristic, as it's possible that such a __hash__ == None
        # was not auto-generated, but it close enough.
        class_hash = self.ctx.cls.__dict__.get('__hash__', dc.MISSING)
        has_explicit_hash = not (class_hash is dc.MISSING or (class_hash is None and '__eq__' in self.ctx.cls.__dict__))
        ha = hash_action[(
            bool(self.ctx.params.unsafe_hash),
            bool(self.ctx.params.eq),
            bool(self.ctx.params.frozen),
            has_explicit_hash,
        )]
        if not ha:
            return
        fn = ha(self.ctx.cls, self.ctx.spec.fields.instance, self.ctx.spec.globals)

        if self.ctx.spec.extra_params.cache_hash:
            attr = self.cache_attr
            self.ctx.set_new_attribute(attr, None)
            ofn = fn

            def fn(obj):
                hsh = getattr(obj, attr)
                if hsh is None:
                    hsh = ofn(obj)
                    object.__setattr__(obj, attr, hsh)
                return hsh

        self.ctx.cls.__hash__ = fn


class Doc(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Init]

    def process(self) -> None:
        if not getattr(self.ctx.cls, '__doc__'):
            sig = inspect.signature(self.ctx.cls)
            self.ctx.cls.__doc__ = self.ctx.cls.__name__ + str(sig).replace(' -> None', '')


class PostInitAspect(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Fields]

    @attach('init')
    class Init(Aspect.Function['PostInitAspect']):

        @attach(Aspect.Function.Phase.POST)
        def build_post_init_lines(self) -> ta.List[str]:
            if not self.fctx.ctx.spec.params.init:
                return []

            ret = []
            if hasattr(self.fctx.ctx.cls, POST_INIT_NAME):
                params_str = ','.join(f.name for f in self.fctx.ctx.spec.fields.by_field_type.get(FieldType.INIT, []))
                ret.append(f'{self.fctx.self_name}.{POST_INIT_NAME}({params_str})')
            return ret

        @attach(Aspect.Function.Phase.POST)
        def build_extra_post_init_lines(self) -> ta.List[str]:
            if not self.fctx.ctx.spec.params.init:
                return []

            ret = []
            for pi in self.fctx.ctx.spec.rmro_extras_by_cls[PostInit]:
                ret.append(f'{self.fctx.nsb.put(pi.fn)}({self.fctx.self_name})')
            return ret


class Pickle(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Fields]

    def process(self) -> None:
        if self.ctx.extra_params.pickle and self.ctx.cls.__reduce__ is object.__reduce__:
            setattr(self.ctx.cls, '__reduce__', SimplePickle.__reduce__)


class Placeholders(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Init]

    def check(self) -> None:
        for a, v in self.ctx.cls.__dict__.items():
            if v is _Placeholder:
                raise TypeError(f'Processed class contains placeholder: {a}')


class Frozen(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Fields]

    def check(self) -> None:
        dc_rmro = [b for b in self.ctx.spec.rmro[:-1] if dc.is_dataclass(b)]
        if dc_rmro:
            any_frozen_base = any(getattr(b, PARAMS).frozen for b in dc_rmro)
            if any_frozen_base:
                if not self.ctx.params.frozen:
                    raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
            elif self.ctx.params.frozen:
                raise TypeError('cannot inherit frozen dataclass from a non-frozen one')

    def process(self) -> None:
        if not self.ctx.params.frozen:
            return

        if not self.ctx.extra_params.allow_setattr:
            slots = [s for a in self.ctx.aspects for s in a.slots]
            locals = {
                'cls': self.ctx.cls,
                'FrozenInstanceError': dc.FrozenInstanceError,
                'allowed': frozenset(self.ctx.spec.fields.by_name) | frozenset(slots),
            }

            for fnname in ['__setattr__', '__delattr__']:
                args = ['name'] + (['value'] if fnname == '__setattr__' else [])
                fn = code.create_function(
                    fnname,
                    code.ArgSpec(['self'] + args),
                    '\n'.join([
                        f'if type(self) is cls and name in allowed:',
                        f'    raise FrozenInstanceError(f"cannot assign to field {{name!r}}")',
                        f'super(cls, self).{fnname}({", ".join(args)})',
                    ]),
                    locals=locals,
                    globals=self.ctx.spec.globals,
                )
                self.ctx.set_new_attribute(fn.__name__, fn, raise_=True)
