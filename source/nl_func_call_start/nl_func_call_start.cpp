
class MyClass;

namespace MyClassHelpers
{
struct MyClassParticipant
{
	MyClassParticipant(MyClass& participant);
	MyClass& m_participant;
};
}

class MyClass
{
public:
MyClass(MyClass& firstChild, MyClass& secondChild);
MyClass(MyClassHelpers::MyClassParticipant firstChild, MyClassHelpers::MyClassParticipant secondChild);

void performRecursiveParticipantProcessing(MyClass& firstParticipant, MyClass& secondParticipant);
void performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant& firstChild, MyClassHelpers::MyClassParticipant& secondChild);

public:
MyClassHelpers::MyClassParticipant m_firstParticipant;
MyClassHelpers::MyClassParticipant m_secondParticipant;
};



/*
        Very long lines.
 */

void work(MyClass& myClass)
{
	myClass.performRecursiveParticipantProcessing(myClass.m_firstParticipant, myClass.m_secondParticipant);
}


/*
        Line break after first argument, not aligned with '('.
 */

void work(MyClass& myClass)
{
	myClass.performRecursiveParticipantProcessing(myClass.m_firstParticipant,
		myClass.m_secondParticipant);
}



/*
        Line break after '(', not aligned with '('.
 */

void work(MyClass& myClass)
{
	myClass.performRecursiveParticipantProcessing(
		myClass.m_firstParticipant, myClass.m_secondParticipant);
}


/*
        Line break after first argument, aligned with '('.
 */

void work(MyClass& myClass)
{
	myClass.performRecursiveParticipantProcessing(myClass.m_firstParticipant,
	                                              myClass.m_secondParticipant);
}


/*
        Function call that doesn't need any line brakes.
 */
void work(MyClass& myClass)
{
	myClass.performProcessing(firstParticipant, secondParticipant);
}