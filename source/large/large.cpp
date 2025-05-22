#include <iostream>
#include <string>

/*
Example code that:
- Uses spaces for indentation.
- Places braces on the same line.
- Indents the contents of namespaces.
- Indents the contents of classes.
*/

namespace MyNamespace {

    class Animal {
    public:
        Animal(const std::string& name) : name(name) {}

        // Inline function
        std::string getName() const {
            return name;
        }

        // Function declared inside but defined outside the class
        void setName(const std::string& newName);

    private:
        std::string name;
    };

    void Animal::setName(const std::string& newName) {
        name = newName;
    }

    class Dog : public Animal {
    public:
        Dog(const std::string& name) : Animal(name) {}

        // Inline function
        void bark() const {
            std::cout << getName() << " says Woof!" << std::endl;
        }
    };

    // Free function
    void makeAnimalSpeak(const Animal& animal) {
        std::cout << animal.getName() << " makes a sound." << std::endl;
    }

    // Another free function
    void renameAnimal(Animal& animal, const std::string& newName) {
        animal.setName(newName);
    }
}

int main() {
    MyNamespace::Dog myDog("Buddy");
    myDog.bark();

    MyNamespace::makeAnimalSpeak(myDog);

    MyNamespace::renameAnimal(myDog, "Max");
    myDog.bark();

    return 0;
}



/*
   Example code that:
   - Uses tabs for indentation.
   - Places braces on a new line.
   - Does not indent the contents of namespaces.
   - Does not indent the contents of classes.
   - Indents block comments with three spaces.
 */

/**
   The main namespace.
 */
namespace MyNamespace
{

/**
   Base class for all Animals.
 */
class Animal
{
public:
Animal(const std::string& name) : name(name) {
}

// Inline function
std::string getName() const
{
	return name;
}

// Function declared inside but defined outside the class
void setName(const std::string& newName);

private:
std::string name;
};

void Animal::setName(const std::string& newName)
{
	name = newName;
}

class Dog : public Animal
{
public:
Dog(const std::string& name) : Animal(name)
{
}

// Inline function
void bark() const
{
	std::cout << getName() << " says Woof!" << std::endl;
}
};

// Free function
void makeAnimalSpeak(const Animal& animal)
{
	std::cout << animal.getName() << " makes a sound." << std::endl;
}

// Another free function
void renameAnimal(Animal& animal, const std::string& newName)
{
	animal.setName(newName);
}
}

int main()
{
	MyNamespace::Dog myDog("Buddy");
	myDog.bark();

	MyNamespace::makeAnimalSpeak(myDog);

	MyNamespace::renameAnimal(myDog, "Max");
	myDog.bark();

	return 0;
}