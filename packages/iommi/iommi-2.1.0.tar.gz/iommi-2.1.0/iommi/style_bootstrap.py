from iommi.style import (
    Style,
)
from iommi.style_font_awesome_4 import font_awesome_4
from iommi.style_base import base

bootstrap_base = Style(
    base,
    base_template='iommi/base_bootstrap.html',
    Container=dict(
        tag='div',
        attrs__class={
            'container': True,
            'mt-5': True,
            'pt-5': True,
        },
    ),
    Field=dict(
        shortcuts=dict(
            boolean=dict(
                input__attrs__class={'form-check-input': True, 'form-control': False},
                attrs__class={'form-check': True},
                label__attrs__class={'form-check-label': True},
                template='iommi/form/bootstrap/row_checkbox.html',
            ),
            radio=dict(
                attrs__class={
                    'form-group': False,
                    'form-check': True,
                },
                input__attrs__class={
                    'form-check-input': True,
                    'form-control': False,
                },
            ),
        ),
        attrs__class={
            'form-group': True,
        },
        input__attrs__class={
            'form-control': True,
            'is-invalid': lambda field, **_: bool(field.errors),
        },
        errors__attrs__class={'invalid-feedback': True},
        template='iommi/form/bootstrap/row.html',
        help__attrs__class={
            'form-text': True,
            'text-muted': True,
        },
    ),
    Action=dict(
        shortcuts=dict(
            button__attrs__class={
                'btn': True,
                'btn-primary': True,
            },
            delete__attrs__class={
                'btn-primary': False,
                'btn-danger': True,
            },
        ),
    ),
    Table=dict(
        attrs__class__table=True,
        attrs__class={'table-sm': True},
    ),
    Column=dict(
        header__attrs__class={'text-nowrap': True},
        shortcuts=dict(
            select=dict(
                header__attrs__title='Select all',
                header__attrs__class={'text-center': True},
                cell__attrs__class={'text-center': True},

            ),
            number=dict(
                cell__attrs__class={'text-right': True},
                header__attrs__class={'text-right': True},
            ),
            boolean__cell__attrs__class={'text-center': True},
            delete=dict(
                cell__link__attrs__class={'text-danger': True},
            ),
        )
    ),
    Query=dict(
        form__iommi_style='bootstrap_horizontal',
        form_container=dict(
            tag='span',
            attrs__class={
                'form-row': True,
                'align-items-center': True,
            },
        ),
    ),
    Menu=dict(
        tag='nav',
        attrs__class={
            'navbar': True,
            'navbar-expand-lg': True,
            'navbar-dark': True,
            'bg-primary': True,
        },
        items_container__attrs__class={'navbar-nav': True},
        items_container__tag='ul'
    ),
    MenuItem=dict(
        tag='li',
        a__attrs__class={'nav-link': True},
        attrs__class={'nav-item': True},
    ),
    Paginator=dict(
        template='iommi/table/bootstrap/paginator.html',
        container__attrs__class__pagination=True,
        active_item__attrs__class={'page-item': True, 'active': True},
        link__attrs__class={'page-link': True},
        item__attrs__class={'page-item': True},
    ),
    Errors=dict(
        attrs__class={'text-danger': True},
    ),
    DebugMenu=dict(
        attrs__class={
            'bg-primary': False,
            'navbar': False,
            'navbar-dark': False,
        }
    ),
    Admin=dict(
        parts__menu=dict(
            # tag='foo',   # TODO: This styling is ignored. We should be able to do this.
            attrs__class={
                'fixed-top': True,
            },
        ),
    ),
    Errors__attrs__class={'with-errors': True},
)
bootstrap = Style(
    bootstrap_base,
    font_awesome_4,
)
bootstrap_horizontal = Style(
    bootstrap,
    Field=dict(
        shortcuts=dict(
            boolean__label__attrs__class={
                'col-form-label': True,
            },
        ),
        attrs__class={
            'form-group': False,
            'col-sm-3': True,
            'my-1': True,
        },
        errors__attrs__class={'invalid-feedback': True},
        errors__template='iommi/form/bootstrap/errors.html',
    ),
    Form__attrs__class={
        'align-items-center': True,
    },
)
