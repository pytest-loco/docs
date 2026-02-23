:tocdepth: 2

Context
=======

The context is the runtime state container for a case. Context variables
are accessible to instructions and can be used for dynamic behavior in test cases.
Context variables can be defined at the case level, step level, or imported from templates.

It holds:

* Case-level variables (defined by ``vars`` in a case)
* Case parameters (defined by ``params`` in a case)
* Template parameters (defined by ``params`` in a template)
* Environment variables (defined by ``envs`` in a case or a template)
* Step-level variables (defined by ``vars`` in a step)
* Step results (stored in ``result`` by default)
* Exported values
* Deferred expressions

Each case has its own isolated context.

Instructions such as ``!var result.status`` are compiled at parse time
but executed at runtime. Deferred evaluation allows instructions to access
the current state of the context when they are executed, rather than when
they are defined.

Deferred evaluation allows:

* Accessing results of previous steps
* Chained transformations
* Late binding of values
* Context-aware resolution

Evaluation order is deterministic and follows step order.
