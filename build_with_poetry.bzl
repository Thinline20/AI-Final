def _build_with_custom_python_impl(ctx):
    

build_with_poetry = rule(implementation = _build_with_custom_python_impl
, attrs = {}
)