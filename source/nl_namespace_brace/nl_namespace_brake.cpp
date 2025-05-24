
/*
    Multiple namespaces on the same line.
    Namespace contents not indented.
 */

namespace A { namespace B { namespace C { } } }

namespace A { namespace B { namespace C {
class MyClass {
MyClass() {
	doInitialization();
}
};
} } }


/*
    Each namespace on its own line, brace on the same line.
    Namespace content indented.
 */

namespace A {
	namespace B {
		namespace C {
		}
	}
}

namespace A {
	namespace B {
		namespace C {
			class MyClass { MyClass() { doInitialization(); }};
		}
	}
}


/*
    Each namespace on its own line, brace on a new line.
    Namespace content indented.
 */

namespace A
{
	namespace B
	{
		namespace C
		{
		}
	}
}

namespace A
{
	namespace B
	{
		namespace C
		{
			class MyClass { MyClass() { doInitialization(); }};
		}
	}
}
