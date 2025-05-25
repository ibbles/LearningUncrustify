
/*
    Multiple namespaces on the same line.
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
class MyClass {
MyClass() {
	doInitialization();
}
};
}
}
}


/*
    Each namespace on its own line, brace on a new line.
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
class MyClass {
MyClass() {
	doInitialization();
}
};
}
}
}
